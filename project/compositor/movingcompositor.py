import logging
from random import randrange
from typing import List

from moviepy.editor import VideoClip
from moviepy.video.VideoClip import ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.fx.resize import resize

from compositor.compositor import Compositor
from config.config import Config
from utils.timer import timer
from utils.pair import Pair
from video_generator.video import Video


def get_closest_square(num: int) -> int:
    val = 1
    while val * val < num:
        val += 1
    return val


def calculate_max_videos(clips: List[Video]) -> int:
    max_count = 0
    count = 0
    start = []
    end = []

    for clip in clips:
        start.append(clip.start)
        end.append(clip.end)

    start.sort()
    end.sort()

    i = 0
    j = 0

    while i < len(clips):
        if start[i] <= end[j]:
            count = count + 1
            if count > max_count:
                max_count = count
            i = i + 1
        else:
            count = count - 1
            j = j + 1

    return max_count


class MovingCompositor(Compositor):
    grid_state = None
    frame_dimension = None
    grid = None

    def __init__(self, config: Config):
        super().__init__(config)

    @timer
    def apply(self, data: dict):
        self.validate(data)

        clips: List[Video] = data["clips"]

        max_vids = calculate_max_videos(clips)
        sqrt = get_closest_square(max_vids)
        self.grid = Pair(sqrt, sqrt)

        bg_video = ImageClip(self.config.data["background_path"])
        bg_video = resize(bg_video, self.config.frame_size.get()).set_duration(self.config.duration)

        final_clips = [bg_video]
        positioned_clips = self.position_clips(clips)

        block_size = Pair(int(self.config.frame_size.first / self.grid.first),
                          int(self.config.frame_size.second / self.grid.second))
        for clip in positioned_clips:
            final_clips.append(self.resize_clip(clip, block_size))

        logging.debug("Positioned %s clips", len(final_clips))

        video = CompositeVideoClip(final_clips, use_bgclip=True)
        data["composite_video"] = video
        return data

    def validate(self, data: dict):
        if "clips" not in data or not data["clips"]:
            raise AssertionError("Clip list empty. Cannot composite")

        if any(clip is None for clip in data["clips"]):
            raise AssertionError("NoneType clips are not allowed")

    def resize_clip(self, clip: VideoClip, size: Pair):
        x, y = clip.size
        if x > y:
            return resize(clip, height=size.second)
        return resize(clip, width=size.first)

    def position_clips(self, clips: List[Video]):
        result = []

        # Divide into 4 quadrants and move around clip
        quadrant_size = Pair(int(self.config.frame_size.first / 2), int(self.config.frame_size.second / 2))
        clip_quadrant = 0

        for clip in clips:
            clip_quadrant = (clip_quadrant + 1) % 4
            quadrant_min = Pair(clip_quadrant / 2 * quadrant_size.first, (clip_quadrant % 2) * quadrant_size.second)
            position = Pair(randrange(quadrant_min.first, quadrant_min.first + quadrant_size.first),
                            randrange(quadrant_min.second, quadrant_min.second + quadrant_size.second))

            direction = Pair(randrange(-100, 100), randrange(-100, 100))
            new_clip = clip.get().set_position(lambda t, px=position.first, dx=direction.first, py=position.second,
                                                      dy=direction.second: (px + dx * t, py + dy * t))
            result.append(new_clip)
            logging.debug("Positioned video with position %s and direction %s", position, direction)

        return result

    @classmethod
    def create_from_config(cls, config: Config):
        return MovingCompositor(config)

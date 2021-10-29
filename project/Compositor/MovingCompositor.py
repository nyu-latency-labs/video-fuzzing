import logging
from random import randrange

from moviepy.video.VideoClip import ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.fx.resize import resize
from moviepy.video.fx.crop import crop
from moviepy.editor import VideoClip

from Compositor.Compositor import Compositor
from Config.Config import Config
from Utils.XY import XY
from Utils.Timer import timer


def get_closest_square(num):
    val = 1
    while val * val < num:
        val += 1
    return val


def calculate_max_videos(clips):
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


def find_empty_position(grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 0:
                logging.debug("getting grid location %s, %s", i, j)
                return XY(i, j)

    return None


class MovingCompositor(Compositor):
    grid_state = None
    frame_dimension = None
    grid = None

    def __init__(self, config: Config):
        super().__init__(config)

    @timer
    def apply(self, data):
        clips = data["clips"]

        if clips is None or clips is []:
            return ImageClip(self.config.data["background_path"]).resize(self.config.frame_size.get_xy())

        max_vids = calculate_max_videos(clips)
        sqrt = get_closest_square(max_vids)
        self.grid = XY(sqrt, sqrt)

        bg_video = ImageClip(self.config.data["background_path"])
        bg_video = resize(bg_video, self.config.frame_size.get_xy()).set_duration(self.config.duration)

        clipped_clips = []

        # Based on video overlap flag, crop/resize the videos to increase throughput
        block_size = XY(self.config.frame_size.x / self.grid.x, self.config.frame_size.y / self.grid.y)
        if self.config.data["allow_overlap"]:
            for clip in clips:
                clipped_clips.append(self.crop_clips(clip, block_size))

        else:
            for clip in clips:
                clipped_clips.append(self.resize_clip(clip, block_size))

        final_clips = [bg_video]
        positioned_clips = self.position_clips(clipped_clips)

        final_clips.extend(positioned_clips)
        logging.debug("Positioned %s clips", len(final_clips))

        video = CompositeVideoClip(final_clips, use_bgclip=True)
        data["composite_video"] = video
        return data

    def resize_clip(self, clip: VideoClip, size: XY):
        x, y = clip.size
        if x > y:
            return resize(clip, height=size.y)
        return resize(clip, width=size.x)

    def position_clips(self, clips):
        result = []

        # Divide into 4 quadrants and move around clip
        quadrant_size = XY(self.config.frame_size.x / 2, self.config.frame_size.y / 2)
        clip_quadrant = 0

        for clip in clips:
            clip_quadrant = (clip_quadrant + 1) % 4
            quadrant_min = XY(clip_quadrant / 2 * quadrant_size.x, (clip_quadrant % 2) * quadrant_size.y)
            position = XY(randrange(quadrant_min.x, quadrant_min.x + quadrant_size.x),
                          randrange(quadrant_min.y, quadrant_min.y + quadrant_size.y))

            direction = XY(randrange(-100, 100), randrange(-100, 100))
            new_clip = clip.set_position(lambda t: (position.x + direction.x*t, position.y + direction.y*t))
            result.append(new_clip)
            logging.debug("Positioned video with position %s and direction %s", position, direction)
            # Everytime a new position lambda is created and added to the list, all others become the same value
        return result

    @classmethod
    def create_from_config(cls, config: Config):
        return MovingCompositor(config)

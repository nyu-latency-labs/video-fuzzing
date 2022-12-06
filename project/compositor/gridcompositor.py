import logging
from typing import Optional
from typing import List

from moviepy.editor import VideoClip
from moviepy.video.VideoClip import ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.fx.crop import crop
from moviepy.video.fx.resize import resize

from compositor.compositor import Compositor
from config.config import Config
from event.event import Event, EventType
from event.eventsimulator import EventSimulator
from utility.timer import timer
from utility.pair import Pair
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
        if start[i] < end[j]:
            count = count + 1
            if count > max_count:
                max_count = count
            i = i + 1
        elif start[i] > end[j]:
            count = count - 1
            j = j + 1
        else:
            i += 1
            j += 1

    return max_count


def find_empty_position(grid) -> Optional[Pair]:
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 0:
                logging.debug("getting grid location %s, %s", i, j)
                return Pair(i, j)

    return None


class GridCompositor(Compositor):
    grid_state = None
    frame_dimension = None
    grid = None

    def __init__(self, config: Config):
        super().__init__(config)

    @timer
    def apply(self, data: dict):
        self.validate(data)

        clips: List[Video] = data["clips"]

        # Create grid and put videos into positions
        # Calc max videos at a time
        max_videos = calculate_max_videos(clips)
        sqrt = get_closest_square(max_videos)
        self.grid = Pair(sqrt, sqrt)

        bg_video = ImageClip(self.config.data["background_path"])
        bg_video = resize(bg_video, self.config.frame_size.get()).set_duration(self.config.duration)

        self.grid_state = [[0 for i in range(self.grid.first)] for j in range(self.grid.second)]

        final_clips = [bg_video]
        positioned_clips = self.position_clips(clips)
        logging.debug("Positioned %s clips", len(positioned_clips))

        # Based on video overlap flag, crop/resize the videos to increase throughput
        if self.config.allow_overlap:
            final_clips.extend(positioned_clips)
        else:
            block_size = Pair((self.config.frame_size.first / self.grid.first),
                              (self.config.frame_size.second / self.grid.second))
            for clip in positioned_clips:
                final_clips.append(self.resize_clip(clip, block_size))

        video = CompositeVideoClip(final_clips, use_bgclip=True)
        video.fps = self.config.fps
        data["video"] = video
        return data

    def validate(self, data: dict):
        if "clips" not in data or not data["clips"]:
            raise AssertionError("Clip list empty. Cannot composite")

        if any(clip is None for clip in data["clips"]):
            raise AssertionError("NoneType clips are not allowed")

    def crop_clips(self, clip: VideoClip, size: Pair):
        return crop(clip, x1=0, y1=0, x2=size.first, y2=size.second)

    def position_clips(self, clips: List[Video]):
        simulator = EventSimulator()
        result = []

        for clip in clips:
            event = Event(EventType.VIDEO_START, clip.start, clip)
            simulator.add(event)

        end_simulation_event = Event(EventType.END_SIMULATION, self.config.duration)
        simulator.add(end_simulation_event)

        block_size = Pair(int(self.config.frame_size.first / self.grid.first),
                          int(self.config.frame_size.second / self.grid.second))

        while not simulator.empty():
            curr_event = simulator.get()

            if curr_event.event_type is EventType.END_SIMULATION:
                break

            if curr_event.event_type == EventType.VIDEO_START:
                position = find_empty_position(self.grid_state)
                if position is None:
                    continue

                self.grid_state[position.first][position.second] = 1

                new_position = block_size.first * position.first, block_size.second * position.second
                new_clip = curr_event.clip.get().set_position(new_position)

                end_event = Event(EventType.VIDEO_END, new_clip.end, new_clip, position)
                logging.debug("Setting event with data %s, %s", end_event.data.first, end_event.data.second)
                result.append(new_clip)

                simulator.add(end_event)
            elif curr_event.event_type == EventType.VIDEO_END:
                position = curr_event.data
                self.grid_state[position.first][position.second] = 0

        return result

    @classmethod
    def create_from_config(cls, config: Config):
        return GridCompositor(config)

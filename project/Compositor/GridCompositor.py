import logging

from moviepy.video.VideoClip import ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.fx.resize import resize
from moviepy.video.fx.crop import crop
from moviepy.editor import VideoClip


from Compositor.Compositor import Compositor
from Config.Config import Config
from Event.Event import Event, EventType
from Event.EventSimulator import EventSimulator
from Config.XY import XY


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


class GridCompositor(Compositor):
    grid_state = None
    frame_dimension = None
    grid = None

    def __init__(self, config: Config):
        super().__init__(config)

    def apply(self, clips):
        logging.debug("Positioned %s clips", len(clips))

        if clips is None or clips is []:
            return ImageClip(self.config.data["background_path"]).resize(self.config.frame_size.get_xy())

        # Create grid and put videos into positions

        # Calc max videos at a time
        max_vids = calculate_max_videos(clips)
        sqrt = get_closest_square(max_vids)
        self.grid = XY(sqrt, sqrt)

        bg_video = ImageClip(self.config.data["background_path"])
        bg_video = resize(bg_video, self.config.frame_size.get_xy()).set_duration(self.config.duration)

        self.grid_state = [[0 for i in range(self.grid.x)] for j in range(self.grid.y)]

        final_clips = [bg_video]
        positioned_clips = self.position_clips(clips)
        logging.debug("Positioned %s clips", len(positioned_clips))

        # Based on video overlap flag, crop/resize the videos to increase throughput
        block_size = XY(self.config.frame_size.x / self.grid.x, self.config.frame_size.y / self.grid.y)
        if self.config.data["allow_overlap"]:
            for clip in positioned_clips:
                final_clips.append(self.crop_clips(clip, block_size))

        else:
            for clip in positioned_clips:
                final_clips.append(self.resize_clip(clip, block_size))

        video = CompositeVideoClip(final_clips, use_bgclip=True).set_audio(None)
        return video

    def crop_clips(self, clip: VideoClip, size: XY):
        x, y = clip.position
        return crop(clip, x1=x, y1=y, x2=x+size.x, y2=y+size.y)

    def resize_clip(self, clip: VideoClip, size: XY):
        x, y = clip.size
        if x > y:
            return resize(clip, height=size.y)
        return resize(clip, width=size.x)

    def position_clips(self, clips):
        simulator = EventSimulator()
        result = []

        for clip in clips:
            event = Event(EventType.VIDEO_START, clip.start, clip)
            simulator.add_event(event)

        end_simulation_event = Event(EventType.END_SIMULATION, self.config.duration)
        simulator.add_event(end_simulation_event)

        block_size = XY(self.config.frame_size.x / self.grid.x, self.config.frame_size.y / self.grid.y)

        while simulator.has_event():
            curr_event = simulator.get_event()

            if curr_event.event_type is EventType.END_SIMULATION:
                break

            if curr_event.event_type == EventType.VIDEO_START:
                position = find_empty_position(self.grid_state)
                if position is None:
                    continue

                self.grid_state[position.x][position.y] = 1

                new_position = block_size.x * position.x, block_size.y * position.y
                new_clip = curr_event.clip.set_position(new_position)

                assert type(position) == XY
                end_event = Event(EventType.VIDEO_END, new_clip.end, new_clip, position)
                logging.debug("Setting event with data %s, %s", end_event.data.x, end_event.data.y)
                result.append(new_clip)

                simulator.add_event(end_event)
            elif curr_event.event_type == EventType.VIDEO_END:
                position = curr_event.data
                self.grid_state[position.x][position.y] = 0

        return result

    @classmethod
    def create_from_config(cls, config: Config):
        return GridCompositor(config)

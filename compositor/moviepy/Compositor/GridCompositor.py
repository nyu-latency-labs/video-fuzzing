from moviepy.video.VideoClip import ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip

from Compositor.Compositor import Compositor
from Event import Event, EventType
from Event.EventSimulator import EventSimulator
from xy import XY


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
        start.append(clip.start_time)
        end.append(clip.end_time)

    start.sort()
    end.sort()

    i = 1
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
                return XY(i, j)

    return None


class BasicCompositor(Compositor):
    duration = None
    grid_state = None
    frame_dimension = None
    grid = None

    def __init__(self, duration):
        super().__init__()
        self.duration = duration

    def apply(self, bg, clips=None):
        if clips is None:
            return ImageClip(bg).set_duration(self.duration)

        # Create grid and put videos into positions

        # Calc max videos at a time
        max_vids = calculate_max_videos(clips)
        sqrt = get_closest_square(max_vids)
        self.grid = XY(sqrt, sqrt)

        bg_video = ImageClip(bg)
        self.frame_dimension = XY(bg_video.w, bg_video.h)

        self.grid_state = [[0 for i in range(self.grid.x)] for j in range(self.grid.y)]

        positioned_clips = [bg_video, self.position_clips(clips)]

        video = CompositeVideoClip(positioned_clips, use_bgclip=True).set_audio(None)
        return video

    def position_clips(self, clips):
        simulator = EventSimulator()
        result = []

        for clip in clips:
            event = Event(EventType.START, clip.start_time, clip)
            simulator.add_event(event)

        block_size = XY(self.frame_dimension.x/self.grid.x, self.frame_dimension.y/self.grid.y)

        curr_event = simulator.get_event()
        while curr_event is not None:

            if curr_event.event_type == EventType.START:
                position = find_empty_position(self.grid_state)
                if position is None:
                    continue

                self.grid_state[position.x][position.y] = 1

                new_position = block_size.x*position.x, block_size.y*position.y
                new_clip = curr_event.clip.clip.set_position(new_position)

                end_event = GridEvent(EventType.END, clip.end_time, new_clip)
                end_event.set_data(position)
                result.append(new_clip)

                simulator.add_event(end_event)
            elif curr_event.event_type == EventType.END:
                position = curr_event.data
                self.grid_state[position.x][position.y] = 0

        return result

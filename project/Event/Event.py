from enum import Enum

from moviepy.video.VideoClip import VideoClip


class EventType(Enum):
    VIDEO_START = 1
    VIDEO_END = 2
    INTERVAL = 3
    END_SIMULATION = 4


class Event:
    event_type = None
    time = None
    clip = None
    data = None  # To store any custom data required for processing

    def __init__(self, event_type: EventType, time, clip: VideoClip = None, data=None):
        self.event_type = event_type
        self.time = time
        self.clip = clip
        self.data = data

    def __lt__(self, other):
        return self.time < other.time

    def set_data(self, data):
        self.data = data

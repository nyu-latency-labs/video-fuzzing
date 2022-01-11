from enum import Enum
from typing import Any, Union

from moviepy.Clip import Clip
from moviepy.video.VideoClip import ImageClip, VideoClip


class EventType(Enum):
    VIDEO_START = 1
    VIDEO_END = 2
    INTERVAL = 3
    END_SIMULATION = 4


class Event:
    event_type: EventType = None
    time: int = None
    clip: Union[VideoClip, ImageClip] = None
    data = None  # To store any custom data required for processing

    def __init__(self, event_type: EventType, time: int, clip: Union[VideoClip, ImageClip] = None, data: Any = None):
        self.event_type = event_type
        self.time = time
        self.clip = clip
        self.data = data

    def __lt__(self, other):
        return self.time < other.time

    def set(self, data):
        self.data = data

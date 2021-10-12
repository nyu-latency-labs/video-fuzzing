from enum import Enum

from Video import Video


class EventType(Enum):
    START = 1
    END = 2


class Event:
    event_type = None
    time = None
    clip = None

    def __init__(self, event_type: EventType, time, clip: Video):
        self.event_type = event_type
        self.time = time
        self.clip = clip

    def __lt__(self, other):
        return self.time < other.time
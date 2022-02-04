import bisect
import logging
from typing import Optional
from typing import List

from event.event import EventType, Event


class EventSimulator:
    events: List[Event] = []

    def __init__(self):
        self.events = []
        pass

    def add(self, event: Event):
        if event.event_type == EventType.VIDEO_END:
            # Remove video the first thing in the future instant
            bisect.insort_left(self.events, event)
        else:
            # Add all other events after
            bisect.insort_right(self.events, event)

        logging.debug("Added event of type %s at time %s and data is %s", event.event_type, event.time, event.data)

    def empty(self) -> bool:
        return len(self.events) == 0

    def has_video_event(self) -> bool:
        return any(e.event_type is EventType.VIDEO_END for e in self.events)

    def get(self) -> Optional[Event]:
        if len(self.events) > 0:
            current_event = self.events.pop(0)
            logging.debug("Got event of type %s at time %s and data is %s", current_event.event_type,
                          current_event.time, current_event.data)
            return current_event
        return None

    def get_video_event(self) -> Event:
        event = next((e for e in self.events if e.event_type is EventType.VIDEO_END), None)

        if event is None:
            raise IndexError("No more video events found")

        self.events.remove(event)
        logging.debug("Removing video event at time %s", event.time)
        return event

    def get_video_events_in_progress(self) -> int:
        return sum(1 for event in self.events if event.event_type is EventType.VIDEO_END)

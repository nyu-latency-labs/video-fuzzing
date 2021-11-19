import bisect
import logging

from Event import Event
from Event.Event import EventType


class EventSimulator:
    events = []

    def __init__(self):
        self.events = []
        pass

    def add_event(self, event: Event):
        if event.event_type == EventType.VIDEO_END:
            bisect.insort_left(self.events, event)
        else:
            bisect.insort_right(self.events, event)
        logging.debug("Added event of type %s at time %s and data is %s", event.event_type, event.time, event.data)

    def has_event(self):
        return len(self.events) > 0

    def has_video_event(self):
        for e in self.events:
            if e.event_type is EventType.VIDEO_END:
                return True
        return False

    def get_event(self) -> Event:
        if len(self.events) > 0:
            current_event = self.events.pop(0)
            logging.debug("Got event of type %s at time %s and data is %s", current_event.event_type,
                          current_event.time, current_event.data)
            return current_event
        return None

    def get_video_event(self) -> Event:
        for e in self.events:
            if e.event_type is EventType.VIDEO_END:
                self.events.remove(e)
                logging.debug("Removing video event at time %s", e.time)
                return e

        raise IndexError("No more video events found")

    def get_video_events_in_progress(self):
        res = 0

        for i in self.events:
            if i.event_type is EventType.VIDEO_END:
                res += 1

        return res


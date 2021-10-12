from bisect import bisect


class EventSimulator:
    events = []

    def __init__(self):
        pass

    def add_event(self, event):
        bisect.insort_right(self.events, event)

    def get_event(self):
        if len(self.events) > 0:
            return self.events.pop()
        return None


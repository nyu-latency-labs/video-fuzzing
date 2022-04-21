import math


class Alpine:

    def __init__(self, data: dict):
        self.multiplier = data.get("multiplier", 1)
        self.x = 0

    def next(self):
        self.x += 1
        return int(self.multiplier * math.sin(self.x) * math.sqrt(self.x))

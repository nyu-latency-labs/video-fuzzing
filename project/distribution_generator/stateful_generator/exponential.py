import math


class Exponential:

    def __init__(self, data: dict):
        self.lam = data["lambda"]
        self.x = 0

    def next(self) -> int:
        self.x += 1
        return int(self.lam * math.exp(-0.15 * self.x))

from __future__ import annotations

from typing import Tuple


class Pair:
    """
    Used to represent any type of data pair of the same type.
    """
    first = 0
    second = 0

    def __init__(self, first: int, second: int):
        self.first = first
        self.second = second

    def get(self) -> Tuple[int, int]:
        return self.first, self.second

    @classmethod
    def from_tuple(cls, tup) -> Pair:
        (first, second) = tup
        return Pair(first, second)

    def __str__(self):
        return "[" + str(self.first) + ", " + str(self.second) + "]"

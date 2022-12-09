from typing import Tuple, Union


class Pair:
    """
    Used to represent any type of data pair of the same type.
    """
    first = 0
    second = 0

    def __init__(self, first: Union[int, float], second: Union[int, float]):
        self.first = first
        self.second = second

    def get(self) -> Tuple[int, int]:
        return self.first, self.second

    @classmethod
    def from_tuple(cls, tup):
        (first, second) = tup
        return Pair(first, second)

    def __str__(self):
        return "[" + str(self.first) + ", " + str(self.second) + "]"
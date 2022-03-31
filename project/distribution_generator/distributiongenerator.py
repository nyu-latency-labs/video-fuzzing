import logging
import random
from typing import Callable


class DistributionGenerator:
    fn: Callable = None
    ds: dict = None

    def __init__(self, ds: dict, fn: Callable = None):
        self.fn = fn
        self.ds = ds

    def next(self):
        return self.fn()

    def process_distribution(self) -> Callable:
        ds_type = self.ds["type"]

        if ds_type == "normal":
            return lambda: random.gauss(self.ds["mean"], self.ds["std"])
        elif ds_type == "linear":
            return lambda: self.ds["value"]
        elif ds_type == "choice":
            return lambda: random.choice(self.ds["value"])
        else:
            raise NotImplementedError(f"{ds_type} is not implemented")

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['fn']

        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.fn = self.process_distribution()

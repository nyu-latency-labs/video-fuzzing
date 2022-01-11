import random
from typing import Callable

from distribution_generator.distributiongenerator import DistributionGenerator


class FixedRandomDG(DistributionGenerator):
    random_state = None
    fixed_fn = None

    def __init__(self, ds: dict, time: int, fn: Callable = None):
        super().__init__(ds)

        self.fixed_fn = lambda: time

        self.fn = fn if fn is not None else self.process_distribution()

        # random.seed(10)
        random.seed(random.randint(1, 100))

        self.random_state = random.getstate()

    def next(self):
        if self.fixed_fn is not None:
            temp = self.fixed_fn()
            self.fixed_fn = None
            return temp

        random.setstate(self.random_state)
        data = self.fn()
        self.random_state = random.getstate()
        return data

import random
from typing import Callable

from ..distribution_generator.distributiongenerator import DistributionGenerator


class RandomDG(DistributionGenerator):
    random_state = None

    def __init__(self, ds: dict, fn: Callable = None):
        super().__init__(ds)

        self.fn = fn if fn is not None else self.process_distribution()

        # random.seed(10)
        random.seed(random.randint(1, 100))

        self.random_state = random.getstate()

    def next(self):
        random.setstate(self.random_state)
        data = self.fn()
        self.random_state = random.getstate()
        return data

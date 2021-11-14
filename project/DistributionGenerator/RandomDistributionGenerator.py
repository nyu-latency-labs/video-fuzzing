from DistributionGenerator.DistributionGenerator import DistributionGenerator
import random


class RandomDistributionGenerator(DistributionGenerator):
    random_state = None

    def __init__(self, fn):
        super().__init__(fn)
        random.seed(10)
        self.random_state = random.getstate()

    def get_next(self):
        random.setstate(self.random_state)
        data = self.fn()
        self.random_state = random.getstate()
        return data



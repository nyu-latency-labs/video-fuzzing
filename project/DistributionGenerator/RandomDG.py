import random

from DistributionGenerator.DistributionGenerator import DistributionGenerator


class RandomDistributionGenerator(DistributionGenerator):
    random_state = None

    def __init__(self, ds, fn=None):
        super().__init__(ds)

        if fn is not None:
            self.fn = fn
        else:
            self.process_distribution()

        random.seed(10)
        self.random_state = random.getstate()

    def get_next(self):
        random.setstate(self.random_state)
        data = self.fn()
        self.random_state = random.getstate()
        return data

    def process_distribution(self):
        ds_type = self.ds["type"]

        if ds_type == "normal":
            self.fn = lambda: random.gauss(self.ds["mean"], self.ds["std"])
        elif ds_type == "linear":
            self.fn = lambda: self.ds["value"]
        elif ds_type == "choice":
            self.fn = lambda: random.choice(self.ds["value"])

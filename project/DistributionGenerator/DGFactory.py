from DistributionGenerator.FixedRandomDG import FixedRandomDG
from DistributionGenerator.RandomDG import RandomDG


class DGFactory:

    @classmethod
    def get_distribution_generator(cls, data, time=None):
        ds_type = data["type"]

        if "fixed_objects" in data:
            return FixedRandomDG(data, time)
        if ds_type == "normal":
            return RandomDG(data)
        elif ds_type == "linear":
            return RandomDG(data)
        elif ds_type == "choice":
            return RandomDG(data)

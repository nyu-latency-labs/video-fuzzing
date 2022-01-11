from distribution_generator.distributiongenerator import DistributionGenerator
from distribution_generator.fixedrandomdg import FixedRandomDG
from distribution_generator.randomdg import RandomDG


class DGFactory:

    @classmethod
    def get_distribution_generator(cls, data: dict, time: int = None) -> DistributionGenerator:
        ds_type = data["type"]

        if "fixed_objects" in data:
            return FixedRandomDG(data, time)
        else:
            return RandomDG(data)

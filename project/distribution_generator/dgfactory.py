import logging
from enum import IntEnum
import random

from distribution_generator.distributiongenerator import DistributionGenerator
from distribution_generator.fixedrandomdg import FixedRandomDG
from distribution_generator.randomdg import RandomDG


class DistributionType(IntEnum):
    NORMAL = 0
    LINEAR = 1


class DGFactory:

    @classmethod
    def get_distribution_generator(cls, data: dict) -> DistributionGenerator:
        ds_type = data["type"]

        if "fixed_objects" in data:
            return FixedRandomDG(data)
        elif ds_type == "random":
            data = get_random_distribution(data["max_value"])
            return RandomDG(data)
        else:
            return RandomDG(data)


def get_random_distribution(max_value) -> dict:
    ds_type = random.randint(0, len(DistributionType) - 1)
    result = None

    # TODO Better formula?
    if ds_type == 0:
        mean = random.randint(0, max_value)
        std = random.randint(0, int((max_value-mean)/2))
        result = {"type": "normal", "mean": mean, "std": std}
    elif ds_type == 1:
        result = {"type": "linear", "value": random.randint(0, max_value)}

    logging.debug(f"Random distribution with value {result} created.")
    return result

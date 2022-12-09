import logging
from enum import IntEnum
import random
from typing import Union

from ..distribution_generator.distributiongenerator import DistributionGenerator
from ..distribution_generator.fixedrandomdg import FixedRandomDG
from ..distribution_generator.randomdg import RandomDG
from ..distribution_generator.stateful_generator.alpine import Alpine
from ..distribution_generator.stateful_generator.exponential import Exponential


class DistributionType(IntEnum):
    NORMAL = 0
    LINEAR = 1
    ALPINE = 1
    EXPONENTIAL = 1


class DGFactory:

    @classmethod
    def get_distribution_generator(cls, data: dict) -> Union[DistributionGenerator, Exponential, Alpine]:
        ds_type = data["type"]

        if ds_type == "random":
            data = cls.get_random_distribution(data["max_value"])
            return RandomDG(data)
        elif ds_type == "exponential":
            return Exponential(data)
        elif ds_type == "alpine":
            return Alpine(data)
        else:
            return RandomDG(data)

    @classmethod
    def get_random_distribution(cls, max_value) -> dict:
        ds_type = random.randint(0, len(DistributionType) - 1)
        result = None

        # TODO Better formula?
        if ds_type == 0:
            mean = random.randint(1, max_value)
            std = random.randint(0, int((max_value - mean) / 2))
            result = {"type": "normal", "mean": mean, "std": std}
        elif ds_type == 1:
            result = {"type": "linear", "value": random.randint(1, max_value)}
        elif ds_type == 2:
            result = {"type": "alpine", "multiplier": random.randint(1, max_value), "downscale": random.randint(1, 10)}
        elif ds_type == 3:
            result = {"type": "exponential", "lambda": random.randint(1, max_value)}

        logging.debug(f"Random distribution with value {result} created.")
        return result

import logging
from math import ceil
from random import choices

from Config.Config import Config
from Fuzzer.Fuzzer import Fuzzer
from Utils.Timer import timer
from Processor.PreProcessor import generate_distribution


class ExperimentFuzzer(Fuzzer):

    def __init__(self, config: Config, data=None):
        super().__init__(config, data)
        self.name = "experiment_fuzzer"

    @timer
    def apply(self, data):
        # Send list of data to be sent down the pipeline
        new_data = []
        for tx in self.transformers:
            local_transforms = {
                "applied": False,
                "transformers": [tx],
                "type": "local"
            }

            obj = {
                "object_distribution": self.config.object_distribution_fn,
                "time_distribution_fn": self.config.time_distribution_fn,
                # "object_types": object_types,
                "num_videos": self.data["num_videos"],
                "filename_prefix": self.name + "_" + tx.name,
            }

            new_obj = {**obj, **data}
            new_obj["transformers"].append(local_transforms)

            new_data.append(new_obj)

        return new_data

    @classmethod
    def create_from_config(cls, config: Config, data):
        return ExperimentFuzzer(config, data)

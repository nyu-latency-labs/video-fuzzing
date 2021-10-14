import logging
from math import ceil
from random import choices

from Config.Config import Config
from Fuzzer.Fuzzer import Fuzzer
from Processor.PreProcessor import generate_distribution


class ExperimentFuzzer(Fuzzer):

    def __init__(self, config: Config, data=None):
        super().__init__(config, data)
        self.name = "experiment_fuzzer"

    def apply(self, data=None):
        object_distribution = generate_distribution(self.config.object_distribution_fn,
                                                    ceil(self.config.duration/self.config.step_size))

        # Generate a large enough distribution
        num_distributions = int(self.config.duration * sum(object_distribution))
        logging.info("Generating distributions of size %s", num_distributions)

        time_distribution = generate_distribution(self.config.time_distribution_fn, num_distributions)

        object_types = choices(self.config.object_classes, k=num_distributions)

        data = []

        # Send list of data to be sent down the pipeline
        for tx in self.transformers:
            obj = {
                "object_distribution": object_distribution,
                "time_distribution": time_distribution,
                "object_types": object_types,
                "transformers": tx,
                "num_videos": 1,
                "filename_prefix": self.name + "_" + tx.name
            }
            data.append(obj)

        return data

    @classmethod
    def create_from_config(cls, config: Config, data):
        return ExperimentFuzzer(config, data)

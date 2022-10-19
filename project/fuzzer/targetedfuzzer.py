import copy
import logging

from component_generator.transformergenerator import TransformerGenerator
from config.config import Config
from distribution_generator.dgfactory import DGFactory
from fuzzer.fuzzer import Fuzzer
from utility.timer import timer


class TargetedFuzzer(Fuzzer):

    def __init__(self, config: Config, data=None):
        super().__init__(config, data)
        self.name = "targeted_fuzzer"

    @timer
    def apply(self, data):
        # Send list of data to be sent down the pipeline
        new_data = []

        transformer_generator = TransformerGenerator(self.config)
        self.transformers = transformer_generator.process(self.config.data.get("transformers", []))

        # distribute remaining cores between transformers
        # TODO: Add remaining cores
        quotient_cores = int(self.config.max_cores / self.config.video_copies)
        quotient_cores = 1 if quotient_cores < 0 else quotient_cores

        self.config.pipeline_cores = min(self.config.max_cores, self.config.video_copies)

        for i in range(self.config.video_copies):

            _data = copy.deepcopy(data)

            local_transforms = {
                "applied": False,
                "transformers": self.transformers,
                "type": "local"
            }

            obj = {
                "object_distribution": DGFactory.get_distribution_generator(self.config.object_distribution),
                "time_distribution": DGFactory.get_distribution_generator(self.config.time_distribution),
                "object_type_distribution": DGFactory.get_distribution_generator(self.config.object_class_distribution),
                "filename": self.config.filename + "_" + str(i),
                "max_tx_cores": quotient_cores,
                "compositor": self.config.data["compositor"]
            }

            logging.debug(f"Setting max tx cores as {quotient_cores}")

            new_obj = {**_data, **obj, "transformers": [local_transforms]}
            new_data.append(new_obj)

        return new_data

    def validate(self, data):
        pass

    @classmethod
    def create_from_config(cls, config: Config, data):
        return TargetedFuzzer(config, data)

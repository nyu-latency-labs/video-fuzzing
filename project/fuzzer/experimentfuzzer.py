import copy

from config.config import Config
from fuzzer.fuzzer import Fuzzer
from utils.timer import timer


class ExperimentFuzzer(Fuzzer):

    def __init__(self, config: Config, data=None):
        super().__init__(config, data)
        self.name = "experiment_fuzzer"

    @timer
    def apply(self, data):
        # Send list of data to be sent down the pipeline
        new_data = []

        # distribute remaining cores between transformers
        quotient_cores = int(self.config.max_cores / (self.config.video_copies * len(self.transformers)))
        quotient_cores = 1 if quotient_cores < 0 else quotient_cores
        remainder_cores = self.config.max_cores % (self.config.video_copies * len(self.transformers))

        for tx in self.transformers:
            _data = copy.deepcopy(data)
            local_transforms = {
                "applied": False,
                "transformers": [tx],
                "type": "local"
            }
            obj = {
                "object_distribution": self.config.object_distribution,
                "time_distribution": self.config.time_distribution,
                "object_type_distribution": self.config.object_class_distribution,
                "num_videos": self.config.video_copies,
                "filename_prefix": self.name + "_" + str(tx),
                "max_tx_cores": quotient_cores + (1 if remainder_cores > 0 else 0)
            }
            remainder_cores -= 1

            new_obj = {**_data, **obj}
            new_obj["transformers"].append(local_transforms)

            new_data.append(new_obj)

        return new_data

    def validate(self, data):
        pass

    @classmethod
    def create_from_config(cls, config: Config, data):
        return ExperimentFuzzer(config, data)

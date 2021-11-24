import copy

from Config.Config import Config
from Fuzzer.Fuzzer import Fuzzer
from Utils.Timer import timer


class ExperimentFuzzer(Fuzzer):

    def __init__(self, config: Config, data=None):
        super().__init__(config, data)
        self.name = "experiment_fuzzer"

    @timer
    def apply(self, data):
        # Send list of data to be sent down the pipeline
        new_data = []
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
                "num_videos": self.data["num_videos"],
                "filename_prefix": self.name + "_" + str(tx),
            }

            new_obj = {**_data, **obj}
            new_obj["transformers"].append(local_transforms)

            new_data.append(new_obj)

        return new_data

    @classmethod
    def create_from_config(cls, config: Config, data):
        return ExperimentFuzzer(config, data)

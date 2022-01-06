import json
import multiprocessing

from DistributionGenerator.DGFactory import DGFactory
from Utils.XY import XY


class Config:
    data = None

    # Fetch required properties and dump rest to a dictionary

    def __init__(self, filename):
        with open(filename) as f:
            self.data = json.load(f)

        object_class_distribution = {
            "type": "choice",
            "value": self.data["object_class"]
        }

        self.duration = int(self.data["duration"])
        self.fps = int(self.data["fps"])
        self.step_size = int(self.data["step_size"])
        self.steps = self.duration / self.step_size
        self.media_root = self.data["media_root"]
        self.frame_size = XY(self.data["dimension"]["x"], self.data["dimension"]["y"])
        self.max_tx_cores = min(self.data["max_tx_cores"], multiprocessing.cpu_count())
        max_total_cores = min(self.data["max_cores"], multiprocessing.cpu_count())
        self.max_cores = int(max_total_cores / self.max_tx_cores)
        self.use_cache = self.data["use_cache"]

        self.object_class_distribution = object_class_distribution
        self.object_distribution = self.data["object_distribution"]
        self.time_distribution = self.data["time_distribution"]

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['object_distribution']
        del state['time_distribution']
        del state['object_class_distribution']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

        # retrieve the excluded method/methods
        self.object_distribution = DGFactory.get_distribution_generator(self.data["object_distribution"])
        self.time_distribution = DGFactory.get_distribution_generator(self.data["time_distribution"])

        object_class_distribution = {
            "type": "choice",
            "value": self.data["object_class"]
        }
        self.object_class_distribution = DGFactory.get_distribution_generator(object_class_distribution)

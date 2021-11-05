import json
from random import gauss
import multiprocessing

from Utils.XY import XY


def process_distribution(ds):
    ds_type = ds["type"]

    if ds_type == "normal":
        return lambda: gauss(ds["mean"], ds["std"])
    elif ds_type == "linear":
        return lambda: ds["value"]


class Config:
    data = None

    # Fetch required properties and dump rest to a dictionary

    def __init__(self, filename):
        with open(filename) as f:
            self.data = json.load(f)

        self.object_classes = self.data["object_class"]
        self.object_distribution_fn = process_distribution(self.data["object_distribution"])
        self.time_distribution_fn = process_distribution(self.data["time_distribution"])

        self.duration = int(self.data["duration"])
        self.fps = int(self.data["fps"])
        self.step_size = int(self.data["step_size"])
        self.steps = self.duration / self.step_size
        self.media_root = self.data["media_root"]
        self.frame_size = XY(self.data["dimension"]["x"], self.data["dimension"]["y"])
        self.max_cores = min(self.data["max_cores"], multiprocessing.cpu_count())


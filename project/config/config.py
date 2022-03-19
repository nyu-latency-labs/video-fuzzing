import json
import multiprocessing

from utils.pair import Pair
from pathlib import Path


class Config:
    data: dict = None

    # Fetch required properties and dump rest to a dictionary
    def __init__(self, filename):
        with open(filename) as f:
            self.data = json.load(f)

        self.validate()

        object_class_distribution = {
            "type": "choice",
            "value": self.data.get("object_class", None)
        }

        self.filename: str = str(Path(filename).with_suffix(''))
        self.duration: int = int(self.data["duration"])
        self.fps: int = int(self.data["fps"])
        self.step_size: int = int(self.data["step_size"])
        self.steps: int = int(self.duration / self.step_size)
        self.video_copies: int = self.data["num_video_copies"]
        self.media_root: str = self.data["media_root"]
        self.frame_size: Pair = Pair(self.data["dimension"]["x"], self.data["dimension"]["y"])
        self.max_cores: int = min(self.data["max_cores"], multiprocessing.cpu_count())
        self.pipeline_cores = self.max_cores
        self.use_cache: bool = self.data["use_cache"]

        self.object_class_distribution = object_class_distribution
        self.object_distribution = self.data.get("object_distribution", None)
        self.time_distribution = self.data.get("time_distribution", None)

    def validate(self):
        params = {"duration", "fps", "media_root", "max_cores", "use_cache", "step_size", "dimension", "num_video_copies"}

        if not params <= self.data.keys():
            raise AssertionError(f"Required params missing from config file. Required params are: {params}")

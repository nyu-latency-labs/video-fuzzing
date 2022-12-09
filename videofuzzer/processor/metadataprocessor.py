import json
import logging
import os

from ..config.config import Config
from ..processor.processor import Processor
from ..utility.timer import timer


class MetadataProcessor(Processor):

    def __init__(self, config: Config):
        super().__init__(config)
        self.name = "metadata_processor"

    @timer
    def apply(self, data: dict) -> dict:
        self.validate(data)

        data["metadata"] = [[] for i in range(self.config.duration*self.config.fps)]

        for clip in data["clips"]:
            for t in range(clip.start, clip.end):
                for i in range(self.config.fps):
                    data["metadata"][t*self.config.fps + i].append(clip.object_type)

        output_json = {"object_distribution": data["metadata"]}

        os.makedirs("media/", exist_ok=True)
        with open("media/" + data["filename"] + "_metadata.json", 'w') as f:
            json.dump(output_json, f)

        logging.debug(f"Saving metadata for video as {data['filename'] + '.json'}")
        return data

    def validate(self, data):
        if "clips" not in data or not data["clips"]:
            raise AssertionError("Clip list empty. Cannot transform")

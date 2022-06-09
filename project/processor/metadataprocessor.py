import json
import logging
import os

from config.config import Config
from processor.processor import Processor
from utils.timer import timer


class MetadataProcessor(Processor):

    def __init__(self, config: Config):
        super().__init__(config)
        self.name = "metadata_processor"

    @timer
    def apply(self, data: dict) -> dict:
        self.validate(data)

        data["objects"] = [[] for i in range(self.config.duration)]

        for clip in data["clips"]:
            for i in range(clip.start, clip.end):
                data["objects"][i].append(clip.object_type)

        output_json = {"object_distribution": data["objects"]}

        os.makedirs("metadata/", exist_ok=True)
        with open("metadata/" + data["filename"] + ".json", 'w') as f:
            json.dump(output_json, f)

        logging.debug(f"Saving metadata for video as {data['filename'] + '.json'}")
        return data

    def validate(self, data):
        if "clips" not in data or not data["clips"]:
            raise AssertionError("Clip list empty. Cannot transform")

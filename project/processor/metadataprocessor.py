import json
import logging

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

        data["objects"] = [[] for i in range(self.config.duration + 1)]

        for clip in data["clips"]:
            for i in range(clip.start, clip.end + 1):
                data["objects"][i].append(clip.object_type)

        output_json = {"object_distribution": data["objects"]}

        with open(data["filename"] + ".json", 'w') as f:
            json.dump(output_json, f)

        logging.debug(f"Saving metadata for video as {data['filename'] + '.json'}")
        return data

    def validate(self, data):
        if "clips" not in data or not data["clips"]:
            raise AssertionError("Clip list empty. Cannot transform")

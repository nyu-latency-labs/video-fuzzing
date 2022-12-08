import logging
import os
from random import choice
from typing import Tuple, List, Dict

from utility.singleton import Singleton
from video_generator.video import Video

VIDEO_ROOT = "../resources"
JSON_PATH = "config.json"


def discover_media(root: str) -> Tuple[List[str], Dict[str, List[Video]]]:
    all_media = {}
    obj_types = []
    for dirs in os.listdir(root):
        if os.path.isdir(os.path.join(root, dirs)):
            dir_path = os.path.join(root, dirs)
            obj_types.append(dirs)
            media = []
            for files in os.listdir(dir_path):
                file_path = os.path.join(dir_path, files)
                # TODO: Merge if it works
                if os.path.isfile(file_path) and files.endswith("jpg"):
                    media.append(Video(file_path, dirs))
                if os.path.isfile(file_path) and files.endswith("mp4"):
                    media.append(Video(file_path, dirs))

            all_media[dirs] = media

    logging.info("Found videos of object_type: %s", obj_types)
    return obj_types, all_media


class VideoGenerator(metaclass=Singleton):
    root: str = VIDEO_ROOT
    videos: Dict[str, List[Video]] = None
    object_types: List[str] = None

    def __init__(self, root: str):
        self.root = root
        self.object_types, self.videos = discover_media(self.root)

    def get(self, object_type: str, duration: int, start_time: int) -> Video:
        logging.debug("Generating video of type: %s with start time: %s and duration: %s",
                      object_type, start_time, duration)

        if object_type not in self.object_types:
            raise AssertionError("Object type not found in media root.")

        candidate = choice(self.videos[object_type]).copy()
        candidate.set_start(start_time)
        candidate.set_duration(duration)
        candidate.set_end(start_time + duration)

        logging.debug("Generated video with start time: %s and duration: %s", candidate.start, candidate.duration)
        return candidate

    def get_object_types(self):
        return self.object_types

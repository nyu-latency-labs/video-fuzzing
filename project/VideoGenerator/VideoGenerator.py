import os
import logging
from random import choice

from moviepy.video.VideoClip import ImageClip, VideoClip


VIDEO_ROOT = "../resources"
JSON_PATH = "config.json"


def discover_media(root):
    all_media = {}
    obj_types = []
    for dirs in os.listdir(root):
        if os.path.isdir(os.path.join(root, dirs)):
            dir_path = os.path.join(root, dirs)
            obj_types.append(dirs)
            media = []
            for files in os.listdir(dir_path):
                file_path = os.path.join(dir_path, files)
                if os.path.isfile(file_path) and files.endswith("jpg"):
                    media.append(ImageClip(file_path))
                if os.path.isfile(file_path) and files.endswith("mp4"):
                    media.append(VideoClip(file_path))

            all_media[dirs] = media

    logging.info("Found videos of object_type: %s", obj_types)
    return obj_types, all_media


class VideoGenerator:
    root = VIDEO_ROOT
    videos = None
    object_types = None

    def __init__(self, root):
        self.root = root
        self.object_types, self.videos = discover_media(self.root)

    def get_video(self, object_type, duration, start_time):
        logging.debug("Generating video of type: %s with start time: %s and duration: %s",
                      object_type, start_time, duration)
        if object_type not in self.object_types:
            return None

        candidate = choice(self.videos[object_type]).copy()
        candidate = candidate.set_duration(duration).set_start(start_time)

        logging.debug("Generated video with start time: %s and duration: %s", candidate.start, candidate.duration)
        return candidate

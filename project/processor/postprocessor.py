import uuid
import os

from moviepy.video.VideoClip import VideoClip

from config.config import Config
from processor.processor import Processor
from utility.timer import timer


class PostProcessor(Processor):

    def __init__(self, config: Config):
        super().__init__(config)
        self.name = "post_processor"

    @timer
    def apply(self, data) -> dict:
        video = data["composite_video"]
        filename = data["filename"]

        video = video.set_duration(self.config.duration)
        video = video.set_fps(self.config.fps)
        video = video.without_audio()

        if filename is None:
            filename = uuid.uuid4()

        os.makedirs("media/", exist_ok=True)
        video_path = "media/" + filename + ".mp4"
        video.write_videofile(video_path, self.config.fps, "mpeg4", audio=False)
        data["status"] = True

        data["video_path"] = video_path

        return data

    def validate(self, data):
        raise NotImplementedError("Validate method not implemented.")

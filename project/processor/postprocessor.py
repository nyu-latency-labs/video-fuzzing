import uuid

from moviepy.video.VideoClip import VideoClip

from config.config import Config
from processor.processor import Processor
from utils.timer import timer


class PostProcessor(Processor):

    def __init__(self, config: Config):
        super().__init__(config)
        self.name = "post_processor"

    @timer
    def apply(self, data) -> VideoClip:
        video = data["composite_video"]
        filename = data["filename"]

        video = video.set_duration(self.config.duration)
        video = video.set_fps(self.config.fps)
        video = video.without_audio()

        if filename is None:
            filename = uuid.uuid4()

        video.write_videofile(filename + ".mp4", self.config.fps, "mpeg4", audio=False, bitrate="1000k")
        data["status"] = True
        return video

    def validate(self, data):
        raise NotImplementedError("Validate method not implemented.")

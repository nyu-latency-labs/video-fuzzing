import uuid

from moviepy.video.VideoClip import VideoClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip

from Config.Config import Config
from Pipeline.PipelineUnit import PipelineUnit
from Pipeline.Utils import timer


class PostProcessor(PipelineUnit):

    def __init__(self, config: Config):
        self.config = config

    @timer(name="PostProcessor")
    def apply(self, data) -> VideoClip:
        video = data["video"]
        filename = data["filename"]

        video = video.set_duration(self.config.duration)
        video = video.set_fps(self.config.fps)
        video = video.without_audio()

        if filename is None:
            filename = uuid.uuid4()

        video.write_videofile(filename, self.config.fps, "mpeg4", audio=False, bitrate="1000k")
        return video

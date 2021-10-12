from moviepy.video.VideoClip import ImageClip

from Config.Config import Config
from Pipeline.PipelineUnit import PipelineUnit


class Compositor(PipelineUnit):
    bg = None
    clips = []

    def __init__(self, config: Config):
        self.config = config

    def apply(self, data):
        return ImageClip(self.config.data["background_path"])

    @classmethod
    def create_from_config(cls, config: Config):
        return Compositor(config)

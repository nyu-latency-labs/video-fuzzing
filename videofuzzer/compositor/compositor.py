from moviepy.video.VideoClip import VideoClip

from ..config.config import Config
from ..pipeline.pipelineunit import PipelineUnit
from moviepy.video.fx.resize import resize

from ..utility.pair import Pair


class Compositor(PipelineUnit):
    bg = None
    clips = []

    def __init__(self, config: Config):
        self.config = config
        self.name = "compositor"

    def apply(self, data: dict) -> dict:
        raise NotImplementedError("Apply method not implemented.")

    def validate(self, data):
        raise NotImplementedError("Validate method not implemented.")

    @classmethod
    def create_from_config(cls, config: Config):
        return Compositor(config)

    def resize_clip(self, clip: VideoClip, size: Pair):
        x, y = clip.size
        if x/size.first > y/size.second:
            return resize(clip, width=size.first)
        return resize(clip, height=size.second)

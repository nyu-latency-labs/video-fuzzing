from Config.Config import Config
from Transformer.Transformer import Transformer
from moviepy.editor import VideoClip


class RotateTransformer(Transformer):
    angle = 0

    def __init__(self, config: Config, angle):
        super().__init__(config)
        self.name = "rotate_transformer"
        self.angle = angle

    def apply(self, clip) -> VideoClip:
        return clip.rotate(self.angle)

    @classmethod
    def create_from_config(cls, config, data):
        return RotateTransformer(config, data["angle"])

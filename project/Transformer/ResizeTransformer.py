from enum import Enum

from Config.Config import Config
from Transformer.Transformer import Transformer
from moviepy.editor import VideoClip

from Config.XY import XY

DEFAULT_DIMENSION = (100, 100)
DEFAULT_RATIO = 1


class ResizeType(Enum):
    DIMENSION = 1
    RATIO = 2
    WIDTH = 3
    HEIGHT = 4


class ResizeTransformer(Transformer):
    dimensions = None
    type = None

    def __init__(self, config: Config, dim: XY = None, ratio=None, width=None, height=None):
        super().__init__(config)
        self.name = "resize_transformer"

        if dim is not None:
            if dim.x < 0 or dim.y < 0:
                raise AssertionError("Dimension should be greater than 0")
            self.dimensions = dim
            self.type = ResizeType.DIMENSION
        elif ratio is not None:
            if ratio < 0:
                raise AssertionError("Ratio should be greater than 0")
            self.ratio = ratio
            self.type = ResizeType.RATIO
        elif width is not None:
            if width < 0:
                raise AssertionError("Width should be greater than 0")
            self.width = width
            self.type = ResizeType.WIDTH
        elif height is not None:
            if height < 0:
                raise AssertionError("Height should be greater than 0")
            self.height = height
            self.type = ResizeType.HEIGHT

    def apply(self, clip) -> VideoClip:
        if self.type == ResizeType.DIMENSION:
            new_data = clip.resize(self.dimensions.x, self.dimensions.y)
        elif self.type == ResizeType.RATIO:
            new_data = clip.resize(self.ratio)
        elif self.type == ResizeType.WIDTH:
            new_data = clip.resize(width=self.width)
        elif self.type == ResizeType.HEIGHT:
            new_data = clip.resize(height=self.height)

        return new_data

    @classmethod
    def create_from_config(cls, config: Config, data):
        dim = None
        ratio = None
        width = None
        height = None

        if "dimension" in data:
            dim = XY(data["dimension"]["x"], data["dimension"]["x"])
        elif "ratio" in data:
            ratio = data["ratio"]
        elif "width" in data:
            width = data["width"]
        elif "height" in data:
            height = data["height"]

        return ResizeTransformer(config, dim, ratio, width, height)
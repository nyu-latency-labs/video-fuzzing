import random
from enum import Enum

from moviepy.editor import VideoClip
from moviepy.video.fx.resize import resize

from transformer.transformer import Transformer
from utils.timer import timer
from utils.pair import Pair

DEFAULT_DIMENSION = (100, 100)
DEFAULT_RATIO = 1


class ResizeType(Enum):
    DIMENSION = 1
    RATIO = 2
    WIDTH = 3
    HEIGHT = 4


class ResizeTransformer(Transformer):
    """
    This transformer resizes the clip by the specified parameter during construction.
    This can be of the following types:-
    - Dimensions
    - Ratio
    - Width (ratio maintained)
    - Height (ratio maintained)
    """

    def __init__(self, **kwargs):
        super().__init__()
        self.name = "resize_transformer"

        self.validate(**kwargs)

        if "dim" in kwargs:
            self.dimensions = kwargs["dim"]
            self.type = ResizeType.DIMENSION
        elif "ratio" in kwargs:
            self.ratio = kwargs["ratio"]
            self.type = ResizeType.RATIO
        elif "width" in kwargs:
            self.width = kwargs["width"]
            self.type = ResizeType.WIDTH
        elif "height" in kwargs:
            self.height = kwargs["height"]
            self.type = ResizeType.HEIGHT

    def __str__(self):
        to_str = self.name + "_"

        if self.type == ResizeType.DIMENSION:
            to_str += "x_" + str(self.dimensions.first) + "_y_" + str(self.dimensions.second)
        elif self.type == ResizeType.RATIO:
            to_str += "ratio_" + str(self.ratio)
        elif self.type == ResizeType.WIDTH:
            to_str += "width_" + str(self.width)
        elif self.type == ResizeType.HEIGHT:
            to_str += "height_" + str(self.height)

        to_str += "_"
        return to_str

    @timer
    def apply(self, clip: VideoClip) -> VideoClip:
        if self.type == ResizeType.DIMENSION:
            return resize(clip, newsize=self.dimensions.get())
        elif self.type == ResizeType.RATIO:
            return resize(clip, newsize=self.ratio)
        elif self.type == ResizeType.WIDTH:
            return resize(clip, width=self.width)
        elif self.type == ResizeType.HEIGHT:
            return resize(clip, height=self.height)

    def validate(self, **kwargs):
        if "dim" in kwargs:
            if kwargs["dim"].first < 0 or kwargs["dim"].second < 0:
                raise AssertionError("Dimension should be greater than 0")
        elif "ratio" in kwargs:
            if kwargs["ratio"] < 0:
                raise AssertionError("Ratio should be greater than 0")
        elif "width" in kwargs:
            if kwargs["width"] < 0:
                raise AssertionError("Width should be greater than 0")
        elif "height" in kwargs:
            if kwargs["height"] < 0:
                raise AssertionError("Height should be greater than 0")

    @classmethod
    def create_from_config(cls, data):
        values = {}
        if "dimension" in data:
            values["dim"] = Pair(data["dimension"]["x"], data["dimension"]["x"])
        elif "ratio" in data:
            values["ratio"] = data["ratio"]
        elif "width" in data:
            values["width"] = data["width"]
        elif "height" in data:
            values["height"] = data["height"]

        return ResizeTransformer(**values)

    @classmethod
    def get_random(cls):
        ratio = random.randint(1, 200) / 100
        data = {"type": "resize_transformer", "ratio": ratio}
        return data

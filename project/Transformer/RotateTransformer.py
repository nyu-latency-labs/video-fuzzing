from moviepy.video.VideoClip import ImageClip

from Utils.Timer import timer
from Transformer.Transformer import Transformer

import numpy as np


class RotateTransformer(Transformer):
    angle = 0

    def __init__(self, angle):
        super().__init__()
        self.name = "rotate_transformer"
        self.angle = angle

    def __str__(self):
        return self.name + ":" + "angle=" + str(self.name) + ";"

    @timer
    def apply(self, clip):
        # clip = data["clip"]
        if type(clip) == ImageClip:
            new_data = rotate(clip, self.angle)
        else:
            new_data = clip.rotate(self.angle)

        # data["clip"] = new_data
        return new_data

    @classmethod
    def create_from_config(cls, data):
        return RotateTransformer(data["angle"])


try:
    from PIL import Image

    PIL_FOUND = True


    def pil_rotater(pic, angle, resample, expand):
        return np.array(Image.fromarray(pic).rotate(angle, expand=expand,
                                                    resample=resample))
except ImportError:
    PIL_FOUND = False


# Copy pasted from fx.rotate, just apply directly to ImageClip
def rotate(clip, angle, unit='deg', resample="bicubic", expand=True):
    resample = {"bilinear": Image.BILINEAR,
                "nearest": Image.NEAREST,
                "bicubic": Image.BICUBIC}[resample]

    transpose = [1, 0] if clip.ismask else [1, 0, 2]

    def fl(im, a):
        if unit == 'rad':
            a = 360.0 * a / (2 * np.pi)

        if (a == 90) and expand:
            return np.transpose(im, axes=transpose)[::-1]
        elif (a == -90) and expand:
            return np.transpose(im, axes=transpose)[:, ::-1]
        elif (a in [180, -180]) and expand:
            return im[::-1, ::-1]
        elif not PIL_FOUND:
            raise ValueError('Without "Pillow" installed, only angles 90, -90,'
                             '180 are supported, please install "Pillow" with'
                             "pip install pillow")
        else:
            return pil_rotater(im, a, resample=resample, expand=expand)

    arr = fl(clip.get_frame(0), angle)
    clip.size = arr.shape[:2][::-1]
    clip.make_frame = lambda t: arr
    clip.img = arr
    return clip

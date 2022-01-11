import copy
from typing import Union

from moviepy.Clip import Clip
from moviepy.video.VideoClip import ImageClip, VideoClip
from moviepy.video.fx.crop import crop
from moviepy.video.fx.resize import resize
from moviepy.video.io.VideoFileClip import VideoFileClip

from utils.pair import Pair


class Video:
    start = 0
    end = None
    position = None
    duration = None  # Set default to prevent possible ffmpeg error
    size = None
    crop_lambda = None
    crop_x1 = None
    crop_x2 = None

    def __init__(self, filepath):
        self.filepath = filepath

    def set_start(self, start):
        self.start = start

    def set_end(self, end):
        self.end = end

    def set_duration(self, duration):
        self.duration = duration

    def resize(self, size: Pair):
        self.size = size

    # TODO: Fix for multiple crops
    def crop(self, position: Pair, size: Pair):
        self.crop_x1 = position
        self.crop_x2 = Pair(position.first + size.first, position.second + size.second)
        self.crop_lambda = True

    def get(self) -> Union[VideoClip, ImageClip]:
        if self.filepath.endswith("jpg"):
            clip = ImageClip(self.filepath)
        else:
            clip = VideoFileClip(self.filepath)

        if self.size is not None:
            clip = resize(clip, self.size.get())
        if self.crop_lambda:
            clip = crop(clip, x1=self.crop_x1.first, y1=self.crop_x1.second, x2=self.crop_x2.first, y2=self.crop_x2.second)
        if self.position is not None:
            clip = clip.set_position(self.position.get())

        if self.duration is None and self.end is None:
            # Setting duration to 0 possibly causes errors with ffmpeg
            self.duration = 1
            self.end = 1
        elif self.duration is None:
            self.duration = self.end - self.start
        elif self.end is None:
            self.end = self.start + self.duration

        clip = clip.set_start(self.start).set_duration(self.duration).set_end(self.end)
        self.clear_ops()

        return clip

    # Clear resizing etc once clip has been transformed
    def clear_ops(self):
        self.size = None
        self.crop_lambda = False
        self.crop_x2 = None
        self.crop_x1 = None

    def copy(self):
        return copy.copy(self)

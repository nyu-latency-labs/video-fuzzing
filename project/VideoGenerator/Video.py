import copy
from moviepy.video.VideoClip import ImageClip, VideoClip
from moviepy.video.fx.crop import crop
from moviepy.video.fx.resize import resize
from moviepy.video.io.VideoFileClip import VideoFileClip

from Config.XY import XY


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

    def resize(self, size: XY):
        self.size = size

    # TODO: Fix for multiple crops
    def crop(self, position: XY, size: XY):
        self.crop_x1 = position
        self.crop_x2 = XY(position.x+size.X, position.y+size.y)
        self.crop_lambda = True
        # self.crop_lambda = lambda clip: crop(clip, x1=position.x, y1=position.y, x2=position.x+size.x,
        #                                      y2=position.y+size.y)

    def get_video(self):
        clip = None
        if self.filepath.endswith("jpg"):
            clip = ImageClip(self.filepath)
        else:
            clip = VideoFileClip(self.filepath)

        if self.size is not None:
            clip = resize(clip, self.size.get_xy())
        if self.crop_lambda:
            clip = crop(clip, x1=self.crop_x1.x, y1=self.crop_x1.y, x2=self.crop_x2.x, y2=self.crop_x2.y)
        if self.position is not None:
            clip = clip.set_position(self.position.get_xy())

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

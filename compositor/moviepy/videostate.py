from moviepy.video.VideoClip import ImageClip

from props import Props
from moviepy.editor import VideoFileClip
from xy import XY
import random
from moviepy.video.fx.crop import crop
import math

min_size = XY(46, 46)


class VideoState:
    offset = 0
    original_size = None
    original_clip = None
    duration_played = 0
    duration_step = 0
    frame_size = None
    category = None

    # remove non original clips
    def __init__(self, location, offset, prop: Props, category):
        self.offset = offset
        self.category = category
        self.duration_played = offset
        self.duration_step = prop.duration_step
        self.original_clip = ImageClip(location).set_fps(prop.fps)
        self.original_size = XY.from_tuple(self.original_clip.size)
        self.frame_size = prop.dim

    def resize(self, clip, new_size):
        xsize, ysize = clip.size
        scale = min(new_size.x/xsize, new_size.y/ysize)

        size = (scale*xsize, scale*ysize)
        clip = clip.resize(size)
        return clip

    # 0 indexed
    def generate_clip(self, idx, nrow, ncol):
        row = math.floor(idx/ncol)
        col = idx % nrow

        # Resize
        nsize = XY(self.frame_size.x/ncol, self.frame_size.y/nrow)
        clip = self.resize(self.original_clip, nsize)

        # Reposition
        pos = (nsize.x*col, nsize.y*row)
        # print("setting position: " + str(pos) + " with size: " + str(nsize) + " for vid type " + self.category + "given " + str(nrow) + "," + str(ncol) + " idx " + str(idx))
        return clip.set_position(pos)

    def get_next_step_clip(self, start_time, clip):
        clip = clip.set_start(start_time).set_end(start_time + self.duration_step)
        # print("creating clip for type:" + self.category + " with start time: " + str(start_time))
        return clip
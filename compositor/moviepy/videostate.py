from props import Props
from moviepy.editor import VideoFileClip
from xy import XY
import random
from moviepy.video.fx.crop import crop
import math
min_size = XY(50, 50)

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
        self.original_clip = VideoFileClip(location, audio=False).set_fps(30)
        self.original_size = XY.fromTuple(self.original_clip.size)
        self.frame_size = prop.dim

    def getNextStepClip(self, start_time, clip):
        clip = clip.subclip(self.duration_played, self.duration_played + self.duration_step).set_start(start_time) \
            .set_end(start_time+self.duration_step)
        self.duration_played += self.duration_step

        if (self.duration_played + self.duration_step > self.original_clip.duration):
            self.duration_played = 0
        return clip

    # try distribution of video size as a function of frame size
    def resizeAndCropVideo(self, clip):
        # Decide on video size
        # print("clip size ", str(clip.size))
        # print("frame size ", self.frame_size)
        new_size = XY(random.randrange(min_size.x, min(clip.size[0], self.frame_size.x)), random.randrange(min_size.y, min(clip.size[1], self.frame_size.y)))
        # print("new size ", new_size)

        # Resize- get ratio btn 2x frame size and newsize
        ratio_max_x = 2*self.frame_size.x/clip.size[0]
        ratio_min_x = new_size.x/clip.size[0]
        ratio_max_y = 2*self.frame_size.y/clip.size[1]
        ratio_min_y = new_size.y/clip.size[1]
        # print(ratio_max_x, ratio_max_y, ratio_min_x, ratio_min_y)

        ratio_max = ratio_max_x if ratio_max_x < ratio_max_y else ratio_max_y
        ratio_min = ratio_min_x if ratio_min_x > ratio_min_y else ratio_min_y
        # print(ratio_min, ratio_max)
        
        # Resize by aspect ratio only
        resize_ratio = random.randrange(math.ceil(100*ratio_min), math.floor(100*ratio_max))/100
        # print(resize_ratio)
        final_size = XY(int(clip.size[0]*resize_ratio), int(clip.size[1]*resize_ratio))
        clip = clip.resize(final_size.getXY())

        # Crop
        # print(final_size, new_size)
        pos_x = 0 if final_size.x == new_size.x else random.randrange(0, final_size.x-new_size.x)
        pos_y = 0 if final_size.y == new_size.y else random.randrange(0, final_size.y-new_size.y)

        crop_xy = XY(pos_x, pos_y)
        clip = crop(clip, x1=crop_xy.x, x2=crop_xy.x+new_size.x, y1=crop_xy.y, y2=crop_xy.y+new_size.y)

        return clip

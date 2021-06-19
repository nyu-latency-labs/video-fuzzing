from moviepy.editor import VideoFileClip
from xy import XY
import random
from moviepy.video.fx.crop import crop

min_size = XY(50, 50)

class VideoState:
    location = "../resources/cars/1.mp4"
    offset = 0
    dim = None
    pos = None
    original_size = None
    original_clip = None
    duration_played = 0
    duration_step = 0
    clip = None
    original_duration = 0
    frame_size = None

    # remove non original clips
    def __init__(self, location, offset, pos: XY, dim: XY, duration_step, frame_size: XY):
        self.location = location
        self.offset = offset
        self.pos = pos
        self.dim = dim
        self.duration_played = offset
        self.duration_step = duration_step
        self.original_clip = VideoFileClip(self.location)
        self.original_size = XY.fromTuple(self.original_clip.size)
        self.clip = self.original_clip.copy().resize(dim.getXY()).set_position(pos.getXY())
        self.original_duration = self.original_duration
        self.frame_size = frame_size

    def getNextStepClip(self, start_time):
        clip = self.clip.subclip(self.duration_played, self.duration_played + self.duration_step).set_start(start_time) \
            .set_end(start_time+self.duration_step)
        self.duration_played += 2
        if (self.duration_played + 2 > self.original_duration):
            self.duration_played = 0
        return clip

    # try distribution of video size
    def resizeAndCropVideo(self):
        # Decide on video size
        new_size = XY(random.randrange(min_size.x, self.frame_size.x), random.randrange(min_size.y, self.frame_size.y))
        # Resize- get ratio of btn 2x frame size and newsize
        ratio_max_x = 2*self.frame_size.x/self.original_size.x
        ratio_min_x = new_size.x/self.original_size.x
        ratio_max_y = 2*self.frame_size.y/self.original_size.y
        ratio_min_y = new_size.y/self.original_size.y
        print(new_size)
        resize_ratio = XY(random.randrange(int(100*ratio_min_x), int(100*ratio_max_x))/100, random.randrange(int(100*ratio_min_y), int(100*ratio_max_y))/100)
        print(resize_ratio)
        final_size = XY(int(self.original_size.x*resize_ratio.x), int(self.original_size.y*resize_ratio.y))
        print(final_size)
        print(self.original_size)
        clip = self.original_clip.resize(final_size.getXY())
        if (True):
            print("reached here")
        # Crop
        crop_xy = XY(random.randrange(0, final_size.x-new_size.x), random.randrange(0, final_size.y-new_size.y))
        print("reached here")
        print(crop_xy)
        clip = crop(clip, x1=crop_xy.x, x2=crop_xy.x+new_size.x, y1=crop_xy.y, y2=crop_xy.y+new_size.y)
        print("cropped clip")
        return clip
 
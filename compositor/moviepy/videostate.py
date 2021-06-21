from moviepy.editor import VideoFileClip
from xy import XY
import random
from moviepy.video.fx.crop import crop

min_size = XY(50, 50)

class VideoState:
    location = None
    offset = 0
    dim = None
    pos = None
    original_size = None
    original_clip = None
    duration_played = 0
    duration_step = 0
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
        self.original_duration = self.original_duration
        self.frame_size = frame_size

    def getNextStepClip(self, start_time, clip):
        clip = clip.subclip(self.duration_played, self.duration_played + self.duration_step).set_start(start_time) \
            .set_end(start_time+self.duration_step)
        self.duration_played += self.duration_step

        if (self.duration_played + self.duration_step > self.original_duration):
            self.duration_played = 0
        return clip

    # try distribution of video size as a function of frame size
    def resizeAndCropVideo(self, clip):
        # Decide on video size
        new_size = XY(random.randrange(min_size.x, self.frame_size.x), random.randrange(min_size.y, self.frame_size.y))
        
        # Resize- get ratio btn 2x frame size and newsize
        ratio_max_x = 2*self.frame_size.x/self.original_size.x
        ratio_min_x = new_size.x/self.original_size.x
        ratio_max_y = 2*self.frame_size.y/self.original_size.y
        ratio_min_y = new_size.y/self.original_size.y

        ratio_max = ratio_max_x if ratio_max_x > ratio_max_y else ratio_max_y
        ratio_min = ratio_min_x if ratio_min_x > ratio_min_y else ratio_min_y

        # Resize by aspect ratio only
        resize_ratio = random.randrange(int(100*ratio_min), int(100*ratio_max))/100
        final_size = XY(int(self.original_size.x*resize_ratio), int(self.original_size.y*resize_ratio))
        clip = clip.resize(final_size.getXY())

        # Crop
        crop_xy = XY(random.randrange(0, final_size.x-new_size.x), random.randrange(0, final_size.y-new_size.y))
        clip = crop(clip, x1=crop_xy.x, x2=crop_xy.x+new_size.x, y1=crop_xy.y, y2=crop_xy.y+new_size.y)

        return clip

    
 
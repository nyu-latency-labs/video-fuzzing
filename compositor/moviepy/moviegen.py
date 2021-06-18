# Import everything needed to edit video clips
from moviepy.editor import *
import random
import math

class XY:
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getXY(self):
        return (self.x, self.y)

class VideoState:
    location = "../resources/cars/1.mp4"
    offset = 0
    dim_x = 400
    dim_y = 200
    pos_x = 0
    pos_y = 0
    duration_played = 0
    duration_step = 0
    clip = None
    clip_duration = 0

    def __init__(self, location, offset, pos: XY, dim: XY, duration_step):
        self.location = location
        self.offset = offset
        self.pos = pos
        self.dim = dim
        self.duration_played = offset
        self.duration_step = duration_step
        self.clip = VideoFileClip(self.location).resize(dim.getXY()).set_position(pos.getXY())
        self.clip_duration = self.clip.duration

    def getNextStepClip(self, start_time):
        clip = self.clip.subclip(self.duration_played, self.duration_played + self.duration_step).set_start(start_time) \
            .set_end(start_time+self.duration_step)
        self.duration_played += 2
        if (self.duration_played + 2 > self.clip_duration):
            self.duration_played = 0
        return clip

class Props:
    duration = 10
    duration_step = 2
    grid = None
    dim = None
    grid_occupied = None
    size = None

    def __init__(self, duration, duration_step, grid: XY, dim: XY):
        self.duration = duration
        self.duration_step = duration_step
        self.grid = grid
        self.dim = dim
        self.grid_occupied = [ [False]*grid.y for i in range(grid.x)]
        self.size = XY(dim.x/grid.x, dim.y/grid.y)

    def allocatePosition(self):
        for i in range(self.grid.x):
            for j in range(self.grid.y):
                if ( not self.grid_occupied[i][j]):
                    self.grid_occupied[i][j] = True
                    return XY(i*self.size.x, j*self.size.y)
        return XY(-1,-1)

    def freePosition(self, pos: XY):
        self.grid_occupied[pos.x][pos.y] = False

    def getVideoSize(self):
        return XY(self.size.x, self.size.y)


props = Props(40, 2, XY(2, 2), XY(400, 200))
 
location1 = "../resources/cars/1.mp4"
location2 = "../resources/cars/3.mp4"   
location3 = "../resources/cars/4.mp4"
location4 = "../resources/cars/2.mov"

dim = props.getVideoSize()
videos = []

pos = props.allocatePosition()
videos.append(VideoState(location1, 0, pos, dim, props.duration_step))

pos = props.allocatePosition()
videos.append(VideoState(location2, 0, pos, dim, props.duration_step))

pos = props.allocatePosition()
videos.append(VideoState(location3, 0, pos, dim, props.duration_step))

pos = props.allocatePosition()
videos.append(VideoState(location4, 0, pos, dim, props.duration_step))

imageclip = ImageClip("../resources/street.jpg").resize(dim.getXY())

distribution = []
for i in range(20):
    distribution.append(random.triangular(0,4))

clips = []
clips.append(imageclip)

for i in range(20):
    for j in range(round(distribution[i])):
        clips.append(videos[j].getNextStepClip(i*2))

video = CompositeVideoClip(clips).set_audio(None).resize(dim.getXY())

video.set_duration(40).write_videofile("output.mp4",fps=25,bitrate="500k",audio_codec=None,codec="mpeg4")
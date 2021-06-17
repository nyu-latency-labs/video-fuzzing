# Import everything needed to edit video clips
from moviepy.editor import *

class VideoState:
    location = "../resources/cars/1.mp4"
    offset = 0
    dim_x = 400
    dim_y = 200
    pos_x = 0
    pos_y = 0
    duration_played = 0
    duration_step = 0

    def __init__(self, location, offset, pos_x, pos_y, dim_x, dim_y, duration_step):
        self.location = location
        self.offset = offset
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.dim_x = dim_x
        self.dim_y = dim_y
        self.duration_played = offset
        self.duration_step = duration_step

    def getNextStepClip(self, start_time):
        clip = VideoFileClip(self.location).resize((self.dim_x,self.dim_y)).set_position((self.pos_x, self.pos_y)) \
            .subclip(self.duration_played, self.duration_played + self.duration_step).set_start(start_time) \
            .set_end(start_time+self.duration_step)
        return clip

class Props:
    duration = 10
    duration_step = 2
    grid_x = 2
    grid_y = 2
    dim_x = 400
    dim_y = 200
    grid_occupied = None
    size_x = 200
    size_y = 100

    def __init__(self, duration, duration_step, grid_x, grid_y, dim_x, dim_y):
        self.duration = duration
        self.duration_step = duration_step
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.dim_x = dim_x
        self.dim_y = dim_y
        self.grid_occupied = [ [False]*grid_y for i in range(grid_x)]
        self.size_x = dim_x/grid_x
        self.size_y = dim_y/grid_y

    def allocatePosition(self):
        for i in range(self.grid_x):
            for j in range(self.grid_y):
                if ( not self.grid_occupied[i][j]):
                    self.grid_occupied[i][j] = True
                    return (i*self.size_x, j*self.size_y)
        return (-1,-1)

    def freePosition(self, pos_x, pos_y):
        self.grid_occupied[pos_x][pos_y] = False

    def getVideoSize(self):
        return (self.size_x, self.size_y)


props = Props(10, 2, 2, 2, 400, 200)
 
location1 = "../resources/cars/1.mp4"
location2 = "../resources/cars/3.mp4"   
location3 = "../resources/cars/4.mp4"
location4 = "../resources/cars/2.mov"

(dim_x, dim_y) = props.getVideoSize()

(pos_x, pos_y) = props.allocatePosition()
video1 = VideoState(location1, 0, pos_x, pos_y, dim_x, dim_y, props.duration_step)

(pos_x, pos_y) = props.allocatePosition()
video2 = VideoState(location2, 0, pos_x, pos_y, dim_x, dim_y, props.duration_step)

(pos_x, pos_y) = props.allocatePosition()
video3 = VideoState(location3, 0, pos_x, pos_y, dim_x, dim_y, props.duration_step)

(pos_x, pos_y) = props.allocatePosition()
video4 = VideoState(location4, 0, pos_x, pos_y, dim_x, dim_y, props.duration_step)

imageclip = ImageClip("../resources/street.jpg").resize((400,200))

video = CompositeVideoClip([imageclip, video1.getNextStepClip(0), video2.getNextStepClip(1), video3.getNextStepClip(4), 
video4.getNextStepClip(6)])

video.set_duration(10).write_videofile("output.mp4",fps=25,bitrate="500k",audio_codec=None,codec="mpeg4")
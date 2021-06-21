# Import everything needed to edit video clips
from moviepy.editor import *
import random
import math
from xy import XY
from videostate import VideoState
from props import Props
from movieclip import MovieClip

# class Object
#     obj_type = None

frame_size = XY(800, 400)
props = Props(40, 2, XY(2, 2), frame_size)
 
location1 = "../resources/cars/1.mp4"
location2 = "../resources/cars/3.mp4"   
location3 = "../resources/cars/4.mp4"
location4 = "../resources/cars/2.mov"

dim = props.getVideoSize()
videos = []

pos = props.allocatePosition()
videos.append(VideoState(location2, 0, pos, dim, props.duration_step, frame_size))

# pos = props.allocatePosition()
# videos.append(VideoState(location2, 0, pos, dim, props.duration_step))

# pos = props.allocatePosition()
# videos.append(VideoState(location3, 0, pos, dim, props.duration_step))

# pos = props.allocatePosition()
# videos.append(VideoState(location4, 0, pos, dim, props.duration_step))

imageclip = ImageClip("../resources/street.jpg").resize(frame_size.getXY())

# def getClipsByDistribution(videos, duration, duration_step, )

# distribution = []
# for i in range(20):
#     distribution.append(random.triangular(0,4))

clips = []
clips.append(imageclip)

# for i in range(20):
#     for j in range(round(distribution[i])):
#         clips.append(videos[j].getNextStepClip(i*2))

movieClip = MovieClip.getNewClipInstance(videos[0])
clip = movieClip.getClipAt(0)
clips.append(clip)
video = CompositeVideoClip(clips).set_audio(None)

video.set_duration(40).write_videofile("output.mp4",fps=25,bitrate="1000k",audio_codec=None,codec="mpeg4")
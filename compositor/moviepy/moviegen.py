# Import everything needed to edit video clips
from moviepy.editor import *
from xy import XY
from videostate import VideoState
from props import Props
from movieclip import MovieClip
import random
import datetime

# class Object
#     obj_type = None

frame_size = XY(800, 400)
props = Props(40, 2, XY(2, 2), frame_size)
 
# location1 = "../resources/cars/1.mp4"
# location2 = "../resources/cars/3.mp4"   
# location3 = "../resources/cars/4.mp4"
# location4 = "../resources/cars/2.mov"

# Scan for objects and create VideoState instances
videoRoot = "../resources/cars/"
videoPaths = {}
rawVideos = {}
for dirs in os.listdir(videoRoot):
    if os.path.isdir(os.path.join(videoRoot, dirs)):
        dirPath = os.path.join(videoRoot, dirs)
        paths = []
        vids = []
        for files in os.listdir(dirPath):
            filePath = os.path.join(dirPath, files)
            if os.path.isfile(filePath) and files.endswith(("mov", "mp4")):
                paths.append(filePath)
                vids.append(VideoState(filePath, 0, props, dirs))
        videoPaths[dirs] = paths
        rawVideos[dirs] = vids

print(videoPaths)
print(rawVideos)

# dim = props.getVideoSize()
# videos = []

# pos = props.allocatePosition()
# videos.append(VideoState(location2, 0, pos, dim, props.duration_step, frame_size))

# pos = props.allocatePosition()
# videos.append(VideoState(location2, 0, pos, dim, props.duration_step))

# pos = props.allocatePosition()
# videos.append(VideoState(location3, 0, pos, dim, props.duration_step))

# pos = props.allocatePosition()
# videos.append(VideoState(location4, 0, pos, dim, props.duration_step))

imageclip = ImageClip("../resources/street.jpg").resize(frame_size.getXY())

# def getClipsByDistribution(videos, duration, duration_step, )

distribution = []
for i in range(20):
    distribution.append(random.gauss(4,1))
print(distribution)

print("reached here")

clips = []
clips.append(imageclip)

print("reached here")

for i in range(20):
    for j in range(round(distribution[i])):
        max = len(rawVideos['result'])
        print(max, j)
        
        k = random.randrange(0, max)
        a = datetime.datetime.now()
        
        movie = MovieClip.getNewClipInstance(rawVideos['result'][k])
        b = datetime.datetime.now()
        print("new instance ", str(b-a))
        clip = movie.getClipAt(i*2)
        c = datetime.datetime.now()
        print("get clip ", str(c-b))
        clips.append(clip)
print("reached here")
# movieClip = MovieClip.getNewClipInstance(videos[0])
# clip = movieClip.getClipAt(0)
# clips.append(clip)
video = CompositeVideoClip(clips, use_bgclip=True).set_audio(None)

video.set_duration(props.duration).write_videofile("output.mp4",fps=25,bitrate="1000k",audio_codec=None,codec="mpeg4")
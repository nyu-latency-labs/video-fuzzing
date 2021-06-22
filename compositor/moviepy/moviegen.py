# Import everything needed to edit video clips
from objectrequirement import ObjectRequirement
import re
from moviepy.editor import *
from xy import XY
from videostate import VideoState
from props import Props
from movieclip import MovieClip
import random
import datetime

def discoverVideos(root):
    allVideos = {}
    objTypes = []
    for dirs in os.listdir(root):
        if os.path.isdir(os.path.join(root, dirs)):
            dirPath = os.path.join(root, dirs)
            objTypes.append(dirs)
            paths = []
            vids = []
            for files in os.listdir(dirPath):
                filePath = os.path.join(dirPath, files)
                if os.path.isfile(filePath) and files.endswith(("mov", "mp4")):
                    paths.append(filePath)
                    vids.append(VideoState(filePath, 0, props, dirs))
            allVideos[dirs] = vids
    return (objTypes, allVideos)
    
def generateDistribution(mean, std, count):
    distribution = []
    for i in range(count):
        distribution.append(int(random.gauss(mean, std)))
    print(distribution)
    return distribution

def generateClipsForDistribution(vids, distribution):
    clips = []
    for i in range(len(distribution)):
        print(len(vids), distribution[i])
        val = min(len(vids), distribution[i])
        sample = random.sample(vids, val)

        for data in sample:
            movie = MovieClip.getNewClipInstance(data)
            clip = movie.getClipAt(i*movie.state.duration_step)
            clips.append(clip)
    return clips

def generateClipsForObjectType(type, allVids, mean, std, count):
    distribution = generateDistribution(mean, std, count)
    objVideos = allVids[type]
    clips = generateClipsForDistribution(objVideos, distribution)
    return clips

def generateVideosForRequirements(objReq, vids, count):
    allClips = []
    for req in objReq:
        allClips.extend(generateClipsForObjectType(req.type, vids, req.mean, req.std, count))
    return allClips

FRAME_SIZE = XY(800, 400)
VIDEO_DURATION = 40
VIDEO_STEP_DURATION = 2
VIDEO_ROOT = "../resources/result"
BG_PATH = "../resources/street.jpg"

props = Props(VIDEO_DURATION, VIDEO_STEP_DURATION, FRAME_SIZE)
 
imageclip = ImageClip(BG_PATH).resize(FRAME_SIZE.getXY())

clips = []
clips.append(imageclip)

(objTypes, allVideos) = discoverVideos(VIDEO_ROOT)

# fix distributions
carReq = ObjectRequirement(2, 1, 'cars')
humanReq = ObjectRequirement(1, 0, 'humans')
bikeReq = ObjectRequirement(3, 1, 'bikes')

req = [carReq, humanReq, bikeReq]

clips.extend(generateVideosForRequirements(req, allVideos, props.getStepCount()))

video = CompositeVideoClip(clips, use_bgclip=True).set_audio(None)

video.set_duration(props.duration).write_videofile("output.mp4",fps=25,bitrate="1000k",audio_codec=None,codec="mpeg4")
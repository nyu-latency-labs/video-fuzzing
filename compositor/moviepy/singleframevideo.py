from moviepy.editor import *
from xy import XY
from props import Props
import sys

DURATION_STEP = 2
path = sys.argv[1]

FRAME_SIZE = XY(416, 416)
VIDEO_DURATION = 40
VIDEO_STEP_DURATION = 2
VIDEO_FPS = 25
VIDEO_ROOT = "../resources"
BG_PATH = "../resources/street.jpg"

props = Props(VIDEO_DURATION, VIDEO_STEP_DURATION, FRAME_SIZE, VIDEO_FPS)

clip = ImageClip(path).resize(FRAME_SIZE.get_xy())

clip.set_duration(props.duration).write_videofile("singleframe.mp4", fps=props.fps, bitrate="1000k",
                                                  audio_codec=None,
                                                  codec="mpeg4")

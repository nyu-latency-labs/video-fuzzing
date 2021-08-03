from moviepy.editor import *
import sys
import os

path = sys.argv[1]
base_name = os.path.basename(path).split(".")[0]

video = VideoFileClip(path, audio=False)
fps = [15, 5, 2, 1]
for i in fps:
    video.set_duration(video.duration).write_videofile(base_name + str(i) + ".mp4", fps=i, bitrate="1000k",
                                                       audio_codec=None, codec="mpeg4")

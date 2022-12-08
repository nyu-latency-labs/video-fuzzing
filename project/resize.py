from typing import Tuple, List

from moviepy.editor import *
import sys
import os

path = sys.argv[1]

# i = 0
# for files in os.listdir(path):
#     i += 1
#     file_path = os.path.join(path, files)
#     print(file_path)
#     video = VideoFileClip(file_path, audio=False)
#     clip = video.resize(height=1080)
#     clip.set_duration(video.duration).write_videofile("out/video" + str(i) + ".mp4", fps=30,
#                                                        audio_codec=None, codec="mpeg4")

from PIL import Image


def discover_media(root: str):
    for dirs in os.listdir(root):
        if os.path.isdir(os.path.join(root, dirs)):
            dir_path = os.path.join(root, dirs)
            for files in os.listdir(dir_path):
                file_path = os.path.join(dir_path, files)
                if os.path.isfile(file_path) and files.endswith("jpg"):
                    im1 = Image.open(file_path)
                    im1.save(file_path[:-3] + "png")

file_path = path
im1 = Image.open(file_path)
im1.save(file_path[:-3] + "png")
# discover_media(path)

from moviepy.editor import *
import sys

src = sys.argv[1]
dst = sys.argv[2]

def resize(path, dest):
    clip = VideoFileClip(path, audio=False)
    height = min(720, clip.size[1])
    clip.resize(height=height).set_duration(clip.duration).write_videofile(dest,fps=30,bitrate="1000k",audio_codec=None,codec="mpeg4")

for dirs in os.listdir(src):
    if os.path.isdir(os.path.join(src, dirs)):
        dirPath = os.path.join(src, dirs)
        for files in os.listdir(dirPath):
            filePath = os.path.join(dirPath, files)
            if os.path.isfile(filePath) and files.endswith(("mov", "mp4")):
                resize(filePath, os.path.join(dirPath, "result", files))

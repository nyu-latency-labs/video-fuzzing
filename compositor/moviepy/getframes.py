from moviepy.editor import *
from pathlib import Path
import sys

DURATION_STEP = 2
path = sys.argv[1]
base_name = os.path.basename(path).split(".")[0]

video = VideoFileClip(path, audio=False)
frames = []

Path(base_name + "_frames").mkdir(parents=True, exist_ok=True)

for i in range(int(DURATION_STEP / 2), int(video.duration), DURATION_STEP):
    frame = video.get_frame(i)
    video.save_frame(base_name + "_frames/frame_" + str(i) + ".png", t=i)

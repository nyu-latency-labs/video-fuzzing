import math
import random

from objectrequirement import ObjectRequirement
from moviepy.editor import *
from xy import XY
from videostate import VideoState
from props import Props
import json
import sys


def discover_media(root):
    all_media = {}
    obj_types = []
    for dirs in os.listdir(root):
        if os.path.isdir(os.path.join(root, dirs)):
            dir_path = os.path.join(root, dirs)
            obj_types.append(dirs)
            paths = []
            media = []
            for files in os.listdir(dir_path):
                file_path = os.path.join(dir_path, files)
                if os.path.isfile(file_path) and files.endswith(("jpg")):
                    paths.append(file_path)
                    media.append(VideoState(file_path, 0, props, dirs))
            all_media[dirs] = media
    return obj_types, all_media


def generate_videos_for_requirements(obj_req, videos):
    all_clips = []
    for requirement in obj_req:
        all_clips.extend(requirement.generate_clips_from_video(videos))
    return all_clips


FRAME_SIZE = XY(416, 416)
VIDEO_DURATION = 40
VIDEO_STEP_DURATION = 2
VIDEO_FPS = 25
VIDEO_ROOT = "../resources"
BG_PATH = "../resources/street.jpg"
N_TIMES = 1

output_name = sys.argv[1]
props = Props(VIDEO_DURATION, VIDEO_STEP_DURATION, FRAME_SIZE, VIDEO_FPS)

image_clip = ImageClip(BG_PATH).resize(FRAME_SIZE.get_xy())

clips = [image_clip]

(objTypes, all_media) = discover_media(VIDEO_ROOT)
# print(objTypes)

# fix distributions
carReq = ObjectRequirement(2, 1, 'car', props)
humanReq = ObjectRequirement(2, 1, 'person', props)
bikeReq = ObjectRequirement(2, 1, 'motorcycle', props)

req = [carReq, humanReq, bikeReq]
# req = [carReq]

total_dist = [0 for i in range(props.step_count * props.fps)]

for r in req:
    print(r.distribution)
    for i in range(len(r.distribution)):
        for j in range(props.fps):
            total_dist[i * props.fps + j] += r.distribution[i]

max_object_num = max(total_dist)

# hard code to  3x3 matrix
for i in range(props.step_count):
    num_obj = 0
    for obj_r in req:
        if num_obj == 9:
            break

        k = obj_r.distribution[i]
        val = min(len(all_media[obj_r.type]), k)
        sample = random.sample(all_media[obj_r.type], val)
        for j in sample:
            klip = j.generate_clip(num_obj, 3, 3)
            _klip = j.get_next_step_clip(i*props.duration_step, klip)
            clips.append(_klip)
            num_obj += 1


def get_objects_frame_level(prop, requirements):
    total_dist_val = []
    for i in range(prop.step_count):
        tmp = []
        for requirement in requirements:
            if requirement.distribution[i] > 0:
                tmp.append(requirement.type)
        for e in range(prop.fps * prop.duration_step):
            total_dist_val.append(tmp)

    return total_dist_val


# Generate multiple videos of the same distribution
for i in range(N_TIMES):
#     clips.extend(generate_videos_for_requirements(req, all_media))

    video = CompositeVideoClip(clips, use_bgclip=True).set_audio(None)

    output_file_name = output_name + ("" if N_TIMES == 1 else str(i)) + ".mp4"
    video.set_duration(props.duration).write_videofile(output_file_name, fps=props.fps, bitrate="1000k",
                                                       audio_codec=None,
                                                       codec="mpeg4")

data = {'distribution': total_dist, 'object_distribution': get_objects_frame_level(props, req)}
json_data = json.dumps(data)

output_json = open(output_name + '.json', 'w')
output_json.write(json_data)
output_json.close()

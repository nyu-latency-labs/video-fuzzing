from objectrequirement import ObjectRequirement
from moviepy.editor import *
from xy import XY
from videostate import VideoState
from props import Props
import json
import sys


def discover_videos(root):
    all_videos = {}
    obj_types = []
    for dirs in os.listdir(root):
        if os.path.isdir(os.path.join(root, dirs)):
            dir_path = os.path.join(root, dirs)
            obj_types.append(dirs)
            paths = []
            vids = []
            for files in os.listdir(dir_path):
                file_path = os.path.join(dir_path, files)
                if os.path.isfile(file_path) and files.endswith(("mov", "mp4")):
                    paths.append(file_path)
                    vids.append(VideoState(file_path, 0, props, dirs))
            all_videos[dirs] = vids
    return obj_types, all_videos


def generate_videos_for_requirements(obj_req, vids):
    all_clips = []
    for req in obj_req:
        all_clips.extend(req.generate_clips_from_video(vids))
    return all_clips


FRAME_SIZE = XY(800, 400)
VIDEO_DURATION = 40
VIDEO_STEP_DURATION = 2
VIDEO_FPS = 25
VIDEO_ROOT = "../resources/result"
BG_PATH = "../resources/street.jpg"
N_TIMES = 1

output_name = sys.argv[1]
props = Props(VIDEO_DURATION, VIDEO_STEP_DURATION, FRAME_SIZE, VIDEO_FPS)

image_clip = ImageClip(BG_PATH).resize(FRAME_SIZE.getXY())

clips = [image_clip]

(objTypes, allVideos) = discover_videos(VIDEO_ROOT)

# fix distributions
carReq = ObjectRequirement(1, 0, 'car', props)
humanReq = ObjectRequirement(1, 1, 'person', props)
bikeReq = ObjectRequirement(1, 1, 'motorcycle', props)

req = [carReq, humanReq, bikeReq]
# req = [carReq]

total_dist = [0 for i in range(props.step_count * props.fps)]

for r in req:
    print(r.distribution)
    for i in range(len(r.distribution)):
        for j in range(props.fps):
            total_dist[i * props.fps + j] += r.distribution[i]


def get_objects_frame_level(props, requirements):
    total_dist_val = []
    for i in range(props.step_count):
        tmp = []
        for req in requirements:
            if req.distribution[i] > 0:
                tmp.append(req.type)
        for j in range(props.fps * props.duration_step):
            total_dist_val.append(tmp)

    return total_dist_val


# Generate multiple videos of the same distribution
for i in range(N_TIMES):
    clips.extend(generate_videos_for_requirements(req, allVideos))

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

import random

from movieclip import MovieClip
from props import Props


def generate_distribution(mean, std, count):
    distribution = []
    for i in range(count):
        distribution.append(int(random.gauss(mean, std)))
    # print(distribution)
    return distribution


def generate_clips_for_distribution(videos, distribution):
    video_clips = []
    for i in range(len(distribution)):
        val = min(len(videos), distribution[i])
        sample = random.sample(videos, val)

        for data in sample:
            movie = MovieClip.getNewClipInstance(data)
            clip = movie.getClipAt(i * movie.state.duration_step)
            video_clips.append(clip)
    return video_clips


class ObjectRequirement:
    mean = None
    std = None
    props = None
    type = None
    distribution = None

    def __init__(self, mean, std, obj_type, props: Props, dist=None):
        self.mean = mean
        self.std = std
        self.type = obj_type
        self.props = props
        if dist is None:
            self.distribution = generate_distribution(mean, std, props.getStepCount())
        else:
            self.distribution = dist

    def generate_clips_from_video(self, videos):
        video_clips = generate_clips_for_distribution(videos[self.type], self.distribution)
        return video_clips

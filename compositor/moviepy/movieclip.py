import random
from videostate import VideoState


class MovieClip:
    clip = None
    state = None

    def __init__(self, clip, state: VideoState):
        self.state = state
        # Get clip, resize, crop, place and save state.
        self.clip = self.state.resize_and_crop_video(clip)
        self.set_new_position()

    def set_new_position(self):
        frame_size = self.state.frame_size
        self.clip = self.clip.set_position((random.randrange(0, frame_size.x), random.randrange(0, frame_size.y)))

    def get_clip_at(self, time):
        clip = self.state.get_next_step_clip(time, self.clip)
        return clip

    @classmethod
    def get_new_clip_instance(cls, state: VideoState):
        return MovieClip(state.original_clip, state)

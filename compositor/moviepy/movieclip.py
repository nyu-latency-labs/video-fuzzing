import random
from videostate import VideoState

class MovieClip:
    clip = None
    state = None

    def __init__(self, clip, state: VideoState):
        self.state = state
        # Get clip, resize, crop, place and save state.
        self.clip = self.state.resizeAndCropVideo(clip)
        self.setNewPosition()

    def setNewPosition(self):
        frame_size = self.state.frame_size
        self.clip = self.clip.set_position((random.randrange(0,frame_size.x), random.randrange(0, frame_size.y)))

    def getClipAt(self, time):
        clip = self.state.getNextStepClip(time, self.clip)
        return clip

    @classmethod
    def getNewClipInstance(cls, state: VideoState):
        return MovieClip(state.original_clip, state)
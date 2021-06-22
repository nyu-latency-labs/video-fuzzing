from xy import XY

class Props:
    duration = 10
    duration_step = 2
    dim = None
    step_count = 5

    def __init__(self, duration, duration_step, dim: XY):
        self.duration = duration
        self.duration_step = duration_step
        self.dim = dim
        self.step_count = int(duration/duration_step)

    def getVideoSize(self):
        return XY(self.size.x, self.size.y)

    def getStepCount(self):
        return self.step_count
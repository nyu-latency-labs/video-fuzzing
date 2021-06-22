from xy import XY

class Props:
    duration = 10
    duration_step = 2
    dim = None

    def __init__(self, duration, duration_step, grid: XY, dim: XY):
        self.duration = duration
        self.duration_step = duration_step
        self.dim = dim

    def getVideoSize(self):
        return XY(self.size.x, self.size.y)
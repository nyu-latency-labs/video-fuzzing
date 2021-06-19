from xy import XY

class Props:
    duration = 10
    duration_step = 2
    grid = None
    dim = None
    grid_occupied = None
    size = None

    def __init__(self, duration, duration_step, grid: XY, dim: XY):
        self.duration = duration
        self.duration_step = duration_step
        self.grid = grid
        self.dim = dim
        self.grid_occupied = [ [False]*grid.y for i in range(grid.x)]
        self.size = XY(dim.x/grid.x, dim.y/grid.y)

    def allocatePosition(self):
        for i in range(self.grid.x):
            for j in range(self.grid.y):
                if ( not self.grid_occupied[i][j]):
                    self.grid_occupied[i][j] = True
                    return XY(i*self.size.x, j*self.size.y)
        return XY(-1,-1)

    def freePosition(self, pos: XY):
        self.grid_occupied[pos.x][pos.y] = False

    def getVideoSize(self):
        return XY(self.size.x, self.size.y)
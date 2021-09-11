class XY:
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_xy(self):
        return self.x, self.y

    @classmethod
    def from_tuple(cls, tup):
        (x, y) = tup
        return XY(x, y)

    def __str__(self):
        return "[" + str(self.x) + ", " + str(self.y) + "]"

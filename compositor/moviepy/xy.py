class XY:
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getXY(self):
        return (self.x, self.y)

    @classmethod
    def fromTuple(cls, tuple):
        (x,y) = tuple
        return XY(x,y)

    def __str__(self):
        return "[" + str(self.x) + ", " + str(self.y) + "]"

class ObjectRequirement:
    mean = None
    std = None
    type = None

    def __init__(self, mean, std, type):
        self.mean = mean
        self.std = std
        self.type = type
    
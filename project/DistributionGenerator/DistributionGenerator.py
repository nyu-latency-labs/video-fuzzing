
class DistributionGenerator:
    fn = None

    def __init__(self, fn):
        self.fn = fn

    def get_next(self):
        return self.fn()


class DistributionGenerator:
    fn = None
    ds = None

    def __init__(self, ds, fn=None):
        self.fn = fn
        self.ds = ds

    def get_next(self):
        return self.fn()

    def process_distribution(self):
        pass

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['fn']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.process_distribution()

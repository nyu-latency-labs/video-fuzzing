from Pipeline.PipelineUnit import PipelineUnit


class Transformer(PipelineUnit):

    def __init__(self, data=None):
        self.name = "transformer"

    def apply(self, data):
        return data

    @classmethod
    def create_from_config(cls, data):
        return Transformer(data)

    def __str__(self):
        raise NotImplementedError("Transformer should implement __str__ method to enable caching")

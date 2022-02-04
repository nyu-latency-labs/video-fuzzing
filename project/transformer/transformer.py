from pipeline.pipelineunit import PipelineUnit


class Transformer(PipelineUnit):
    """
    A type of PipelineUnit used to make transformations to input clip.
    This class needs to be extended to create custom transformers.
    """

    def __init__(self, data=None):
        self.name = "transformer"

    def apply(self, data):
        raise NotImplementedError("Apply method not implemented.")

    def validate(self, data):
        raise NotImplementedError("Validate method not implemented.")

    @classmethod
    def create_from_config(cls, data):
        return Transformer(data)

    def __str__(self):
        raise NotImplementedError("Transformer should implement __str__ method to enable caching")

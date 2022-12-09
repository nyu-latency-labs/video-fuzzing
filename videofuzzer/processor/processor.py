from ..config.config import Config
from ..pipeline.pipelineunit import PipelineUnit


class Processor(PipelineUnit):
    """
    A type of PipelineUnit used to add any custom processing to the pipeline.
    Examples are pre and post processor.
    """

    def __init__(self, config: Config):
        self.name = "processor"
        self.config = config

    def apply(self, data):
        raise NotImplementedError("Apply method not implemented.")

    def validate(self, data):
        raise NotImplementedError("Validate method not implemented.")

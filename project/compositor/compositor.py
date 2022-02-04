from config.config import Config
from pipeline.pipelineunit import PipelineUnit


class Compositor(PipelineUnit):
    bg = None
    clips = []

    def __init__(self, config: Config):
        self.config = config
        self.name = "compositor"

    def apply(self, data: dict) -> dict:
        raise NotImplementedError("Apply method not implemented.")

    def validate(self, data):
        raise NotImplementedError("Validate method not implemented.")

    @classmethod
    def create_from_config(cls, config: Config):
        return Compositor(config)

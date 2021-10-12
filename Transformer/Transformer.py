from Config.Config import Config
from Pipeline.PipelineUnit import PipelineUnit


class Transformer(PipelineUnit):

    def __init__(self, config: Config):
        self.name = "transformer"
        self.config = config

    def apply(self, data):
        return data

    @classmethod
    def create_from_config(cls, config: Config, data):
        return Transformer(config)

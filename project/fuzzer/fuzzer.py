from config.config import Config
from pipeline.pipelineunit import PipelineUnit


class Fuzzer(PipelineUnit):

    def __init__(self, config: Config, data):
        self.name = "fuzzer"
        self.config = config
        self.data = data
        self.transformers = data["transformers"]

    def apply(self, data):
        raise NotImplementedError("Apply method not implemented.")

    def validate(self, data):
        raise NotImplementedError("Validate method not implemented.")

    @classmethod
    def create_from_config(cls, config: Config, data):
        return Fuzzer(config, data)

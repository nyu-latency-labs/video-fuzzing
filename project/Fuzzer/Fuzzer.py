from Config.Config import Config
from Pipeline.PipelineUnit import PipelineUnit


class Fuzzer(PipelineUnit):

    def __init__(self, config: Config, data):
        self.name = "fuzzer"
        self.config = config
        self.data = data
        self.transformers = data["transformers"]

    def apply(self, data=None):
        return data

    @classmethod
    def create_from_config(cls, config: Config, data):
        return Fuzzer(config, data)

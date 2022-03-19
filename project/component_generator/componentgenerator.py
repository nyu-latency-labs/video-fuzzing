from pipeline.pipelineunit import PipelineUnit
from utils.singleton import Singleton


class ComponentGenerator(metaclass=Singleton):
    config = None

    def __init__(self, config):
        self.config = config

    def process(self, ds) -> PipelineUnit:
        pass
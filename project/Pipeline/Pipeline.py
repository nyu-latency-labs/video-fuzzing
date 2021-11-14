import copy
import logging
import random
from time import perf_counter

from Config.Config import Config
from Processor.PostProcessor import PostProcessor
from Processor.PreProcessor import PreProcessor
from Transformer.MultiTransformer import MultiTransformer
from Utils.ComponentProcessor import ComponentProcessor
from Utils.Timer import timer


class Pipeline:
    config = None

    @timer
    def apply(self, filename):
        random.seed(10)
        config = Config(filename)
        self.config = config

        component_processor = ComponentProcessor(config)

        transformers = component_processor.process_transformer(config.data["transformers"])
        fuzzer = component_processor.process_fuzzer(config.data["fuzzer"])

        data = {
            "max_cores": self.config.max_cores,
            "use_cache": self.config.use_cache,
            "transformers": [
                {
                    "applied": False,
                    "transformers": transformers,
                    "type": "global"
                }
            ]
        }

        fuzzer_output = fuzzer.apply(data)
        self.run_pipeline(fuzzer_output, config)

    @timer
    def run_pipeline(self, fuzzer_output, config):
        component_processor = ComponentProcessor(config)
        compositor = component_processor.process_compositor(config.data["compositor"])
        multi_transformer = MultiTransformer(config)
        preprocessor = PreProcessor(config)
        postprocessor = PostProcessor(config)

        for output in fuzzer_output:
            for i in range(output["num_videos"]):
                data = copy.deepcopy(output)
                data["max_cores"] = config.max_cores
                data["filename"] = output["filename_prefix"] + "_" + str(i) + ".mp4"

                processing_pipeline = [preprocessor, multi_transformer, multi_transformer,
                                       compositor, postprocessor]

                for processor in processing_pipeline:
                    data = processor.apply(data)

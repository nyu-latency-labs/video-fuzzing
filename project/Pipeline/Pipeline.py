import copy
import logging
import random

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
            "transformers": [
                {
                    "applied": False,
                    "transformers": transformers,
                    "type": "global"
                }
            ]
        }

        fuzzer_output = fuzzer.apply(data)
        # For benchmarking
        for time in range(10, 300, 10):
            logging.info("Running for time: " + str(time))
            for cpu in range(1, 33):
                logging.info("Running for cpu: " + str(cpu))
                new_config = copy.copy(config)
                new_config.duration = time
                new_config.max_cores = cpu
                self.run_pipeline(fuzzer_output, new_config)

    @timer
    def run_pipeline(self, fuzzer_output, config):
        component_processor = ComponentProcessor(config)
        compositor = component_processor.process_compositor(config.data["compositor"])
        multi_transformer = MultiTransformer(config)
        preprocessor = PreProcessor(config)
        postprocessor = PostProcessor(config)

        for output in fuzzer_output:
            for i in range(output["num_videos"]):
                data = copy.copy(output)
                data["filename"] = output["filename_prefix"] + "_" + str(i) + ".mp4"

                processing_pipeline = [preprocessor, multi_transformer, multi_transformer,
                                       compositor, postprocessor]

                for processor in processing_pipeline:
                    data = processor.apply(data)

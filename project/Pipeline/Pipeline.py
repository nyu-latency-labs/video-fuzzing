import copy
import logging
import random

from Config.Config import Config
from Processor.PostProcessor import PostProcessor
from Processor.PreProcessor import PreProcessor
from Transformer.MultiTransformer import MultiTransformer
from Utils.ComponentProcessor import ComponentProcessor
from Utils.NonDaemonicProcess import NestablePool
from Utils.Timer import timer


def pipeline_task(config, inp, pos):
    component_processor = ComponentProcessor(config)
    compositor = component_processor.process_compositor(config.data["compositor"])
    multi_transformer = MultiTransformer(config)
    preprocessor = PreProcessor(config)
    postprocessor = PostProcessor(config)

    data = copy.deepcopy(inp)
    data["max_tx_cores"] = config.max_tx_cores
    data["filename"] = inp["filename_prefix"] + "_" + str(pos) + ".mp4"

    processing_pipeline = [preprocessor, multi_transformer, multi_transformer,
                           compositor, postprocessor]

    for processor in processing_pipeline:
        data = processor.apply(data)


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
            "max_tx_cores": self.config.max_tx_cores,
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

        logging.info("Using %s cores", config.max_cores)
        pool = NestablePool(config.max_cores)

        for output in fuzzer_output:
            for i in range(output["num_videos"]):
                pool.apply_async(pipeline_task, (config, output, i,))

        pool.close()
        pool.join()

import copy
import logging
import random

from config.config import Config
from processor.metadataprocessor import MetadataProcessor
from processor.postprocessor import PostProcessor
from processor.preprocessor import PreProcessor
from transformer.multitransformer import MultiTransformer
from utils.componentprocessor import ComponentProcessor
from utils.nondaemonicprocess import NestablePool
from utils.timer import timer


def pipeline_task(config: Config, data: dict, n: int):
    component_processor = ComponentProcessor(config)
    compositor = component_processor.process_compositor(config.data["compositor"])
    multi_transformer = MultiTransformer(config)
    preprocessor = PreProcessor(config)
    postprocessor = PostProcessor(config)
    metaprocessor = MetadataProcessor(config)

    data["filename"] = data["filename_prefix"] + "_" + str(n)

    processing_pipeline = [preprocessor, metaprocessor, multi_transformer, multi_transformer, compositor, postprocessor]

    for processor in processing_pipeline:
        data = processor.apply(data)


class Pipeline:
    config = None

    @timer
    def apply(self, filename: str):
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
        # total_latencies = []
        # for i in range(32, 0, -1): #cpu
        #     logging.info("Running for processes: " + str(i))
        #     latency = []
        #     import os, shutil
        #     os.makedirs("tmp/", exist_ok=True)
        #     for j in range(1, 32): #thread
        #         if i*j > 32:
        #             break
        #         data_copy = copy.deepcopy(fuzzer_output)
        #         for idx in data_copy:
        #             idx["max_cores"] = i
        #             idx["max_tx_cores"] = j
        #         logging.info("Running for thread: " + str(j))
        #         start_time = perf_counter()
        #         new_config = copy.deepcopy(config)
        #         new_config.max_cores = i
        #         self.run_pipeline(data_copy,  new_config)
        #         end_time = perf_counter()  # 2
        #         run_time = end_time - start_time
        #         latency.append(run_time)
        #     total_latencies.append(latency)
        #     shutil.rmtree("tmp/")
        #
        # print(total_latencies)

        self.run_pipeline(fuzzer_output, config)

    @timer
    def run_pipeline(self, fuzzer_output: dict, config: Config):

        logging.info("Using %s cores", config.max_cores)
        pool = NestablePool(config.max_cores)

        results = []
        for output in fuzzer_output:
            for i in range(output["num_videos"]):
                results.append(pool.apply_async(pipeline_task, (copy.deepcopy(config), copy.deepcopy(output), i,)))
                # pipeline_task(copy.deepcopy(config), copy.deepcopy(output), i)
        pool.close()

        for r in results:
            r.get()

        pool.join()

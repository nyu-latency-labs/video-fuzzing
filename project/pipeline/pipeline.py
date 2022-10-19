import copy
import logging
import random
from time import perf_counter

from component_generator.compositorgenerator import CompositorGenerator
from component_generator.fuzzergenerator import FuzzerGenerator
from config.config import Config
from inference.modelfactory import ModelFactory
from inference.model import Model
from processor.metadataprocessor import MetadataProcessor
from processor.postprocessor import PostProcessor
from processor.preprocessor import PreProcessor
from transformer.multitransformer import MultiTransformer
from utility.multiprocessinglog import worker_init, logger_init
from utility.nondaemonicprocess import NestablePool
from utility.timer import timer


@timer
def pipeline_task(config: Config, data: dict):
    compositor_generator = CompositorGenerator(config)
    compositor = compositor_generator.process(data["compositor"])
    multi_transformer = MultiTransformer(config)
    preprocessor = PreProcessor(config)
    postprocessor = PostProcessor(config)
    meta_processor = MetadataProcessor(config)
    model_inference = ModelFactory.get_model(config)

    processing_pipeline = [preprocessor, meta_processor, multi_transformer, compositor, postprocessor, model_inference]

    for processor in processing_pipeline:
        data = processor.apply(data)


class Pipeline:
    config = None

    @timer
    def apply(self, filename: str):
        random.seed(10)
        config = Config(filename)
        self.config = config

        fuzzer_processor = FuzzerGenerator(config)
        fuzzer = fuzzer_processor.process(config.data["fuzzer"])

        data = {
            "max_cores": self.config.max_cores,
            "use_cache": self.config.use_cache,
        }

        fuzzer_output = fuzzer.apply(data)

        self.run_pipeline(fuzzer_output, config)

    @timer
    def run_pipeline(self, fuzzer_output: dict, config: Config):

        logging.info("Using %s cores", config.pipeline_cores)

        q_listener, q = logger_init()
        pool = NestablePool(config.pipeline_cores, worker_init, [q])

        results = []
        for output in fuzzer_output:
            # results.append(pool.apply_async(pipeline_task, (copy.deepcopy(config), copy.deepcopy(output),)))
            pipeline_task(copy.deepcopy(config), copy.deepcopy(output))
        pool.close()

        for r in results:
            r.get()

        pool.join()

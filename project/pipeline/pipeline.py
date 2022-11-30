import copy
import logging
import random

from component_generator.compositorgenerator import CompositorGenerator
from config.config import Config
from fuzzer.randomizedfuzzer import RandomizedFuzzer
from inference.modelfactory import ModelFactory
from processor.finalprocessor import FinalProcessor
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
    finalprocessor = FinalProcessor(config)
    meta_processor = MetadataProcessor(config)
    model_inference = []
    for model in config.model:
        model_inference.append(ModelFactory.get_model(config, model))

    processing_pipeline = [preprocessor, meta_processor, multi_transformer, compositor, postprocessor]
    processing_pipeline.extend(model_inference)
    processing_pipeline.append(finalprocessor)

    for processor in processing_pipeline:
        data = processor.apply(data)

    data_to_return = {"config": data["final_config"], "metrics": data["inference"][0]["model_accuracy"]}
    return data_to_return


class Pipeline:
    config = None

    @timer
    def apply(self, filename: str):
        config = Config(filename)
        self.config = config
        # data = []

        # generate videos with 10deg diff
        # for i in range(0, 1, 10):
        #     random.seed(10)
        #     config.data["transformers"][0]["angle"] = i
        #     fuzzer_output = RandomizedFuzzer(config).apply({"idx": i})
        #     data.append(fuzzer_output[0])
        fuzzer_output = RandomizedFuzzer(config).apply()
        self.run_pipeline(fuzzer_output, config)

    @timer
    def run_pipeline(self, fuzzer_output: dict, config: Config):
        logging.info("Using %s cores", config.pipeline_cores)

        q_listener, q = logger_init()
        pool = NestablePool(config.pipeline_cores, worker_init, [q])

        data = []
        results = []
        for output in fuzzer_output:
            results.append(pool.apply_async(pipeline_task, (copy.deepcopy(config), copy.deepcopy(output),)))
            # data.append(pipeline_task(copy.deepcopy(config), copy.deepcopy(output)))
        pool.close()
        pool.join()


        for r in results:
            data.append(r.get())

        # precision = []
        # recall = []
        # for d in data:
        #     precision.append(d["precision"])
        #     recall.append(d["recall"])



        # logging.info(data)
        # logging.info(recall)

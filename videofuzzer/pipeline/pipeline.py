import copy
import json
import logging
import multiprocessing

from ..component_generator.compositorgenerator import CompositorGenerator
from ..config.config import Config
from ..fuzzer.randomizedfuzzer import RandomizedFuzzer
from ..inference.modelfactory import ModelFactory
from ..processor.finalprocessor import FinalProcessor
from ..processor.metadataprocessor import MetadataProcessor
from ..processor.postprocessor import PostProcessor
from ..processor.preprocessor import PreProcessor
from ..transformer.multitransformer import MultiTransformer
from ..utility.multiprocessinglog import worker_init, logger_init
from ..utility.nondaemonicprocess import NestablePool
from ..utility.timer import timer


@timer
def pipeline_task(config: Config, data: dict, idx: int):
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
    def apply(self, filename: str = None, data_dict: list = None, ncpus=1):


        # to support old method to fetch data
        # python main.py config.json
        # data_dict method to support calling as lib
        data = []
        if filename is not None:
            with open(filename) as f:
                input = json.load(f)
                input["filename"] = filename
                config = Config(input)
                fuzzer_output = RandomizedFuzzer(config).apply()
                for fout in fuzzer_output:
                    data.append((config, fout))
                ncpus = min(input["max_cores"], multiprocessing.cpu_count())

        else:
            # assuming only single output for data dict
            for ddict in data_dict:
                config = Config(ddict)
                fuzzer_output = RandomizedFuzzer(config).apply()
                data.append((config, fuzzer_output[0]))

        return self.run_pipeline(data, ncpus)

    @timer
    def run_pipeline(self, fuzzer_outputs: list, ncpus: int):
        logging.info("Using %s cores", ncpus)

        data = []

        if ncpus == 1:
            for idx, output in enumerate(fuzzer_outputs):
                data.append(pipeline_task(output[0], output[1], idx, ))
        else:
            q_listener, q = logger_init()
            pool = NestablePool(ncpus, worker_init, [q])

            results = []
            for idx, output in enumerate(fuzzer_outputs):
                results.append(pool.apply_async(pipeline_task, (output[0], output[1], idx,)))
            pool.close()
            pool.join()

            for r in results:
                data.append(r.get())

        return data

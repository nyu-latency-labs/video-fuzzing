import copy

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
        config = Config(filename)
        self.config = config

        component_processor = ComponentProcessor(config)

        transformers = component_processor.process_transformer(config.data["transformers"])
        fuzzer = component_processor.process_fuzzer(config.data["fuzzer"])
        compositor = component_processor.process_compositor(config.data["compositor"])

        preprocessor = PreProcessor(config)
        postprocessor = PostProcessor(config)

        multi_transformer = MultiTransformer(config)
        multi_transformer1 = MultiTransformer(config)

        fuzzer_output = fuzzer.apply()

        for output in fuzzer_output:
            for i in range(output["num_videos"]):
                data = copy.copy(output)
                data["global_transformers"] = transformers
                data["global_transformers_applied"] = False
                data["local_transformers_applied"] = False
                data["filename"] = output["filename_prefix"] + "_" + str(i) + ".mp4"

                processing_pipeline = [preprocessor, multi_transformer, multi_transformer1,
                                       compositor, postprocessor]

                for processor in processing_pipeline:
                    data = processor.apply(data)

import logging
import sys

from Compositor.Compositor import Compositor
from Compositor.GridCompositor import GridCompositor
from Config.Config import Config
from Fuzzer.ExperimentFuzzer import ExperimentFuzzer
from Fuzzer.Fuzzer import Fuzzer
from Processor.PostProcessor import PostProcessor
from Processor.PreProcessor import PreProcessor
from Transformer.ResizeTransformer import ResizeTransformer
from Transformer.RotateTransformer import RotateTransformer
from Transformer.Transformer import Transformer


class Pipeline:
    config = None

    def apply(self, filename):
        config = Config(filename)
        self.config = config

        transformers = self.process_transformer(config.data["transformers"])
        fuzzer = self.process_fuzzer(config.data["fuzzer"])
        compositor = self.process_compositor(config.data["compositor"])

        preprocessor = PreProcessor(config)
        postprocessor = PostProcessor(config)

        global_transformers = transformers

        fuzzer_output = fuzzer.apply()

        for output in fuzzer_output:
            for i in range(output["num_videos"]):
                logging.info("In PreProcessor step")
                preprocessor_result = preprocessor.apply(output)
                logging.info("PreProcessor step done")

                local_transformers = global_transformers.copy()
                local_transformers.append(output["transformers"])

                logging.info("In Transformer pipeline step")
                # Transform all videos
                transformer_result = []
                for video in preprocessor_result:
                    for transformer in local_transformers:
                        logging.debug("Making transformations on the video. Please be patient.")
                        video = transformer.apply(video)
                    transformer_result.append(video)
                logging.info("Transformer pipeline step done")

                logging.info("In Compositor step")
                compositor_result = compositor.apply(transformer_result)
                logging.info("Compositor step done")

                postprocessor_input = {
                    "video": compositor_result,
                    "filename": output["filename_prefix"] + "_" + str(i) + ".mp4"
                }

                logging.info("In PostProcessor step")
                postprocessor_output = postprocessor.apply(postprocessor_input)
                logging.info("PostProcessor step done")

    def process_transformer(self, tx):
        transformers = []

        for element in tx:
            tx_type = element["type"]

            if tx_type == "rotate_transformer":
                transformers.append(RotateTransformer.create_from_config(self.config, element))
            elif tx_type == "resize_transformer":
                transformers.append(ResizeTransformer.create_from_config(self.config, element))
            else:
                transformers.append(Transformer.create_from_config(self.config, element))

        return transformers

    def process_fuzzer(self, fz):
        fz_type = fz["type"]

        tx = self.process_transformer(fz["transformers"])
        fz["transformers"] = tx

        if fz_type == "experiment_fuzzer":
            return ExperimentFuzzer.create_from_config(self.config, fz)
        else:
            return Fuzzer(self.config, fz)

    def process_compositor(self, cs):
        cs_type = cs["type"]

        if cs_type == "grid_compositor":
            return GridCompositor.create_from_config(self.config)
        else:
            return Compositor(self.config)


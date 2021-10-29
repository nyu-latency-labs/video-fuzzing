import copy
import logging
import multiprocessing
import uuid

from moviepy.video.VideoClip import ImageClip

from Compositor.Compositor import Compositor
from Compositor.GridCompositor import GridCompositor
from Compositor.MovingCompositor import MovingCompositor
from Config.Config import Config
from Fuzzer.ExperimentFuzzer import ExperimentFuzzer
from Fuzzer.Fuzzer import Fuzzer
from Transformer.MultiTransformer import MultiTransformer
from Utils.ComponentProcessor import ComponentProcessor
from Utils.Timer import timer
from Processor.PostProcessor import PostProcessor
from Processor.PreProcessor import PreProcessor
from Transformer.ResizeTransformer import ResizeTransformer
from Transformer.RotateTransformer import RotateTransformer
from Transformer.Transformer import Transformer


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

        global_transformers = transformers

        fuzzer_output = fuzzer.apply()

        for output in fuzzer_output:
            for i in range(output["num_videos"]):
                data = copy.copy(output)
                data = preprocessor.apply(data)

                local_transformers = global_transformers.copy()
                local_transformers.append(data["transformers"])
                data["transformers"] = local_transformers

                data = multi_transformer.apply(data)

                data = compositor.apply(data)

                data["filename"] = output["filename_prefix"] + "_" + str(i) + ".mp4"

                data = postprocessor.apply(data)


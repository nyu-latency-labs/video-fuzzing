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
from Utils.Timer import timer
from Processor.PostProcessor import PostProcessor
from Processor.PreProcessor import PreProcessor
from Transformer.ResizeTransformer import ResizeTransformer
from Transformer.RotateTransformer import RotateTransformer
from Transformer.Transformer import Transformer


def transformer_task(video, tx_list, out_list):
    clip = video.get_video()
    for tx in tx_list:
        clip = tx.apply(clip)

    tmp_name = "tmp/"
    if type(clip) is ImageClip:
        tmp_name = tmp_name + str(uuid.uuid4()) + ".jpg"
        clip.save_frame(tmp_name, 0)
        logging.debug("Saving ImageClip frame as jpg")
    else:
        tmp_name = tmp_name + str(uuid.uuid4()) + ".mp4"
        clip.write_videofile(tmp_name, 25, "mpeg4", audio=False, bitrate="1000k")
    video.filepath = tmp_name
    out_list.append(video)
    logging.debug("Updated video references")


class Pipeline:
    config = None

    @timer
    def apply(self, filename):
        config = Config(filename)
        self.config = config

        transformers = self.process_transformer(config.data["transformers"])
        fuzzer = self.process_fuzzer(config.data["fuzzer"])
        compositor = self.process_compositor(config.data["compositor"])

        preprocessor = PreProcessor(config)
        postprocessor = PostProcessor(config)

        multitransformer = MultiTransformer(config)

        global_transformers = transformers

        fuzzer_output = fuzzer.apply()

        for output in fuzzer_output:
            for i in range(output["num_videos"]):
                data = output
                data = preprocessor.apply(data)

                local_transformers = global_transformers.copy()
                local_transformers.append(data["transformers"])
                data["transformers"] = local_transformers

                data = multitransformer.apply(data)

                data = compositor.apply(data)

                data["filename"] = output["filename_prefix"] + "_" + str(i) + ".mp4"

                postprocessor_output = postprocessor.apply(data)

    def process_transformer(self, tx):
        transformers = []

        for element in tx:
            tx_type = element["type"]

            if tx_type == "rotate_transformer":
                transformers.append(RotateTransformer.create_from_config(element))
            elif tx_type == "resize_transformer":
                transformers.append(ResizeTransformer.create_from_config(element))
            else:
                transformers.append(Transformer.create_from_config(element))

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
        if cs_type == "moving_compositor":
            return MovingCompositor.create_from_config(self.config)
        else:
            return Compositor(self.config)


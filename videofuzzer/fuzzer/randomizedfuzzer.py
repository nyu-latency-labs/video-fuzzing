import copy
import logging
import random
from enum import IntEnum

from ..component_generator.transformergenerator import TransformerGenerator
from ..config.config import Config
from ..distribution_generator.dgfactory import DGFactory
from ..fuzzer.fuzzer import Fuzzer
from ..transformer.resizetransformer import ResizeTransformer
from ..transformer.rotatetransformer import RotateTransformer
from ..utility.timer import timer
from ..video_generator.videogenerator import VideoGenerator


class TransformerTypes(IntEnum):
    RESIZE_TRANSFORMER = 0
    ROTATE_TRANSFORMER = 1


class CompositorTypes(IntEnum):
    GRID_COMPOSITOR = 0
    MOVING_COMPOSITOR = 1


class RandomizedFuzzer(Fuzzer):

    def __init__(self, config: Config, data=None):
        super().__init__(config, data)
        self.video_generator = VideoGenerator(self.config.media_root)
        self.name = "randomized_fuzzer"

    @timer
    def apply(self, data=None):

        quotient_cores = int(self.config.max_cores / self.config.video_copies)
        quotient_cores = 1 if quotient_cores <= 0 else quotient_cores
        self.config.pipeline_cores = min(self.config.max_cores, self.config.video_copies)

        new_data = []

        for i in range(self.config.video_copies):
            # Set object class
            total_object_types = self.video_generator.get_object_types()
            n_objects = random.randint(1, len(total_object_types) - 1)
            object_classes = random.sample(self.video_generator.get_object_types(), n_objects)
            object_class_distribution_input = {"type": "choice", "value": self.config.object_class_distribution["value"] or object_classes}
            object_class_distribution = DGFactory.get_distribution_generator(object_class_distribution_input)
            logging.info(f"Object class distribution type {object_class_distribution_input} used.")

            # Set time distribution
            time_dist_map = self.config.time_distribution or DGFactory.get_random_distribution(10)
            time_distribution = DGFactory.get_distribution_generator(time_dist_map)
            logging.info(f"Time distribution type {time_dist_map} used.")

            # Set object distribution
            obj_dist_map = self.config.object_distribution or DGFactory.get_random_distribution(16)
            object_distribution = DGFactory.get_distribution_generator(obj_dist_map)
            logging.info(f"Object distribution type {obj_dist_map} used.")

            # Set transformers
            transformer_list = self.config.data.get("transformers") or self.transformer_picker()
            transformer_generator = TransformerGenerator(self.config)
            transformers = transformer_generator.process(transformer_list)
            logging.info(f"Transformers of type {[str(tx) for tx in transformers]} picked.")

            # Set compositor
            compositor = self.config.data.get("compositor") or self.compositor_picker()
            logging.info(f"Compositor of type {str(compositor)} picked.")

            final_config = {
                "object_classes": object_class_distribution_input,
                "time_distribution": time_dist_map,
                "object_distribution": obj_dist_map,
                "transformers": transformer_list,
                "compositor": compositor,
                "model": self.config.model,
                "duration": self.config.duration,
                "step": self.config.step_size,
                "fps": self.config.fps,
                "frame_size_x": self.config.frame_size.first,
                "frame_size_y": self.config.frame_size.second
            }

            idx_str = data["idx"] + "_" if data is not None else ""

            obj = {
                "object_distribution": object_distribution,
                "time_distribution": time_distribution,
                "object_type_distribution": object_class_distribution,
                "filename": self.config.filename + "_" + idx_str + str(i),
                "max_tx_cores": quotient_cores,
                "compositor": compositor,
                "transformers": transformers,
                "use_cache": self.config.use_cache,
                "video_path": self.config.video_path,
                "final_config": final_config
            }

            logging.debug(f"Setting max tx cores as {quotient_cores}")

            new_data.append(obj)

        return new_data

    def validate(self, data):
        pass

    @classmethod
    def create_from_config(cls, config: Config, data):
        return RandomizedFuzzer(config, data)

    def transformer_picker(self):
        total_transformers = random.randint(1, len(TransformerTypes) - 1)
        picked_tx = random.sample([i for i in range(len(TransformerTypes))], total_transformers)

        tx = []
        # tx.append({"type": "rotate_transformer", "angle": -45})
        for i in picked_tx:
            if i == 0:
                tx.append(ResizeTransformer.get_random())
            elif i == 1:
                tx.append(RotateTransformer.get_random())
        return tx

    def compositor_picker(self):
        compositor_no = random.randint(0, len(CompositorTypes) - 1)

        if compositor_no == 0:
            return {"type": "grid_compositor"}
        elif compositor_no == 1:
            return {"type": "moving_compositor"}

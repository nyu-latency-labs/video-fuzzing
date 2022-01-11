from compositor.compositor import Compositor
from compositor.gridcompositor import GridCompositor
from compositor.movingcompositor import MovingCompositor
from fuzzer.experimentfuzzer import ExperimentFuzzer
from fuzzer.fuzzer import Fuzzer
from transformer.resizetransformer import ResizeTransformer
from transformer.rotatetransformer import RotateTransformer
from transformer.transformer import Transformer
from utils.singleton import Singleton


class ComponentProcessor(metaclass=Singleton):
    config = None

    def __init__(self, config):
        self.config = config

    def process_transformer(self, tx: dict) -> list[Transformer]:
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

    def process_fuzzer(self, fz: dict) -> Fuzzer:
        fz_type = fz["type"]

        tx = self.process_transformer(fz["transformers"])
        fz["transformers"] = tx

        if fz_type == "experiment_fuzzer":
            return ExperimentFuzzer.create_from_config(self.config, fz)
        else:
            return Fuzzer(self.config, fz)

    def process_compositor(self, cs: dict) -> Compositor:
        cs_type = cs["type"]

        if cs_type == "grid_compositor":
            return GridCompositor.create_from_config(self.config)
        elif cs_type == "moving_compositor":
            return MovingCompositor.create_from_config(self.config)
        else:
            return Compositor(self.config)

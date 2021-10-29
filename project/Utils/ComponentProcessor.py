from Compositor.Compositor import Compositor
from Compositor.GridCompositor import GridCompositor
from Compositor.MovingCompositor import MovingCompositor
from Fuzzer.ExperimentFuzzer import ExperimentFuzzer
from Fuzzer.Fuzzer import Fuzzer
from Transformer.ResizeTransformer import ResizeTransformer
from Transformer.RotateTransformer import RotateTransformer
from Transformer.Transformer import Transformer


class ComponentProcessor:
    config = None

    def __init__(self, config):
        self.config = config

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

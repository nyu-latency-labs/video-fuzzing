from typing import List

from ..component_generator.componentgenerator import ComponentGenerator
from ..transformer.resizetransformer import ResizeTransformer
from ..transformer.rotatetransformer import RotateTransformer
from ..transformer.transformer import Transformer


class TransformerGenerator(ComponentGenerator):

    def __init__(self, config):
        super().__init__(config)

    def process(self, tx: list) -> List[Transformer]:
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
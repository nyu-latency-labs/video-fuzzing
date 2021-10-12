import json
from random import random

from Fuzzer.ExperimentFuzzer import ExperimentFuzzer
from Fuzzer.Fuzzer import Fuzzer
from Transformer.ResizeTransformer import ResizeTransformer
from Transformer.RotateTransformer import RotateTransformer
from Transformer.Transformer import Transformer


def process_transformer(tx):
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


def process_fuzzer(fz):
    fz_type = fz["type"]
    transformers = process_transformer(fz["transformers"])

    if fz_type == "ExperimentFuzzer":
        return ExperimentFuzzer.create_from_config(transformers)
    else:
        return Fuzzer()


def process_distribution(ds):
    ds_type = ds["type"]

    if ds_type == "normal":
        return lambda: random.gauss(ds["mean"], ds["std"])
    elif ds_type == "linear":
        return lambda: ds_type["value"]


class Config:
    data = None

    # Fetch required properties and dump rest to a dictionary

    def __init__(self, filename):
        with open(filename) as f:
            self.data = json.load(f)

        self.object_classes = self.data["object_class"]
        self.object_distribution_fn = process_distribution(self.data["object_distribution"])
        self.time_distribution_fn = process_distribution(self.data["time_distribution"])
        self.transformers = process_transformer(self.data["transformers"])
        self.fuzzer = process_fuzzer(self.data["fuzzer"])

        self.duration = self.data["duration"]
        self.fps = self.data["fps"]
        self.step_size = self.data["step_size"]
        self.steps = self.duration / self.step_size
        self.media_root = self.data["media_root"]
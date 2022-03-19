from component_generator.componentgenerator import ComponentGenerator
from fuzzer.fuzzer import Fuzzer
from fuzzer.randomizedfuzzer import RandomizedFuzzer
from fuzzer.targetedfuzzer import TargetedFuzzer


class FuzzerGenerator(ComponentGenerator):

    def __init__(self, config):
        super().__init__(config)

    def process(self, fz: dict) -> Fuzzer:
        fz_type = fz["type"]

        fz["transformers"] = []

        if fz_type == "targeted_fuzzer":
            return TargetedFuzzer.create_from_config(self.config, fz)
        if fz_type == "randomized_fuzzer":
            return RandomizedFuzzer.create_from_config(self.config, fz)
        else:
            return Fuzzer(self.config, fz)

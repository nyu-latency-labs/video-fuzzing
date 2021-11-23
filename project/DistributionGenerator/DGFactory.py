from DistributionGenerator.RandomDG import RandomDistributionGenerator


class DGFactory:

    @classmethod
    def get_distribution_generator(cls, data):
        ds_type = data["type"]

        if ds_type == "normal":
            return RandomDistributionGenerator(data)
        elif ds_type == "linear":
            return RandomDistributionGenerator(data)
        elif ds_type == "choice":
            return RandomDistributionGenerator(data)

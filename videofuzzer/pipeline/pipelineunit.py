# Global interface for all pipeline elements
# All data is passed as a data object
from videofuzzer.utility.singleton import Singleton


class PipelineUnit:
    """
    Basic building block for all pipeline components
    """

    def apply(self, data: dict):
        """
        Process data as per the unit type.

        @param data: input data
        @return: resultant data
        """
        raise NotImplementedError("Apply method not implemented.")

    def validate(self, data: dict):
        """
        Validation function to ensure input contains all required data.

        @param data: input data
        @return: raise exception if validation fails, do nothing otherwise
        """
        raise NotImplementedError("Validate method not implemented.")

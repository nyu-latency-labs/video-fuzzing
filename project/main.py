import sys
from Pipeline.Pipeline import Pipeline
import logging

if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    file = sys.argv[1]
    pipeline = Pipeline()
    pipeline.apply(file)

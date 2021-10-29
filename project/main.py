import sys
import os
from Pipeline.Pipeline import Pipeline
import logging
import shutil

if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    file = sys.argv[1]

    os.makedirs("tmp/", exist_ok=True)
    pipeline = Pipeline()
    pipeline.apply(file)
    shutil.rmtree("tmp/")

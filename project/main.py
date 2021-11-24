import logging
import os
import shutil
import sys

from Pipeline.Pipeline import Pipeline

if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
    file = sys.argv[1]

    os.makedirs("tmp/", exist_ok=True)
    pipeline = Pipeline()
    pipeline.apply(file)
    shutil.rmtree("tmp/")

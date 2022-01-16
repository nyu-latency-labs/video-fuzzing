import logging
import os
import shutil
import sys

from pipeline.pipeline import Pipeline

if __name__ == "__main__":
    logging.basicConfig(format='[%(asctime)s] %(process)s %(filename)s:%(lineno)d %(levelname)s - %(message)s', level=logging.DEBUG)
    file = sys.argv[1]

    os.makedirs("tmp/", exist_ok=True)
    pipeline = Pipeline()
    pipeline.apply(file)
    shutil.rmtree("tmp/")

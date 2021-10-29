import logging
import multiprocessing
import uuid

from moviepy.video.VideoClip import ImageClip

from Utils.Timer import timer
from Transformer.Transformer import Transformer


def transformer_task(video, tx_list, out_list):
    clip = video.get_video()
    for tx in tx_list:
        clip = tx.apply(clip)

    tmp_name = "tmp/"
    if type(clip) is ImageClip:
        tmp_name = tmp_name + str(uuid.uuid4()) + ".jpg"
        clip.save_frame(tmp_name, 0)
        logging.debug("Saving ImageClip frame as jpg")
    else:
        tmp_name = tmp_name + str(uuid.uuid4()) + ".mp4"
        clip.write_videofile(tmp_name, 25, "mpeg4", audio=False, bitrate="1000k")
    video.filepath = tmp_name
    out_list.append(video)
    logging.debug("Updated video references")


class MultiTransformer(Transformer):
    angle = 0

    def __init__(self, data):
        super().__init__()
        self.name = "multi_transformer"

    @timer
    def apply(self, data):
        clips = data["clips"]
        transformers = data["transformers"]

        transformer_result = []
        with multiprocessing.Manager() as manager:
            pool = multiprocessing.Pool()
            logging.debug("Found %s cores", multiprocessing.cpu_count())

            multi_transformer_result = manager.list()
            for idx in range(len(clips)):
                video = data["clips"][idx]
                pool.apply_async(transformer_task, args=(video, transformers, multi_transformer_result))
            pool.close()
            pool.join()

            for res in multi_transformer_result:
                transformer_result.append(res.get_video())

        data["clips"] = transformer_result
        return data

    @classmethod
    def create_from_config(cls, data):
        return MultiTransformer(data)

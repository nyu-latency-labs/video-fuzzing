import logging
import multiprocessing
import uuid

from moviepy.video.VideoClip import ImageClip

from Utils.Timer import timer
from Transformer.Transformer import Transformer
from Caching.CacheItem import CacheItem
from Caching.VideoCache import VideoCache

video_cache = VideoCache()


def transformer_task(video, use_cache, tx_list, out_list):
    if use_cache:
        cache_item = video_cache.get_item(video.filepath, tx_list)

        if cache_item is not None:
            logging.debug("Serving item from cache")
            video.filepath = cache_item.processed_filename
            out_list.append(video)
            return

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

    if use_cache:
        cache_item = CacheItem(video.filepath, tx_list, tmp_name)
        video_cache.add_item(cache_item)

    video.filepath = tmp_name
    out_list.append(video)
    logging.debug("Updated video references")


class MultiTransformer(Transformer):

    def __init__(self, data):
        super().__init__(data)
        self.name = "multi_transformer"

    @timer
    def apply(self, data):
        clips = data["clips"]
        transformers = None
        for tx in data["transformers"]:
            if not tx["applied"]:
                transformers = tx

        if transformers is None:
            return data

        transformer_result = []
        with multiprocessing.Manager() as manager:
            pool = multiprocessing.Pool(processes=data["max_cores"])
            logging.debug("Using %s cores", data["max_cores"])

            multi_transformer_result = manager.list()
            for idx in range(len(clips)):
                video = data["clips"][idx]
                pool.apply_async(transformer_task, args=(video, data["use_cache"], transformers["transformers"],
                                                         multi_transformer_result))
            pool.close()
            pool.join()

            for res in multi_transformer_result:
                transformer_result.append(res)

        data["clips"] = transformer_result

        transformers["applied"] = True
        return data

    @classmethod
    def create_from_config(cls, data=None):
        return MultiTransformer(data)

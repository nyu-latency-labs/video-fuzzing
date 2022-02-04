import logging
import multiprocessing
import uuid
from typing import Optional

from moviepy.video.VideoClip import ImageClip

from caching.cacheitem import CacheItem
from caching.videocache import VideoCache
from transformer.transformer import Transformer
from utils.multiprocessinglog import logger_init, worker_init
from utils.timer import timer
from video_generator.video import Video

video_cache = VideoCache()


@timer
def transformer_task(video: Video, use_cache: bool, tx_list: list[Transformer], out_list: list[Video]):
    cache_item: Optional[CacheItem] = None

    if use_cache:
        cache_item = video_cache.get(video.filepath, tx_list)

    if cache_item is not None:
        logging.debug("Serving item from cache")
        video.filepath = cache_item.processed_filename
        out_list.append(video)
        return

    clip = video.get()
    for tx in tx_list:
        clip = tx.apply(clip)

    tmp_name = "tmp/"
    if type(clip) is ImageClip:
        tmp_name = tmp_name + str(uuid.uuid4()) + ".jpg"
        clip.save_frame(tmp_name, 0)
        logging.debug(f"Saving ImageClip frame as {tmp_name}")
    else:
        tmp_name = tmp_name + str(uuid.uuid4()) + ".mp4"
        clip.write_videofile(tmp_name, 25, "mpeg4", audio=False, bitrate="1000k")
        logging.debug(f"Saving VideoClip frame as {tmp_name}")

    if use_cache:
        cache_item = CacheItem(video.filepath, tx_list, tmp_name)
        video_cache.add(cache_item)

    video.filepath = tmp_name
    out_list.append(video)


class MultiTransformer(Transformer):

    def __init__(self, data):
        super().__init__(data)
        self.name = "multi_transformer"

    def __str__(self):
        return self.name + "_"

    @timer
    def apply(self, data: dict) -> dict:
        self.validate(data)

        clips = data["clips"]
        transformers = None
        for tx in data["transformers"]:
            if not tx["applied"]:
                transformers = tx
                break

        transformer_result = []
        logging.debug(f"Using {data['max_tx_cores']} cores")

        q_listener, q = logger_init()
        pool = multiprocessing.Pool(1, worker_init, [q])

        with multiprocessing.Manager() as manager:

            multi_transformer_result = manager.list()
            results = []
            for video in clips:
                results.append(pool.apply_async(transformer_task, args=(video, data["use_cache"],
                                                                        transformers["transformers"], multi_transformer_result)))
                # transformer_task(video, data["use_cache"], transformers["transformers"], multi_transformer_result)
            pool.close()

            # To allow propagation of exceptions from child processes, otherwise they get missed.
            for r in results:
                r.get()

            pool.join()

            for res in multi_transformer_result:
                transformer_result.append(res)

        # Ensure we aren't missing any clips due to some bug.
        assert(len(clips) == len(transformer_result))
        data["clips"] = transformer_result

        transformers["applied"] = True
        return data

    def validate(self, data: dict):
        if "clips" not in data or not data["clips"]:
            raise AssertionError("Clip list empty. Cannot transform")

        for tx in data["transformers"]:
            if not tx["applied"]:
                break
        else:
            raise AssertionError("No transformer left to apply.")

    @classmethod
    def create_from_config(cls, data=None):
        return MultiTransformer(data)

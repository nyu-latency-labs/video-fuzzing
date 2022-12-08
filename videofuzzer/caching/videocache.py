from typing import Optional
from typing import List, Dict

from caching.cacheitem import CacheItem
from transformer.transformer import Transformer
from utility.singleton import Singleton


class VideoCache(metaclass=Singleton):
    data: Dict[str, List[CacheItem]] = {}

    def add(self, item: CacheItem):
        if item.original_filename not in self.data.keys():
            self.data[item.original_filename] = [item]
        else:
            self.data[item.original_filename].append(item)

    def get(self, filename: str, transformers: List[Transformer]) -> Optional[CacheItem]:
        if filename not in self.data.keys():
            return None

        tx_set = set()
        for tx in transformers:
            tx_set.add(str(tx))

        result = list(filter(lambda x: x.attributes == tx_set, self.data[filename]))
        return result[0] if result else None

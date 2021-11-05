from VideoGenerator.CacheItem import CacheItem


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class VideoCache(metaclass=Singleton):

    data = {}

    def add_item(self, item: CacheItem):
        if item.original_filename not in self.data.keys():
            self.data[item.original_filename] = [item]
        else:
            self.data[item.original_filename].append(item)

    def get_item(self, filename, transformers) -> CacheItem:
        if filename not in self.data.keys():
            return None

        tx_set = set()
        for tx in transformers:
            tx_set.add(str(tx))

        for item in self.data[filename]:
            if item.attributes == tx_set:
                return item

        return None


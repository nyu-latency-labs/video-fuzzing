
class CacheItem:
    original_filename = None
    attributes = set()
    processed_filename = None

    def __init__(self, original_filename, transformers, processed_filename):
        self.original_filename = original_filename
        self.processed_filename = processed_filename
        for tx in transformers:
            self.attributes.add(str(tx))

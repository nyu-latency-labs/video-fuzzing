from transformer.transformer import Transformer


class CacheItem:
    original_filename: str = None
    attributes: set[str] = set()
    processed_filename: str = None

    def __init__(self, original_filename: str, transformers: list[Transformer], processed_filename: str):
        self.original_filename = original_filename
        self.processed_filename = processed_filename
        for tx in transformers:
            self.attributes.add(str(tx))

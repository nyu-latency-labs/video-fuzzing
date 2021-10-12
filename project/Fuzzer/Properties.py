
class Properties:
    data = {}

    def __init__(self, data={}):
        self.data = data

    def set_property(self, key, value):
        self.data[key] = value

    def get_property(self, key):
        return self.data[key]
from datetime import datetime

class Cache:
    """Simple Cache implementation.
    """

    def __init__(self):
        self.data = {}

    def _timestamp(self):
        return datetime.now().timestamp()

    def set(self, key, data, cache_time):
        self.data[key] = {}
        self.data[key]["data"] = data
        self.data[key]["timestamp"] = self._timestamp()
        self.data[key]["cache_time"] = cache_time

    def get(self, key):
        data = self.data.get(key, {})

        if not data:
            return None
        if (self._timestamp() - data["timestamp"]) > data["cache_time"]:
            return None

        return data["data"]

    def remove(self, key):
        self.data[key] = {}

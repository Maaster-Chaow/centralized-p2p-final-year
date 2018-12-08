from werkzeug.contrib.cache import SimpleCache


class HostCache(SimpleCache):
    def __init__(self, threshold=500, default_timeout=600):
        super().__init__(threshold, default_timeout)

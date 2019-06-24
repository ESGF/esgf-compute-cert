import time


class Timing(object):
    def __init__(self):
        self.start = None
        self.stop = None

    @property
    def elapsed(self):
        return self.stop - self.start

    def __enter__(self):
        self.start = time.time()

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop = time.time()

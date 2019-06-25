import time

import requests


def download(uri, output_path):
    res = requests.get(uri, stream=True)

    res.raise_for_status()

    with open(output_path, 'wb') as outfile:
        for chunk in res.iter_content(chunk_size=8192):
            outfile.write(chunk)


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

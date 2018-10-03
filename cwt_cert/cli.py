import logging
import multiprocessing

from cwt_cert import runner

logger = logging.getLogger('cwt_cert.cli')


class CLI(object):
    def __init__(self):
        pass

    def run(self, **kwargs):
        proc = multiprocessing.Process(target=runner.runner, kwargs=kwargs)

        proc.start()

        proc.join()

import logging
import sys

logger = logging.getLogger('cwt_cert.cli')


class CLI(object):
    def __init__(self):
        pass

    def setup_logging(self):
        logger.setLevel(logging.DEBUG)

        logger.addHandler(logging.StreamHandler(stream=sys.stdout))

    def run(self, **kwargs):
        self.setup_logging()

        logger.info('%r', kwargs)

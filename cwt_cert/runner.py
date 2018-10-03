import cStringIO
import logging
import multiprocessing
import sys

from cwt_cert import actions
from cwt_cert import validators

logger = logging.getLogger('cwt_cert.runner')

logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))


def build_node_tests():
    node = [
        {
            'name': 'Official ESGF Operators',
            'action_id': actions.HTTP_REQ_ACTION,
            'validator_ids': [
                validators.STATUS_CODE
            ],
            'args': [
                'GET',
                'https://192.168.39.34/wps/',
            ],
            'kwargs': {
                'verify': False,
            },
        }
    ]

    return node


class LogCapture(object):
    @property
    def value(self):
        return self.buffer.getvalue()

    def __enter__(self):
        self.buffer = cStringIO.StringIO()

        self.handler = logging.StreamHandler(self.buffer)

        formatter = logging.Formatter(
            '%(asctime)s [[%(module)s.%(funcName)s] %(levelname)s]: '
            '%(message)s')

        self.handler.setFormatter(formatter)

        self.logger = logging.getLogger()

        self.logger.addHandler(self.handler)

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.buffer.close()

        self.logger.removeHandler(self.handler)


def node_test_unpack(kwargs):
    return node_test(**kwargs)


def node_test(name, action_id, validator_ids, args=None, kwargs=None):
    if args is None:
        args = []

    if kwargs is None:
        kwargs = {}

    failed = False
    validation_result = []
    action = actions.REGISTRY[action_id]

    with LogCapture() as capture:
        act_result = action(*args, **kwargs)

        for val in [validators.REGISTRY[x] for x in validator_ids]:
            val_result = val(**act_result)

            validation_result.append(val_result)

        result = {
            'name': name,
            'action': action_id,
            'logs': capture.value,
        }

    if failed:
        result['failure'] = validation_result
    else:
        result['success'] = validation_result

    return result


def runner(**kwargs):
    node_tests = build_node_tests()

    pool = multiprocessing.Pool(5)

    it = pool.imap(node_test_unpack, node_tests)

    try:
        while True:
            result = it.next()

            logger.debug('Result %r', result)

            status = 'Success' if 'success' in result else 'Failure'

            logger.info('Test %r has completed with status %r', result['name'],
                        status)
    except StopIteration:
        pass
    finally:
        pool.close()

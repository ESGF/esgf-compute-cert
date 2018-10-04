import cStringIO
import json
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
            'action': actions.HTTP_REQ_ACTION,
            'validations': [
                {
                    'type': validators.WPS_CAPABILITIES,
                    'kwargs': {
                        'operations': [
                            '.*\.idontexist',
                            '.*\.aggregate',
                            '.*\.average',
                            '.*\.max',
                            '.*\.metrics',
                            '.*\.min',
                            '.*\.regrid',
                            '.*\.subset',
                            '.*\.sum',
                        ]
                    }
                },
            ],
            'args': [
                'GET',
                'https://192.168.39.34/wps/',
            ],
            'kwargs': {
                'verify': False,
                'params': {
                    'service': 'WPS',
                    'request': 'GetCapabilities',
                }
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


def node_test(name, action, validations, args=None, kwargs=None):
    if args is None:
        args = []

    if kwargs is None:
        kwargs = {}

    failed = False
    validation_result = []
    act = actions.REGISTRY[action]

    with LogCapture() as capture:
        act_result = act(*args, **kwargs)

        act_snapshot = {
            'args': args,
            'kwargs': kwargs,
            'result': act_result,
        }

        for x in validations:
            type_id = x['type']

            val = validators.REGISTRY[type_id]

            val_result = val(act_snapshot, **x.get('kwargs', {}))

            if val_result['validation_result'] == validators.FAILURE:
                failed = True

            validation_result.append(val_result)

        result = {
            'name': name,
            'action': action,
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

            logger.info('%s', json.dumps(result, indent=2))
    except StopIteration:
        pass
    finally:
        pool.close()

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
            'actions': [
                {
                    'type': actions.WPS_CAPABILITIES,
                    'args': [
                        'https://192.168.39.34/wps/',
                    ],
                    'validations': [
                        {
                            'type': validators.WPS_CAPABILITIES,
                            'kwargs': {
                                'operations': [
                                    '.*\.aggregates',
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
                    ]
                },
            ]
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


def run_action(type, args=None, kwargs=None, **extra):
    if args is None:
        args = []

    if kwargs is None:
        kwargs = {}

    action = actions.REGISTRY[type]

    result = action(*args, **kwargs)

    return result


def run_validation(output, type, args=None, kwargs=None, **extra):
    if args is None:
        args = []

    if kwargs is None:
        kwargs = {}

    validator = validators.REGISTRY[type]

    result = validator(output, *args, **kwargs)

    return result


def node_test(name, actions):
    with LogCapture() as capture:
        results = {'name': name, 'actions': []}

        test_status = validators.SUCCESS

        for act in actions:
            act_result = run_action(**act)

            # act['result'] = act_result

            act_status = validators.SUCCESS

            for val in act.get('validations'):
                val_result = run_validation(act_result, **val)

                val['result'] = val_result

                if val_result['status'] == validators.FAILURE:
                    act_status = validators.FAILURE

            if act_status == validators.FAILURE:
                test_status = validators.FAILURE

            act['status'] = act_status

            results['actions'].append(act)

        results['status'] = test_status

        results['log'] = capture.value

    return results


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

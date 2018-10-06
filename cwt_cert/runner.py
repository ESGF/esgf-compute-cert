import cStringIO
import json
import logging
import multiprocessing
import sys

import cwt
from cwt_cert import actions
from cwt_cert import validators

logger = logging.getLogger('cwt_cert.runner')

logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))


def default(x):
    if isinstance(x, cwt.Variable):
        data = x.parameterize()

        data['_type'] = 'variable'
    elif isinstance(x, cwt.Domain):
        data = x.parameterize()

        data['_type'] = 'domain'
    else:
        raise TypeError(type(x))

    return data


def object_hook(x):
    if '_type' in x:
        type = x.pop('_type')

        if type == 'variable':
            x = cwt.Variable.from_dict(x)
        elif type == 'domain':
            x = cwt.Domain.from_dict(x)

    return x


def json_encoder(x, **kwargs):
    return json.dumps(x, default=default, **kwargs)


def json_decoder(x):
    return json.loads(x, object_hook=object_hook)


def build_operator_tests(url, **kwargs):
    operator = [
        {
            'name': 'Operator aggregate',
            'actions': [
                {
                    'type': actions.WPS_EXECUTE,
                    'args': [
                        url,
                    ],
                    'kwargs': {
                        'inputs': [
                            cwt.Variable('https://dataserver.nccs.nasa.gov/thredds/dodsC/CMIP5/NASA/GISS/historical/E2-H_historical_r2i1p3/ccb_Amon_GISS-E2-H_historical_r2i1p3_185001-190012.nc',  # noqa E501
                                         'ccb'),
                            cwt.Variable('https://dataserver.nccs.nasa.gov/thredds/dodsC/CMIP5/NASA/GISS/historical/E2-H_historical_r2i1p3/ccb_Amon_GISS-E2-H_historical_r2i1p3_190101-195012.nc',  # noqa E501
                                         'ccb'),
                            cwt.Variable('https://dataserver.nccs.nasa.gov/thredds/dodsC/CMIP5/NASA/GISS/historical/E2-H_historical_r2i1p3/ccb_Amon_GISS-E2-H_historical_r2i1p3_195101-200512.nc',  # noqa E501
                                         'ccb'),
                        ],
                        'identifier': '.*\.aggregate',
                        'variable': 'ccb',
                    },
                    'validations': [
                        {
                            'type': validators.CHECK_VARIABLE,
                            'kwargs': {
                                'var_name': 'ccb',
                            }
                        },
                        {
                            'type': validators.CHECK_SHAPE,
                            'kwargs': {
                                'var_name': 'ccb',
                                'shape': (1869, 90, 144),
                            },
                        },
                    ],
                },
            ],
        }
    ]

    return operator


def build_node_tests(url, **kwargs):
    node = [
        {
            'name': 'Official ESGF Operators',
            'actions': [
                {
                    'type': actions.WPS_CAPABILITIES,
                    'args': [
                        url,
                    ],
                    'validations': [
                        {
                            'type': validators.WPS_CAPABILITIES,
                            'kwargs': {
                                'operations': [
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
    pool = multiprocessing.Pool(5)

    operator_tests = build_operator_tests(**kwargs)

    for test in operator_tests:
        result = node_test(**test)

        print json_encoder(result, indent=2)

    # node_tests = build_node_tests()

    # pool = multiprocessing.Pool(5)

    # result = pool.map_async(node_test_unpack, node_tests)

    # data = result.get()

    # logger.info('%s', json.dumps(data, indent=2))

    pool.close()

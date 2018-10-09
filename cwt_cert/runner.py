import cStringIO
import json
import logging
import multiprocessing

import cwt
from cwt_cert import actions
from cwt_cert import validators

logger = logging.getLogger('cwt_cert.runner')


class CertificationError(Exception):
    pass


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


def json_encoder_to_file(x, fp, **kwargs):
    return json.dump(x, fp, default=default, **kwargs)


def json_encoder(x, **kwargs):
    return json.dumps(x, default=default, **kwargs)


def json_decoder(x):
    return json.loads(x, object_hook=object_hook)


def build_operator_tests(url, api_key, **kwargs):
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
                            cwt.Variable('http://aims3.llnl.gov/thredds/dodsC/cmip5_css02_data/cmip5/output1/CMCC/CMCC-CM/decadal2005/mon/atmos/Amon/r1i2p1/cct/1/cct_Amon_CMCC-CM_decadal2005_r1i2p1_200511-201512.nc',
                                         'cct'),
                            cwt.Variable('http://aims3.llnl.gov/thredds/dodsC/cmip5_css02_data/cmip5/output1/CMCC/CMCC-CM/decadal2005/mon/atmos/Amon/r1i2p1/cct/1/cct_Amon_CMCC-CM_decadal2005_r1i2p1_201601-202512.nc',
                                         'cct'),
                            cwt.Variable('http://aims3.llnl.gov/thredds/dodsC/cmip5_css02_data/cmip5/output1/CMCC/CMCC-CM/decadal2005/mon/atmos/Amon/r1i2p1/cct/1/cct_Amon_CMCC-CM_decadal2005_r1i2p1_202601-203512.nc',
                                         'cct'),
                        ],
                        'identifier': '.*\.aggregate',
                        'variable': 'ccb',
                        'api_key': api_key,
                    },
                    'validations': [
                        {
                            'type': validators.CHECK_SHAPE,
                            'kwargs': {
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


def run_action(type, args=None, kwargs=None, **extra):
    if args is None:
        args = []

    if kwargs is None:
        kwargs = {}

    try:
        action = actions.REGISTRY[type]
    except KeyError:
        raise CertificationError('Missing action {!r}'.format(type))

    result = action(*args, **kwargs)

    return result


def run_validation(output, type, args=None, kwargs=None, **extra):
    if args is None:
        args = []

    if kwargs is None:
        kwargs = {}

    try:
        validator = validators.REGISTRY[type]
    except KeyError:
        raise CertificationError('Missing validator {!r}'.format(type))

    result = validator(output, *args, **kwargs)

    return result


def run_validations(output, validations, **kwargs):
    status = validators.SUCCESS

    for item in validations:
        try:
            result = run_validation(output, **item)
        except Exception as e:
            item['message'] = str(e)

            item['status'] = validators.FAILURE
        else:
            item['message'] = result

            item['status'] = validators.SUCCESS

        if item['status'] == validators.FAILURE:
            status = item['status']

    return status


def run_test(name, actions):
    with LogCapture() as capture:
        result = {'name': name, 'actions': []}

        status = validators.SUCCESS

        for item in actions:
            action_status = validators.SUCCESS

            try:
                action_result = run_action(**item)
            except Exception as e:
                item['message'] = str(e)

                action_status = validators.FAILURE
            else:
                action_status = run_validations(action_result, **item)

            item['status'] = action_status

            result['actions'].append(item)

            if action_status == validators.FAILURE:
                status = action_status

        result['status'] = status

        result['log'] = capture.value

    return result


def run_test_unpack(kwargs):
    return run_test(**kwargs)


def runner(**kwargs):
    results = {'node': [], 'operator': []}

    pool = multiprocessing.Pool(5)

    node_tests = build_node_tests(**kwargs)

    async_result = pool.map_async(run_test_unpack, node_tests)

    data = async_result.get(120)

    results['node'] = data

    operator_tests = build_operator_tests(**kwargs)

    for test in operator_tests:
        test_result = pool.map(run_test_unpack, [test])

        results['operator'].append(test_result)

    pool.close()

    if kwargs['output'] is not None:
        with open(kwargs['output'], 'w') as outfile:
            json_encoder_to_file(results, outfile, indent=2)

    return results

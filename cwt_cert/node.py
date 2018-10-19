import logging

import cwt

from cwt_cert import actions
from cwt_cert import validators


def build_node_tests(url, api_key, **kwargs):
    node = [
        {
            'cli_kwargs': kwargs,
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
                            'name': 'Check GetCapabilities',
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
            ],
        },
        {
            'cli_kwargs': kwargs,
            'name': 'Official Dataset',
            'actions': [
                {
                    'type': actions.WPS_EXECUTE_UNTIL_SUCCESS,
                    'args': [
                        url,
                    ],
                    'kwargs': {
                        'identifier': '.*\.subset',
                        'api_key': api_key,
                        'inputs': [
                            cwt.Variable('https://dataserver.nccs.nasa.gov/thredds/dodsC/CMIP5/NASA/GISS/historical/E2-H_historical_r2i1p3/ccb_Amon_GISS-E2-H_historical_r2i1p3_185001-190012.nc',
                                         'ccb'),
                        ],
                    },
                    'validations': [
                        {
                            'type': validators.CHECK_IS_NOT_NONE,
                            'name': 'Check Dataset access',
                        }
                    ],
                }
            ],
        },
        {
            'cli_kwargs': kwargs,
            'name': 'Metrics',
            'actions': [
                {
                    'type': actions.WPS_EXECUTE,
                    'args': [
                        url,
                    ],
                    'kwargs': {
                        'identifier': '.*\.metrics',
                        'api_key': api_key,
                    },
                    'validations': [
                        {
                            'type': validators.CHECK_METRICS,
                            'name': 'Check Metrics',
                        }
                    ],
                }
            ],
        },
    ]

    return node


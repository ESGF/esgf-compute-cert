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
        #{
        #    'name': 'Official Dataset',
        #    'actions': [
        #    ],
        #},
        #{
        #    'cli_kwargs': kwargs,
        #    'name': 'Metrics',
        #    'actions': [
        #        {
        #            'type': actions.WPS_EXECUTE,
        #            'args': [
        #                url,
        #            ],
        #            'kwargs': {
        #                'identifier': '.*\.metrics',
        #                'api_key': api_key,
        #            },
        #        }
        #    ],
        #},
    ]

    return node


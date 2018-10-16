import cwt

from cwt_cert import actions
from cwt_cert import validators


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
            ],
        },
        {
            'name': 'Official Dataset',
            'actions': [
            ],
        },
        {
            'name': 'Security',
            'actions': [
            ],
        },
        {
            'name': 'Metrics',
            'actions': [
            ],
        },
    ]

    return node


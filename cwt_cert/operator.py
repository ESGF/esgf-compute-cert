import cwt

from cwt_cert import actions
from cwt_cert import validators


def build_operator_tests(url, api_key, **kwargs):
    operator = [
        {
            'name': 'Operator aggregate',
            'actions': [
                {
                    'name': 'Performance',
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

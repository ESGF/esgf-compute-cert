import cwt

from cwt_cert import actions
from cwt_cert import validators


def build_operator_tests(url, api_key, **kwargs):
    operator = [
        {
            'name': 'Aggregate',
            'actions': [
                {
                    'type': actions.WPS_EXECUTE,
                    'args': [
                        url,
                    ],
                    'kwargs': {
                        'inputs': [
                            cwt.Variable('https://dataserver.nccs.nasa.gov/thredds/dodsC/CMIP5/NASA/GISS/historical/E2-H_historical_r2i1p3/ccb_Amon_GISS-E2-H_historical_r2i1p3_185001-190012.nc',
                                         'ccb'),
                            cwt.Variable('https://dataserver.nccs.nasa.gov/thredds/dodsC/CMIP5/NASA/GISS/historical/E2-H_historical_r2i1p3/ccb_Amon_GISS-E2-H_historical_r2i1p3_190101-195012.nc',
                                         'ccb'),
                            cwt.Variable('https://dataserver.nccs.nasa.gov/thredds/dodsC/CMIP5/NASA/GISS/historical/E2-H_historical_r2i1p3/ccb_Amon_GISS-E2-H_historical_r2i1p3_195101-200512.nc',
                                         'ccb'),
                        ],
                        'identifier': '.*\.aggregate',
                        'variable': 'ccb',
                        'api_key': api_key,
                    },
                    'validations': [
                        {
                            'name': 'API Compliant',
                        },
                        {
                            'name': 'Performance',
                            'type': validators.CHECK_SHAPE,
                            'kwargs': {
                                'shape': (1872, 90, 144),
                            },
                        },
                        {
                            'name': 'Provenance',
                        }
                    ],
                },
                {
                    'name': 'Stress',
                    'validations': [],
                },
            ],
        }
    ]

    return operator

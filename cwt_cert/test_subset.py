#! /usr/bin/env python

from process_base import ProcessBase

class TestSubset(ProcessBase):
    identifier = 'subset'

    performance = {
        'variable': 'ta',
        'files': [
            'https://aims3.llnl.gov/thredds/dodsC/cmip3_data/data2/20c3m/atm/mo/ta/ipsl_cm4/run1/ta_A1_1860-2000.nc',
        ],
        'domain': {
            'lat': (-45, 45),
            'lon': (0, 180),
            'time': (10000, 11000),
            'plev': (40000, 20000),
        },
        'validations': {
            'shape': (34, 4, 36, 49)
        }
    }

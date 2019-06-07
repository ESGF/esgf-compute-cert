#! /usr/bin/env python

from __future__ import absolute_import
import pytest

from cwt_cert import test_base


@pytest.mark.subset
class TestSubset(test_base.TestBase):
    identifier = 'subset'

    api_compliance = [
        {
            'variable': 'ta',
            'files': [
                test_base.TA[0],
            ],
            'domain': {
                'time': slice(50, 100),
            },
            'validations': {
                'shape': (50, 19, 90, 144)
            }
        },
        {
            'variable': 'ta',
            'files': [
                test_base.TA[0],
            ],
            'domain': {
                'time': (2144.0, 3116.5),
            },
            'validations': {
                'shape': (32, 19, 90, 144)
            }
        },
        {
            'variable': 'ta',
            'files': [
                test_base.TA[0],
            ],
            'domain': {
                'time': ('1854-1-16 12:0:0.0', '1854-12-16 12:0:0.0'),
            },
            'validations': {
                'shape': (12, 19, 90, 144)
            }
        },
    ]

    performance = {
        'variable': 'ta',
        'files': [
            test_base.TA[0],
        ],
        'domain': {
            'lat': (-45, 45),
            'lon': (0, 180),
            'time': (10000, 11000),
            'plev': (40000, 20000),
        },
        'validations': {
            'shape': (33, 4, 46, 72)
        }
    }

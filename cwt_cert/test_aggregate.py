#! /usr/bin/env python

from __future__ import absolute_import
import pytest

from cwt_cert import test_base


@pytest.mark.aggregate
class TestAggregate(test_base.TestBase):
    identifier = 'aggregate'

    api_compliance = [
        {
            'variable': 'ta',
            'files': test_base.TA[:2],
            'domain': {
                'time': slice(300, 912),
            },
            'validations': {
                'shape': (612, 19, 90, 144)
            }
        },
        {
            'variable': 'ta',
            'files': test_base.TA[:2],
            'domain': {
                'time': (2144.0, 25838.5),
            },
            'validations': {
                'shape': (779, 19, 90, 144)
            }
        },
        {
            'variable': 'ta',
            'files': test_base.TA[:2],
            'domain': {
                'time': ('1854-1-16 12:0:0.0', '1910-12-16 12:0:0.0'),
            },
            'validations': {
                'shape': (684, 19, 90, 144)
            }
        },
    ]

    performance = {
        'variable': 'clt',
        'files': test_base.CLT,
        'domain': None,
        'validations': {
            'shape': (1812, 90, 144),
        }
    }

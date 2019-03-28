#! /usr/bin/env python

from __future__ import absolute_import
import pytest

from . import process_base

@pytest.mark.subset
class TestSubset(process_base.ProcessBase):
    identifier = '.*\.subset'

    performance = {
        'variable': 'ta',
        'files': [
            process_base.TA[0],
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

    stress = {
        'variable': 'ta',
        'files': [
            process_base.TA[0],
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

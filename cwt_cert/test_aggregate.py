#! /usr/bin/env python

import pytest

import process_base

@pytest.mark.aggregate
class TestAggregate(process_base.ProcessBase):
    identifier = '.*\.aggregate'

    performance = {
        'variable': 'clt',
        'files': process_base.CLT,
        'domain': None,
        'validations': {
            'shape': (1980, 90, 144),
        }
    }
    
    stress = {
        'variable': 'ta',
        'files': process_base.TA,
        'domain': None,
        'validations': {
            'shape': (1980, 19, 90, 144),
        }
    }

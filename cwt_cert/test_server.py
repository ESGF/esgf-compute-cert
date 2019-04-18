from __future__ import absolute_import
import cwt
import pytest
from jsonschema import validate

from . import metrics_schema
from . import process_base

@pytest.mark.stress
@pytest.mark.server
def test_stress(context, request):
    tests = [
        {
            'identifier': '.*\\.subset',
            'variable': 'clt',
            'files': process_base.CLT[0:1],
            'domain': {
                'time': (1000, 10000),
                'lat': (-45, 45),
                'lon': (0, 180),
            },
            'validations': {
                'shape': (296, 46, 72),
            },
        },
        {
            'identifier': '.*\\.subset',
            'variable': 'ta',
            'files': process_base.TA[0:1],
            'domain': {
                'time': (1000, 10000),
                'lat': (-45, 45),
                'lon': (0, 180),
                'plev': (50000, 10000),
            },
            'validations': {
                'shape': (296, 7, 46, 72),
            },
        },
        {
            'identifier': '.*\\.aggregate',
            'variable': 'tas',
            'files': process_base.TAS,
            'domain': None,
            'validations': {
                'shape': (1980, 90, 144),
            },
        },
        {
            'identifier': '.*\\.aggregate',
            'variable': 'clt',
            'files': process_base.CLT,
            'domain': None,
            'validations': {
                'shape': (1812, 90, 144),
            },
        },
    ]

    base = process_base.ProcessBase()
    
    client = context.get_client_token()

    for item in tests:
        process = base.execute(context, request, client, **item)

        item['process'] = process

    for item in tests:
        assert item['process'].wait(20*60)

        base.run_validations(item['process'].output, item['validations'])

@pytest.mark.api_compliance
@pytest.mark.server
def test_api_compliance(context, request):
    tests = [
        {
            'identifier': '.*\\.subset',
            'variable': 'clt',
            'files': process_base.CLT[0:1],
            'domain': {
                'time': slice(0, 100),
            },
            'validations': {
                'shape': (100, 90, 144),
            }
        },
        {
            'identifier': '.*\\.subset',
            'variable': 'clt',
            'files': process_base.CLT[0:1],
            'domain': {
                'time': (0, 100),
            },
            'validations': {
                'shape': (3, 90, 144),
            }
        },
        {
            'identifier': '.*\\.subset',
            'variable': 'clt',
            'files': process_base.CLT[0:1],
            'domain': {
                'time': ('1900-1-16 12:0:0.0', '1900-12-16 12:0:0.0'),
            },
            'validations': {
                'shape': (12, 90, 144),
            }
        },
    ]

    base = process_base.ProcessBase()
    
    client = context.get_client_token()

    for item in tests:
        process = base.execute(context, request, client, **item)

        assert process.wait(20*60)

        base.run_validations(process.output, item['validations'])

@pytest.mark.metrics
@pytest.mark.server
def test_metrics(context):
    client = context.get_client_token()

    process = client.processes('.*\\.metrics')[0]

    client.execute(process)

    assert process.wait()

    validate(instance=process.output, schema=metrics_schema.schema)

@pytest.mark.security
@pytest.mark.server
def test_security(context):
    # Check SSL
    # Check execute is protected
    # ?

    client = context.get_client()

    process = client.processes('.*\\.metrics')[0]

    # Expect an error to be raised no token provided
    with pytest.raises(cwt.WPSClientError):
        client.execute(process)

@pytest.mark.operators
@pytest.mark.server
def test_official_operators(context):
    client = context.get_client()

    expected = set(['aggregate', 'subset', 'metrics'])

    for method in expected:
        process = client.processes('.*\\.{!s}'.format(method))

        assert len(process) > 0

        assert method in process[0].identifier

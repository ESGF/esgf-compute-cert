from __future__ import absolute_import
import cwt
import pytest
from jsonschema import validate

from cwt_cert import metrics_schema
from cwt_cert import test_base


@pytest.mark.stress
@pytest.mark.server
def test_stress(context, request):
    tests = [
        {
            'identifier': 'subset',
            'variable': 'clt',
            'files': test_base.CLT[0:1],
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
            'identifier': 'subset',
            'variable': 'ta',
            'files': test_base.TA[0:1],
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
            'identifier': 'aggregate',
            'variable': 'tas',
            'files': test_base.TAS,
            'domain': None,
            'validations': {
                'shape': (1980, 90, 144),
            },
        },
        {
            'identifier': 'aggregate',
            'variable': 'clt',
            'files': test_base.CLT,
            'domain': None,
            'validations': {
                'shape': (1812, 90, 144),
            },
        },
    ]

    base = test_base.TestBase()

    client = context.get_client_token()

    for item in tests:
        process = base.execute(context, request, client, **item)

        item['process'] = process

    for item in tests:
        assert item['process'].wait(20*60)

        base.run_validations(item['process'].output, item['validations'])


@pytest.mark.metrics
@pytest.mark.server
def test_metrics(context):
    client = context.get_client_token()

    process = client.process_by_name(context.metrics_identifier)

    assert process is not None, 'Missing metrics operation'

    client.execute(process)

    assert process.wait()

    validate(instance=process.output, schema=metrics_schema.schema)


@pytest.mark.security
@pytest.mark.server
def test_security(context):
    client = context.get_client()

    process = client.process_by_name(context.metrics_identifier)

    assert process is not None, 'Missing metrics operation'

    # Expect an error to be raised no token provided
    with pytest.raises(cwt.WPSClientError):
        client.execute(process)


@pytest.mark.operators
@pytest.mark.server
def test_official_operators(context):
    client = context.get_client()

    found = set()
    expected = set([
        context.format_identifier('subset'),
        context.format_identifier('aggregate'),
        context.metrics_identifier,
    ])

    for identifier in expected:
        process = client.process_by_name(identifier)

        if process is not None:
            found.add(process.identifier)

    assert found == expected, 'Missing expected operations'

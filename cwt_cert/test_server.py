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
            'name': 'stress-subset-1',
            'identifier': 'subset',
            'variable': 'clt',
            'files': [
                test_base.CLT[0]
            ],
            'domain': {
                'time': (1000, 10000),
                'lat': (-45, 45),
                'lon': (0, 180),
            },
            'validations': [
                test_base.validate_axes,
            ]
        },
        {
            'name': 'stress-subset-2',
            'identifier': 'subset',
            'variable': 'ta',
            'files': [
                test_base.TA[0]
            ],
            'domain': {
                'time': (1000, 10000),
                'lat': (-45, 45),
                'lon': (0, 180),
                'plev': (50000, 10000),
            },
            'validations': [
                test_base.validate_axes,
            ]
        },
        {
            'name': 'stress-aggregate-1',
            'identifier': 'aggregate',
            'variable': 'tas',
            'files': test_base.TAS,
            'domain': None,
            'validations': [
                test_base.validate_axes,
            ]
        },
        {
            'name': 'stress-aggregate-2',
            'identifier': 'aggregate',
            'variable': 'clt',
            'files': test_base.CLT,
            'domain': None,
            'validations': [
                test_base.validate_axes,
            ]
        },
    ]

    base = test_base.TestBase()

    client = context.get_client_token()

    for item in tests:
        process = base.execute(context, request, client, **item)

        item['process'] = process

    for item in tests:
        base.validate(context, request, item['process'], item['name'], item['files'], item['variable'], item['domain'],
                      item['validations'])


@pytest.mark.metrics
@pytest.mark.server
def test_metrics(context, request):
    client = context.get_client_token()

    process = client.process_by_name(context.metrics_identifier)

    assert process is not None, 'Missing metrics operation'

    client.execute(process)

    with test_base.Timing() as timing:
        assert process.wait()

    context.set_extra(request, 'timing', 'metrics', timing.elapsed)

    validate(instance=process.output, schema=metrics_schema.schema)

    context.set_extra(request, 'output', 'metrics', process.output)


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
def test_official_operators(context, request):
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

    context.set_extra(request, 'operators', 'verified', list(found))

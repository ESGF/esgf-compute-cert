from __future__ import absolute_import

import cwt
import pytest
from jsonschema import validate

from cwt_cert import metrics_schema
from cwt_cert import utils


@pytest.mark.stress
@pytest.mark.server
def test_stress(context, request):
    client = context.get_client_token()

    try:
        config = context.test_config['stress']
    except KeyError as e:
        raise Exception('Missing configuration key {!r} in performance'.format(e))

    processing = {}

    for test in config:
        var_name = test['variable']

        inputs = [cwt.Variable(x, var_name) for x in test['inputs']]

        process = client.process_by_name('{!s}.{!s}'.format(context.module, test['op']))

        params = test.get('parameters', {})

        domain = params.pop('domain', None)

        client.execute(process, inputs, **params)

        processing[var_name] = process

        variable, domain, operation = client.prepare_data_inputs(process, inputs, domain, **params)

        data_inputs = {
            'variable': variable,
            'domain': domain,
            'operation': operation,
        }

        context.set_extra(request, 'data_inputs', var_name, data_inputs)

    for var_name, process in processing.items():
        with utils.Timing() as timing:
            assert process.wait(20 * 60)

        context.set_extra(request, 'timing', var_name, timing.elapsed)


@pytest.mark.metrics
@pytest.mark.server
def test_metrics(context, request):
    client = context.get_client_token()

    process = client.process_by_name('{!s}.metrics'.format(context.module))

    assert process is not None, 'Missing metrics operation'

    client.execute(process)

    with utils.Timing() as timing:
        assert process.wait()

    context.set_extra(request, 'timing', 'metrics', timing.elapsed)

    validate(instance=process.output, schema=metrics_schema.schema)

    context.set_extra(request, 'output', 'metrics', process.output)


@pytest.mark.security
@pytest.mark.server
def test_security(context):
    client = context.get_client()

    process = client.process_by_name('{!s}.metrics'.format(context.module))

    assert process is not None, 'Missing metrics operation'

    # Expect an error to be raised no token provided
    with pytest.raises(cwt.WPSClientError):
        client.execute(process)


@pytest.mark.official_operator
@pytest.mark.server
def test_official_operators(context, request):
    client = context.get_client()

    expected_values = ['{!s}.{!s}'.format(context.module, x) for x in context.test_config['operators'].keys()]

    expected_values.append('{!s}.metrics'.format(context.module))

    found = set()
    expected = set(expected_values)

    for identifier in expected:
        process = client.process_by_name(identifier)

        if process is not None:
            found.add(process.identifier)

    assert found == expected, 'Missing expected operations'

    context.set_extra(request, 'operators', 'verified', list(found))

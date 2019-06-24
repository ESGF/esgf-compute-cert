import cwt
import pytest

from cwt_cert import utils


@pytest.mark.performance
def test_performance(context, request, module, op, version):
    try:
        config = context.test_config['performance'][op]
    except KeyError as e:
        raise Exception('Missing configuration key {!r} in performance'.format(e))

    inputs = [cwt.Variable(x, config['variable']) for x in config['inputs']]

    params = config.get('parameters', {})

    client = context.get_client_token()

    identifier = '{!s}.{!s}'.format(module, op)

    process = client.process_by_name(identifier)

    client.execute(process, inputs, **params)

    with utils.Timing() as timing:
        assert process.wait(20 * 60)

    context.set_extra(request, 'timing', op, timing.elapsed)


@pytest.mark.api_compliance
def test_api_compliance(context, request, module, op, version):
    try:
        config = context.test_config['api_compliance'][op]
    except KeyError as e:
        raise Exception('Missing configuration key {!r} in api_compliance'.format(e))

    inputs = [cwt.Variable(x, config['variable']) for x in config['inputs']]

    params = config.get('parameters', {})

    client = config.get_client_token()

    identifier = '{!s}.{!s}'.format(module, op)

    process = client.process_by_name(identifier)

    client.execute(process, inputs, **params)

    with utils.Timing() as timing:
        assert process.wait(20 * 60)

    context.set_extra(request, 'timing', op, timing.elapsed)

import os

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

    identifier = '{!s}.{!s}'.format(module, op)

    for test in config:
        inputs = [cwt.Variable(x, test['variable']) for x in test['inputs']]

        params = test.get('parameters', {})

        client = context.get_client_token()

        process = client.process_by_name(identifier)

        client.execute(process, inputs, **params)

        with utils.Timing() as timing:
            assert process.wait(20 * 60)

        name = test.get('name', op)

        context.set_extra(request, 'timing', name, timing.elapsed)

        if context.output_dir is not None:
            output_filename = '{!s}-{!s}-{!s}'.format(identifier, version, name)

            output_path = os.path.join(context.output_dir, output_filename)

            utils.download(process.output.uri.replace('dodsC', 'fileServer'), output_path)

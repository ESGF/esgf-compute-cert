import copy
import logging
import re
from functools import partial

import cwt

logger = logging.getLogger('cwt_cert.validators')
logger.setLevel(logging.DEBUG)

WPS_CAPABILITIES = 'wps_capabilities'
CHECK_SHAPE = 'check_shape'

SUCCESS = 'success'
FAILURE = 'failure'


def format_result(message, extra=None, status=None, *args):
    result = {
        'status': status,
        'message': message.format(args),
    }

    if extra is not None:
        result['extra'] = extra

    return result


format_success = partial(format_result, status=SUCCESS)


format_failure = partial(format_result, status=FAILURE)


def check_shape(output, shape):
    try:
        f = cdms2.open(output.uri)

        try:
            var_shape = f[output.var_name].shape
        except AttributeError:
            return format_failure('Variable {!r} was not found in {!r}',
                                  output.var_name, output.uri)

        if var_shape != shape:
            return format_failure('Outputs shape {!r} does not match the'
                                  'expected shape {!r}', var_shape, shape)
    except cdms2.CDMSError as e:
        return format_failure('Failed to open {!r}', output.uri)
    finally:
        f.close()

    return format_success('Verified variable {!r} shape is {!r}',
                          output.var_name, shape)

def check_wps_capabilities(output, operations):
    if not isinstance(output, cwt.CapabilitiesWrapper):
        msg = 'Expecting type {!r} got {!r}'.format(cwt.CapabilitiesWrapper,
                                                    type(output))

        return format_failure(msg)

    identifiers = [x.identifier for x in output.processes]

    missing_ops = copy.deepcopy(operations)

    for x in identifiers:
        for y in missing_ops:
            if re.match(y, x) is not None:
                break

        missing_ops.remove(y)

    if len(missing_ops) > 0:
        missing = ', '.join(missing_ops)

        msg = 'Missing operations matching {!r}'.format(missing)

        extra = {
            'operations': identifiers,
        }

        return format_failure(msg, extra=extra)

    return format_success('Successfully identifier all required operators')


REGISTRY = {
    WPS_CAPABILITIES: check_wps_capabilities,
    CHECK_SHAPE: check_shape,
}

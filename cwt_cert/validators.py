import copy
import logging
import re

import cdms2
import cwt

logger = logging.getLogger('cwt_cert.validators')
logger.setLevel(logging.DEBUG)

WPS_CAPABILITIES = 'wps_capabilities'
CHECK_SHAPE = 'check_shape'

SUCCESS = 'success'
FAILURE = 'failure'


class ValidationError(Exception):
    def __init__(self, message, *args):
        self.message = message.format(*args)

    def __str__(self):
        return self.message


def check_shape(output, shape):
    f = None

    logger.info('Opening %r', output.uri)

    try:
        f = cdms2.open(output.uri)

        logger.info('Reading shape of variable %r', output.var_name)

        try:
            var_shape = f[output.var_name].shape
        except AttributeError:
            raise ValidationError('Variable {!r} was not found in {!r}',
                                  output.var_name, output.uri)

        logger.info('Read shape of %r', var_shape)

        if var_shape != shape:
            raise ValidationError('Outputs shape {!r} does not match the'
                                  ' expected shape {!r}', var_shape, shape)
    except cdms2.CDMSError:
        raise ValidationError('Failed to open {!r}', output.uri)
    finally:
        if f is not None:
            f.close()

    return 'Verified variable {!r} shape is {!r}'.format(
        output.var_name, shape)


def check_wps_capabilities(output, operations):
    if not isinstance(output, cwt.CapabilitiesWrapper):
        msg = 'Expecting type {!r} got {!r}'.format(cwt.CapabilitiesWrapper,
                                                    type(output))

        raise ValidationError(msg)

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

        raise ValidationError('Missing operations matching {!r}', ', '.join(
            missing_ops))

    return 'Successfully identifier all required operators'


REGISTRY = {
    WPS_CAPABILITIES: check_wps_capabilities,
    CHECK_SHAPE: check_shape,
}

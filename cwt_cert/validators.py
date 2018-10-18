import copy
import logging
import re

import cdms2
import cwt

from cwt_cert import exceptions

logger = logging.getLogger('cwt_cert.validators')
logger.setLevel(logging.DEBUG)

WPS_CAPABILITIES = 'wps_capabilities'
CHECK_SHAPE = 'check_shape'

SUCCESS = 'success'
FAILURE = 'failure'


def check_shape(action_output, shape):
    output = action_output.get('output')

    logger.info('Opening %r', output.uri)

    try:
        with cdms2.open(output.uri) as f:
            logger.info('Reading shape of variable %r', output.var_name)

            try:
                var_shape = f[output.var_name].shape
            except AttributeError:
                msg = 'Variable {!r} was not found in {!r}'.format(
                    output.var_name, output.uri)

                raise exceptions.CertificationError(msg)

            logger.info('Read shape of %r', var_shape)

            if var_shape != shape:
                msg = 'Outputs shape {!r} does not match the '
                'expected shape {!r}'.format(var_shape, shape)

                raise exceptions.CertificationsError(msg)
    except cdms2.CDMSError:
        msg = 'Failed to open {!r}'.format(output.uri)
        
        raise exceptions.CertificationError(msg)

    return 'Verified variable {!r} shape is {!r}'.format(
        output.var_name, shape)


def check_wps_capabilities(output, operations):
    if not isinstance(output, cwt.CapabilitiesWrapper):
        msg = 'Expecting type {!r} got {!r}'.format(cwt.CapabilitiesWrapper,
                                                    type(output))

        raise exceptions.CertificationError(msg)

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

        raise exceptions.CertificationError(msg)

    return 'Successfully identifier all required operators'


REGISTRY = {
    WPS_CAPABILITIES: check_wps_capabilities,
    CHECK_SHAPE: check_shape,
}

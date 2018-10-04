import copy
import logging
import re
from functools import partial

import cwt

logger = logging.getLogger('cwt_cert.validators')
logger.setLevel(logging.DEBUG)

WPS_CAPABILITIES = 'wps_capabilities'

SUCCESS = 'success'
FAILURE = 'failure'


def format_result(message, extra=None, status=None):
    result = {
        'status': status,
        'message': message,
    }

    if extra is not None:
        result['extra'] = extra

    return result


format_success = partial(format_result, status=SUCCESS)


format_failure = partial(format_result, status=FAILURE)


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
}

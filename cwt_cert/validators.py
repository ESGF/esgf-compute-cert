import logging
import re
from functools import partial

from cwt.wps import wps

logger = logging.getLogger('cwt_cert.validators')
logger.setLevel(logging.DEBUG)

WPS_CAPABILITIES = 'wps_capabilities'

SUCCESS = 'success'
FAILURE = 'failure'


def format_result(message, extra=None, status=None):
    return {
        'status': status,
        'message': message,
        'extra': extra,
    }


format_success = partial(format_result, status=SUCCESS)


format_failure = partial(format_result, status=FAILURE)


def check_wps_capabilities(output, operations):
    assert 'status_code' in output
    assert 'text' in output

    status_code = output['status_code']

    if status_code >= 300:
        msg = 'Expected status code less than 300, recieved {}'.format(
            status_code)

        return format_failure(msg)

    text = output['text']

    item = wps.CreateFromDocument(text)

    if item is None or not isinstance(item, wps.WPSCapabilitiesType):
        msg = 'Did not recieve a WPS GetCapabilities response'

        return format_failure(msg)

    identifiers = [x.Identifier.value() for x in item.ProcessOfferings.Process]

    operations_copy = [x for x in operations]

    for x in identifiers:
        for y in operations_copy:
            if re.match(y, x) is not None:
                logger.info('Matched %r to %r', y, x)

                break

        operations_copy.remove(y)

    if len(operations_copy) > 0:
        msg = 'Missing operations matching the following: "{}"'.format(
            ', '.join(operations_copy))

        return format_failure(msg)

    extra = {
        'operations': identifiers,
    }

    return format_success('Successfully identifier all required operations',
                          extra)


REGISTRY = {
    WPS_CAPABILITIES: check_wps_capabilities,
}

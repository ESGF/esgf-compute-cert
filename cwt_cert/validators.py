import logging
import re
from functools import partial

from cwt.wps import wps

logger = logging.getLogger('cwt_cert.validators')
logger.setLevel(logging.DEBUG)

WPS_CAPABILITIES = 'wps_capabilities'

SUCCESS = 'success'
FAILURE = 'failure'


def format_result(check_type, snapshot, result):
    data = {
        'type': check_type,
        'validation_result': result,
    }

    data.update(snapshot)

    return data


format_success = partial(format_result, result=SUCCESS)


def format_failure(check_type, snapshot, message, value, expected=None,
                   **extra):
    data = format_result(check_type, snapshot, FAILURE)

    data['reason'] = {
        'message': message,
        'value': value,
        'expected': expected,
    }

    data['reason'].update(extra)

    return data


def check_wps_capabilities(snapshot, operations):
    result = snapshot['result']

    assert 'status_code' in result
    assert 'text' in result

    status_code = result['status_code']

    if status_code >= 300:
        msg = 'Expected status code less than 300, recieved {}'.format(
            status_code)

        return format_failure(WPS_CAPABILITIES, snapshot, msg, status_code)

    text = result['text']

    item = wps.CreateFromDocument(text)

    if item is None or not isinstance(item, wps.WPSCapabilitiesType):
        msg = 'Did not recieve a WPS GetCapabilities response'

        return format_failure(WPS_CAPABILITIES, snapshot, msg, text)

    identifiers = [x.Identifier.value() for x in item.ProcessOfferings.Process]

    operations_copy = [x for x in operations]

    for x in identifiers:
        for y in operations:
            if re.match(y, x) is not None:
                logger.info('Matched %r to %r', y, x)

                break

        operations.remove(y)

    if len(operations) > 0:
        msg = 'Missing operations matching the following: "{}"'.format(
            ', '.join(operations))

        return format_failure(WPS_CAPABILITIES, snapshot, msg, identifiers,
                              operations=operations_copy)

    return format_success(WPS_CAPABILITIES, snapshot)


REGISTRY = {
    WPS_CAPABILITIES: check_wps_capabilities,
}

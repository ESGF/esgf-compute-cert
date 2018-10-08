import logging
import re
import time

import cwt

logging.getLogger('urllib3').setLevel(logging.DEBUG)

logger = logging.getLogger('cwt_cert.actions')
logger.setLevel(logging.DEBUG)

WPS_CAPABILITIES = 'wps_capabilities_action'
WPS_EXECUTE = 'wps_execute_action'


class ActionError(Exception):
    pass


def wps_execute_action(url, identifier, inputs, api_key, *args, **kwargs):
    client = cwt.WPSClient(url, verify=False, api_key=api_key)

    try:
        process = [x for x in client.get_capabilities().processes if
                   re.match(identifier, x.identifier) is not None][0]
    except IndexError:
        raise ActionError('Did not find a process matching {}'.format(
            identifier))

    client.execute(process, inputs=inputs) 

    logger.info('%r', process.status)

    while process.processing:
        logger.info('%r', process.status)

        time.sleep(1)

    logger.info('%r', process.status)

    return process.output


def wps_capabilities_action(url, *args, **kwargs):
    client = cwt.WPSClient(url, verify=False)

    return client.get_capabilities()


REGISTRY = {
    WPS_CAPABILITIES: wps_capabilities_action,
    WPS_EXECUTE: wps_execute_action,
}

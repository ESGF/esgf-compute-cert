import logging
import re

import cwt

logging.getLogger('urllib3').setLevel(logging.DEBUG)

logger = logging.getLogger('cwt_cert.actions')
logger.setLevel(logging.DEBUG)

WPS_CAPABILITIES = 'wps_capabilities_action'
WPS_EXECUTE = 'wps_execute_action'


def wps_execute_action(url, identifier, inputs, api_key, *args, **kwargs):
    client = cwt.WPSClient(url, verify=False, api_key=api_key)

    process = [x for x in client.get_capabilities().processes if
               re.match(identifier, x.identifier) is not None][0]

    client.execute(process, inputs=inputs) 

    return None


def wps_capabilities_action(url, *args, **kwargs):
    client = cwt.WPSClient(url, verify=False)

    return client.get_capabilities()


REGISTRY = {
    WPS_CAPABILITIES: wps_capabilities_action,
    WPS_EXECUTE: wps_execute_action,
}

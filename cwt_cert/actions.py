import logging

import cwt

logging.getLogger('urllib3').setLevel(logging.DEBUG)

logger = logging.getLogger('cwt_cert.actions')
logger.setLevel(logging.DEBUG)

WPS_CAPABILITIES = 'wps_capabilities_action'
WPS_EXECUTE = 'wps_execute_action'


def wps_execute_action(url, *args, **kwargs):
    client = cwt.WPSClient(args[0], verify=False)

    identifiers = [x.identifier for x in client.get_capabilities().processes]

    print identifiers

    return None


def wps_capabilities_action(*args, **kwargs):
    client = cwt.WPSClient(args[0], verify=False)

    return client.get_capabilities()


REGISTRY = {
    WPS_CAPABILITIES: wps_capabilities_action,
    WPS_EXECUTE: wps_execute_action,
}

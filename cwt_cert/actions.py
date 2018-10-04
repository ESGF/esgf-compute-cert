import logging

import cwt

logging.getLogger('urllib3').setLevel(logging.DEBUG)

logger = logging.getLogger('cwt_cert.actions')
logger.setLevel(logging.DEBUG)

WPS_CAPABILITIES = 'wps_capabilities_action'


def wps_capabilities_action(*args, **kwargs):
    client = cwt.WPSClient(args[0], verify=False)

    return client.get_capabilities()


REGISTRY = {
    WPS_CAPABILITIES: wps_capabilities_action,
}

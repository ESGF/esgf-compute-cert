import logging
import re
import time
from datetime import datetime

import cwt

from cwt_cert import exceptions

logging.getLogger('urllib3').setLevel(logging.DEBUG)

logger = logging.getLogger('cwt_cert.actions')
logger.setLevel(logging.DEBUG)

WPS_EXECUTE_UNTIL_SUCCESS = 'wps_execution_success_action'
WPS_EXECUTE = 'wps_execute_action'
WPS_CAPABILITIES = 'wps_capabilities_action'

REGISTRY = {}


def register(name):
    def wrapper(func):
        if name not in REGISTRY:
            REGISTRY[name] = func

        return func

    return wrapper


@register(WPS_EXECUTE_UNTIL_SUCCESS)
def wps_execute_success_action(url, api_key, inputs, *args, **kwargs):
    domain = cwt.Domain(time=slice(0, 1))

    client = cwt.WPSClient(url, verify=False, api_key=api_key)

    process = client.processes('.*\.subset')[0]

    result = None

    logger.info('INPUTS %r', inputs)

    for input in inputs:
        try:
            client.execute(process, inputs=[input], domain=domain)

            if process.wait():
                result = input

                break
        except Exception:
            logger.exception('Error executing subset')

            pass

    return result


@register(WPS_EXECUTE)
def wps_execute_action(url, identifier, api_key, inputs=None, domain=None,
                       parameters=None, *args, **kwargs):
    client = cwt.WPSClient(url, verify=False, api_key=api_key)

    try:
        process = [x for x in client.get_capabilities().processes if
                   re.match(identifier, x.identifier) is not None][0]
    except IndexError:
        raise exceptions.CertificationError(
            'Did not find a process matching {}'.format(identifier))

    start = datetime.now()

    client.execute(process, inputs=inputs)

    process.wait()

    elapsed = datetime.now() - start

    result = {
        'output': process.output,
        'elapsed': elapsed,
    }

    return result


@register(WPS_CAPABILITIES)
def wps_capabilities_action(url, *args, **kwargs):
    client = cwt.WPSClient(url, verify=False)

    data = client.get_capabilities()

    return data

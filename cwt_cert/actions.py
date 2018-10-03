import logging

import requests

logging.getLogger('urllib3').setLevel(logging.DEBUG)

logger = logging.getLogger('cwt_cert.actions')
logger.setLevel(logging.DEBUG)

HTTP_REQ_ACTION = 'http_req_action'


def http_request_action(*args, **kwargs):
    response = requests.request(*args, **kwargs)

    result = {
        'status_code': response.status_code,
        'text': response.text,
    }

    return result


REGISTRY = {
    HTTP_REQ_ACTION: http_request_action,
}

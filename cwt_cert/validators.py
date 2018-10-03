import logging

logger = logging.getLogger('cwt_cert.validators')
logger.setLevel(logging.DEBUG)

STATUS_CODE = 'status_code'

SUCCESS = 'success'
FAILURE = 'failure'


def format_result(check_type, kwargs, result):
    return {
        'type': check_type,
        'kwargs': kwargs,
        'result': result,
    }


def check_status_code(**kwargs):
    assert 'status_code' in kwargs

    status_code = kwargs['status_code']

    if status_code >= 300:
        return format_result(STATUS_CODE,  kwargs, FAILURE)

    return format_result(STATUS_CODE, kwargs, SUCCESS)


REGISTRY = {
    STATUS_CODE: check_status_code,
}

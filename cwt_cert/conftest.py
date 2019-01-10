import cwt
import pytest

def pytest_addoption(parser):
    parser.addoption('--host', required=True, help='')

    parser.addoption('--token', required=True, help='')

class Context(object):
    def __init__(self, host, token):
        self.host = host
        self.token = token

    def get_client(self):
        client = cwt.WPSClient(self.host, verify=False)

        return client

    def get_client_token(self):
        client = cwt.WPSClient(self.host, api_key=self.token, verify=False)

        return client

@pytest.fixture
def context(request):
    host = request.config.getoption('--host')

    token = request.config.getoption('--token')

    return Context(host, token)

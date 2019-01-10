import cwt
import pytest

def pytest_addoption(parser):
    parser.addoption('--host', required=True, help='')

class Context(object):
    def __init__(self, host):
        self.host = host

    def get_client(self):
        client = cwt.WPSClient(self.host, verify=False)

        return client

@pytest.fixture
def context(request):
    host = request.config.getoption('--host')

    return Context(host)

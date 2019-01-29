import collections
import json

import cwt
import pytest

pytest.register_assert_rewrite('cwt_cert.process_base')

class Context(object):
    def __init__(self, host, token):
        self.host = host
        self.token = token
        self.data_inputs = {}

    def get_client(self):
        client = cwt.WPSClient(self.host, verify=False)

        return client

    def get_client_token(self):
        client = cwt.WPSClient(self.host, api_key=self.token, verify=False)

        return client

    def set_data_inputs(self, request, variables, domain, operation):
        client = self.get_client()

        data_inputs = client.prepare_data_inputs(operation, variables, domain)

        if request.node._nodeid in self.data_inputs:
            self.data_inputs[request.node._nodeid].append(data_inputs) 
        else:
            self.data_inputs[request.node._nodeid] = [data_inputs]

class CWTCertificationReport(object):
    def __init__(self, config):
        self.config = config

        self._context = None
        self.tests = collections.OrderedDict()

    @pytest.fixture
    def context(self, request):
        ctx = getattr(self, 'context', None)

        if ctx is None:
            host = request.config.getoption('--host')

            token = request.config.getoption('--token')

            ctx = Context(host, token)

            setattr(self, 'context', ctx)

        return ctx

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):
        outcome = yield

        rep = outcome.get_result()

        if rep.when == 'call':
            self.tests[rep.nodeid] = {
                'outcome': rep.outcome,
                'longrepr': str(rep.longrepr),
                'stdout': str(rep.capstdout),
                'stderr': str(rep.capstderr),
                'duration': rep.duration,
            }

            if rep.nodeid in self._context.data_inputs:
                self.tests[rep.nodeid]['data_inputs'] = self._context.data_inputs[rep.nodeid]

    def pytest_sessionfinish(self, session, exitstatus):
        json_report_file = self.config.getoption('--json-report-file', None)

        if json_report_file is not None:
            report = {
                'tests': self.tests,
            }

            with open(json_report_file, 'w') as outfile:
                json.dump(report, outfile, indent=True)

def pytest_addoption(parser):
    group = parser.getgroup('cwt certification', 'cwt certification')

    group.addoption('--host', required=True, help='target host to run tests on')

    group.addoption('--token', required=True, help='token to be used for api access')

    group.addoption('--test', help='specify a test to run')

    group.addoption('--list-tests', action='store_true', help='lists the available tests')

    group.addoption('--json-report-file', help='path to store json report')

def pytest_configure(config):
    plugin = CWTCertificationReport(config)

    config._cert_report = plugin

    config.pluginmanager.register(plugin)

def pytest_unconfigure(config):
    plugin = getattr(config, '_cert_report', None)

    if plugin is not None:
        del config._cert_report

        config.pluginmanager.unregister(plugin)

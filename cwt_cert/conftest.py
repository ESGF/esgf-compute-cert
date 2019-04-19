from builtins import str
from builtins import object
import collections
import json

import cwt
import pytest

pytest.register_assert_rewrite('cwt_cert.process_base')

MARKERS = [
    'stress: mark a test as a stress test.',
    'performance: mark a test as a performance test.',
    'api_compliance: mark a test as an api compliance test.',
    'metrics: mark a test as a metrics test.',
    'security: mark a test as a security test.',
    'operators: mark a test as an operators test.',
    'server: mark a test as a server test.',
    'aggregate: mark a test as an aggregate test.',
    'subset: mark a test as a subset test.',
]


class Context(object):
    def __init__(self, config):
        self.config = config
        self.data_inputs = {}

    @property
    def host(self):
        return self.config.getoption('--host')

    @property
    def token(self):
        return self.config.getoption('--token')

    @property
    def module(self):
        return self.config.getoption('--module')

    @property
    def module_metrics(self):
        value = self.config.getoption('--module-metrics')

        # Default to the module option
        if value is None:
            return self.config.getoption('--module')

        return value

    @property
    def metrics_identifier(self):
        return '{!s}.metrics'.format(self.module_metrics)

    def format_identifier(self, operation):
        return '{!s}.{!s}'.format(self.module, operation)

    def get_client(self):
        client = cwt.WPSClient(self.host)

        return client

    def get_client_token(self):
        client = cwt.WPSClient(self.host, api_key=self.token)

        return client

    def set_data_inputs(self, request, variables, domain, operation, **kwargs):
        client = self.get_client()

        data_inputs = client.prepare_data_inputs(operation, variables, domain)

        if request.node._nodeid in self.data_inputs:
            self.data_inputs[request.node._nodeid].append(data_inputs)
        else:
            self.data_inputs[request.node._nodeid] = [data_inputs]


class CWTCertificationReport(object):
    def __init__(self, config):
        self.config = config

        self._context = Context(config)

        self.tests = collections.OrderedDict()

    @classmethod
    def from_config(cls, config):
        return cls(config)

    @pytest.fixture(scope='session')
    def context(self, request):
        return self._context

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

    def pytest_sessionstart(self, session):
        if self._context.host is None:
            raise pytest.UsageError('Missing required parameter --host')

        if self._context.module is None:
            raise pytest.UsageError('Missing required parameter --module')

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

    group.addoption('--host', help='target host to run tests on')

    group.addoption('--token', help='token to be used for api access')

    group.addoption('--module', help='name of the module to be tested')

    group.addoption('--module-metrics', default=None, help='name of the metrics module, this may differ from the '
                    'target module')

    group.addoption('--json-report-file', help='path to store json report')


def pytest_configure(config):
    plugin = CWTCertificationReport.from_config(config)

    config._cert_report = plugin

    config.pluginmanager.register(plugin)

    for marker in MARKERS:
        config.addinivalue_line('markers', marker)


def pytest_unconfigure(config):
    plugin = getattr(config, '_cert_report', None)

    if plugin is not None:
        del config._cert_report

        config.pluginmanager.unregister(plugin)

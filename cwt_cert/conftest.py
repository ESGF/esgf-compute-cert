import collections
import json
import os
import re
from functools import partial
from uuid import uuid4

import cwt
import pytest
import requests

pytest.register_assert_rewrite('cwt_cert.process_base')

MARKERS = [
    'stress: mark a test as a stress test.',
    'performance: mark a test as a performance test.',
    'api_compliance: mark a test as an api compliance test.',
    'metrics: mark a test as a metrics test.',
    'security: mark a test as a security test.',
    'operators: mark a test as an operators test.',
    'server: mark a test as a server test.',
]


def default(o):
    return o


def object_hook(o):
    if 'domain' in o:
        domain = o['domain']

        domain['id'] = str(uuid4())

        o = {'domain': cwt.Domain.from_dict(domain)}

    return o


encoder = partial(json.dumps, default=default)

decoder = partial(json.loads, object_hook=object_hook)


class Context(object):
    def __init__(self, config, test_config):
        self.config = config
        self.test_config = test_config
        self.storage = {}

    @property
    def install_dir(self):
        return os.path.dirname(__file__)

    @property
    def output_dir(self):
        return self.config.getoption('--output-dir')

    @property
    def verify(self):
        return self.config.getoption('--skip-verify')

    @property
    def url(self):
        return self.config.getoption('--url')

    @property
    def token(self):
        return self.config.getoption('--token')

    @property
    def module(self):
        return self.config.getoption('--module')

    def get_client(self):
        client = cwt.WPSClient(self.url, verify=self.verify)

        return client

    def get_client_token(self):
        client = cwt.WPSClient(self.url, api_key=self.token, verify=self.verify)

        return client

    def set_extra(self, request, key, name, value):
        nodeid = request.node._nodeid

        if nodeid not in self.storage:
            node = self.storage[nodeid] = {}
        else:
            node = self.storage[nodeid]

        if key in node:
            node[key].update({name: value})
        else:
            node[key] = {
                name: value
            }


class CWTCertificationPlugin(object):
    def __init__(self, config, test_config):
        self.config = config

        self.test_config = test_config

        self._context = Context(config, test_config)

        self.test_output = collections.OrderedDict()

    @staticmethod
    def read_file(uri):
        if re.match('^http[s]?://.*', uri) is None:
            with open(uri) as infile:
                data = infile.read()
        else:
            res = requests.get(uri)

            res.raise_for_status()

            data = res.content

        return data

    @classmethod
    def from_config(cls, config):
        install_path = os.path.dirname(__file__)

        test_config_path = os.path.join(install_path, 'config-test.json')

        test_config_file = cls.read_file(test_config_path)

        test_config = decoder(test_config_file)

        config_override_path = config.getoption('--config')

        if config_override_path is not None:
            config_override_file = cls.read_file(config_override_path)

            test_config.update(decoder(config_override_file))

        return cls(config, test_config)

    @pytest.fixture(scope='session')
    def context(self, request):
        return self._context

    def pytest_generate_tests(self, metafunc):
        if ('module' in metafunc.fixturenames and
                'op' in metafunc.fixturenames and
                'version' in metafunc.fixturenames):
            parameters = []

            for op_name, op_val in self.test_config['operators'].items():
                for mod_name, mod_val in op_val.items():
                    for version in mod_val['version']:
                        parameters.append((mod_name, op_name, version))

            metafunc.parametrize(('module', 'op', 'version'), parameters)

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):
        outcome = yield

        rep = outcome.get_result()

        if rep.when == 'call':
            self.test_output[rep.nodeid] = {
                'outcome': rep.outcome,
                'longrepr': str(rep.longrepr),
                'stdout': str(rep.capstdout),
                'stderr': str(rep.capstderr),
                'duration': rep.duration,
            }

            if rep.nodeid in self._context.storage:
                self.test_output[rep.nodeid].update(self._context.storage[rep.nodeid])

    def pytest_sessionstart(self, session):
        if self._context.url is None:
            raise pytest.UsageError('Missing required parameter --url')

        if self._context.module is None:
            raise pytest.UsageError('Missing required parameter --module')

        if self._context.output_dir is not None:
            if not os.path.exists(self._context.output_dir):
                os.makedirs(self._context.output_dir)

    def pytest_sessionfinish(self, session, exitstatus):
        json_report_file = self.config.getoption('--json-report-file', None)

        if json_report_file is not None:
            with open(json_report_file, 'w') as outfile:
                json.dump(self.test_output, outfile, indent=True)


def pytest_addoption(parser):
    group = parser.getgroup('cwt certification', 'cwt certification')

    group.addoption('--url', help='url of the WPS service to run certification on')

    group.addoption('--module', help='name of the module to use for server testing')

    group.addoption('--config', help='config file to override test configuration')

    group.addoption('--skip-verify', help='skip tls verifying', action='store_false')

    group.addoption('--token', help='compute token')

    group.addoption('--output-dir', help='directory to write process outputs')

    group.addoption('--json-report-file', help='file to write JSON report')


def pytest_configure(config):
    plugin = CWTCertificationPlugin.from_config(config)

    config._cert_report = plugin

    config.pluginmanager.register(plugin)

    for marker in MARKERS:
        config.addinivalue_line('markers', marker)


def pytest_unconfigure(config):
    plugin = getattr(config, '_cert_report', None)

    if plugin is not None:
        del config._cert_report

        config.pluginmanager.unregister(plugin)

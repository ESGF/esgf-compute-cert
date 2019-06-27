# ESGF Compute Certification

The esgf-compute-cert tool is a Python 3 utility to certify [ESGF](https://esgf.llnl.gov/) compute nodes. This tool will run a set of tests to certify a compute node and/or WPS operaotrs according to the [ESGF-Compute-Certification](https://esgf.llnl.gov/esgf-media/pdf/ESGF-Compute-Certification.pdf) document.

A compute node can be a certified node and/or serve certified WPS operations. The following is a quick overview of the tests to certify a node or operation.

- Node certification
  - Official Operator: Check that official approved operators are present.
  - Stress: A WPS submission that will attempt to tax the service.
  - Metrics Operator: Check that a metrics operator exists and passes correctly formatted output.
  - Security: Check that the WPS execute endpoint is secure.
- Operation certification
  - Performance: A single WPS submission that will be timed.
  - Api Compliance: One or many WPS submission to test that an operator is Api compliant. This is dependent on each operators secificiation.

The tool itself is built on [pytest](https://docs.pytest.org/en/latest/) and runs much like a traditional unit test suite.

## Installation

#### Release
```
conda install -c conda-forge -c cdat esgf-compute-cert
```

#### Development
```
conda install -c conda-forge -c cdat esgf-compute-cert=0.*
```

## Usage

#### Simple
Run all test cases against a server. The argument `--module CDAT` is the module the testing framework will use to run the server tests against.
```
cwt-cert --url https://aims2.llnl.gov/wps/ --module CDAT --token abcd.1234
```

Create a result file.
```
cwt-cert --url https://aims2.llnl.gov/wps/ --module CDAT --token abcd.1234 --json-report-file result.json
```

#### Markers
The tool is built on top of pytest which enables the filtering of which tests
are run by passing marker expressions.

List the markers.
```
cwt-cert --markers
@pytest.mark.operators: filter operator tests (will run performance and api_compliance tests)

@pytest.mark.performance: filter operator performance tests

@pytest.mark.api_compliance: filter operator api compliance tests

@pytest.mark.server: filter server tests (will run stress, metrics, security and official_operator tests)

@pytest.mark.stress: filter server stress tests

@pytest.mark.metrics: filter server metrics test

@pytest.mark.security: filter server security test

@pytest.mark.official_operator: filter server official operator test

@pytest.mark.CDAT: filter CDAT module tests

@pytest.mark.subset: filter subset operation tests

@pytest.mark.aggregate: filter aggregate operation tests

@pytest.mark.1_0_0: filter 1_0_0 version tests
```

Run only server stress test.
```
cwt-cert ... -m "server and stress"
```

Run all tests except stress tests.
```
cwt-cert ... -m "not stress"
```

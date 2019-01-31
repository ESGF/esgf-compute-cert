# ESGF Compute Certification

This tool is provided to certify [ESGF](https://esgf.llnl.gov/) compute nodes according to the this
[document](https://esgf.llnl.gov/esgf-media/pdf/ESGF-Compute-Certification.pdf).

## Installation

```
conda install -c conda-forge -c cdat esgf-compute-cert
```

## Usage

#### Simple
Run all test cases against the server.
```
cwt-cert --host https://aims2.llnl.gov/wps
```

Pass an authorization token to the server.
```
cwt-cert --host https://aims2.llnl.gov/wps --token abcd.1234
```

Create a result file.
```
cwt-cert --host https://aims2.llnl.gov/wps --json-report-file result.json
```

#### Markers
The tool is built on top of pytest which enables the filtering of which tests
are run by passing marker expressions.

List the markers.
```
cwt-cert --markers
```

Run only server stress test.
```
cwt-cert ... -m "server and stress"
```

Run all tests except stress tests.
```
cwt-cert ... -m "not stress"
```

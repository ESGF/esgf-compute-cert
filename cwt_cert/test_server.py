import cwt
import pytest

# subset
# https://aims3.llnl.gov/thredds/catalog/esgcet/123/cmip3.IPSL.ipsl_cm4.historical.mon.atmos.run1.ta.v1.html#cmip3.IPSL.ipsl_cm4.historical.mon.atmos.run1.ta.v1
# aggregate
# https://aims3.llnl.gov/thredds/catalog/esgcet/122/cmip3.NCAR.ncar_ccsm3_0.historical.mon.atmos.run1.tas.v1.html#cmip3.NCAR.ncar_ccsm3_0.historical.mon.atmos.run1.tas.v1

def test_stress(context):
    client = context.get_client_token()

    config = [
        {
            'identifier': '.*\.subset',
            'variable': 'ta',
            'inputs': [
                'https://aims3.llnl.gov/thredds/dodsC/cmip3_data/data2/20c3m/atm/mo/ta/ipsl_cm4/run1/ta_A1_1860-2000.nc',
            ],
            'domain': {
                'time': (0, 1000),
            },
        },
        {
            'identifier': '.*\.subset',
            'variable': 'ta',
            'inputs': [
                'https://aims3.llnl.gov/thredds/dodsC/cmip3_data/data2/20c3m/atm/mo/ta/ipsl_cm4/run1/ta_A1_1860-2000.nc',
            ],
            'domain': {
                'time': (5000, 6000),
            },
        },
        {
            'identifier': '.*\.aggregate',
            'variable': 'tas',
            'inputs': [
                'https://aims3.llnl.gov/thredds/dodsC/cmip3_data/data2/20c3m/atm/mo/tas/ncar_ccsm3_0/run1/tas_A1.20C3M_1.CCSM.atmm.1870-01_cat_1879-12.nc',
                'https://aims3.llnl.gov/thredds/dodsC/cmip3_data/data2/20c3m/atm/mo/tas/ncar_ccsm3_0/run1/tas_A1.20C3M_1.CCSM.atmm.1880-01_cat_1889-12.nc',
            ],
        },
        {
            'identifier': '.*\.aggregate',
            'variable': 'tas',
            'inputs': [
                'https://aims3.llnl.gov/thredds/dodsC/cmip3_data/data2/20c3m/atm/mo/tas/ncar_ccsm3_0/run1/tas_A1.20C3M_1.CCSM.atmm.1980-01_cat_1989-12.nc',
                'https://aims3.llnl.gov/thredds/dodsC/cmip3_data/data2/20c3m/atm/mo/tas/ncar_ccsm3_0/run1/tas_A1.20C3M_1.CCSM.atmm.1990-01_cat_1999-12.nc',
            ],
        },
    ]

    active = []

    for data in config:
        domain = None

        if 'domain' in data:
            domain = cwt.Domain(**data['domain'])

        inputs = [cwt.Variable(x, data['variable']) for x in data['inputs']]

        process = client.processes(data['identifier'])[0]

        client.execute(process, inputs, domain)

        active.append(process)

    while len(active) > 0:
        current = active.pop()

        assert current.wait(timeout=3*60)

def test_api_compliance(context):
    client = context.get_client_token()

    process = client.processes('.*\.subset')[0]

    inputs = [
        cwt.Variable('https://aims3.llnl.gov/thredds/dodsC/cmip3_data/data2/20c3m/atm/mo/ta/ipsl_cm4/run1/ta_A1_1860-2000.nc', 'ta'),
    ]

    # Dimension by values
    domain = cwt.Domain(time=(0, 30))

    client.execute(process, inputs, domain)

    assert process.wait(240)

    # Dimension by indices
    domain = cwt.Domain(time=slice(0, 2))

    client.execute(process, inputs, domain)

    assert process.wait(240)

def test_metrics(context):
    client = context.get_client_token()

    process = client.processes('.*\.metrics')

    assert len(process) > 0

    process = process[0]

    client.execute(process)

    assert process.wait()

    data = process.output

    assert 'usage' in data
    assert 'health' in data

def test_security(context):
    # Check SSL
    # Check execute is protected
    # ?

    client = context.get_client()

    process = client.processes('.*\.metrics')

    assert len(process) > 0

    process = process[0]

    # Expect an error to be raised
    with pytest.raises(cwt.WPSExceptionError):
        client.execute(process)

def test_official_operators(context):
    client = context.get_client()

    expected = set(['aggregate', 'subset', 'metrics'])

    for method in expected:
        process = client.processes('.*\.{!s}'.format(method))

        assert len(process) > 0

        assert method in process[0].identifier

import cwt
import pytest

@pytest.mark.stress
@pytest.mark.server
def test_stress(context):
    client = context.get_client_token()


@pytest.mark.api_compliance
@pytest.mark.server
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

@pytest.mark.metrics
@pytest.mark.server
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

@pytest.mark.security
@pytest.mark.server
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

@pytest.mark.operators
@pytest.mark.server
def test_official_operators(context):
    client = context.get_client()

    expected = set(['aggregate', 'subset', 'metrics'])

    for method in expected:
        process = client.processes('.*\.{!s}'.format(method))

        assert len(process) > 0

        assert method in process[0].identifier

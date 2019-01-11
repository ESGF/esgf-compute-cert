import cwt
import pytest

def test_stress(context):
    client = context.get_client_token()

    inputs = [
        cwt.Variable('https://aims3.llnl.gov/thredds/dodsC/css03_data/CMIP6/CMIP/NASA-GISS/GISS-E2-1-G/amip/r1i1p1f1/Amon/pr/gn/v20181016/pr_Amon_amip_GISS-E2-1-G_r1i1p1f1_gn_185001-190012.nc', 'pr'),
    ]

    domain = cwt.Domain(time=(500, 1000))

    active = []

    for _ in range(4):
        process = client.processes('.*\.subset')[0]

        client.execute(process, inputs, domain)

        active.append(process)

    while len(active) > 0:
        current = active.pop()

        assert current.wait()

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

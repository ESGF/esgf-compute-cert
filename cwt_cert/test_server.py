import cwt
import pytest

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

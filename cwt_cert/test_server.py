import cwt

def test_official_operators(context):
    client = context.get_client()

    expected = set(['aggregate', 'subset'])

    for method in expected:
        process = client.processes('.*\.{!s}'.format(method))

        assert len(process) > 0

        assert method in process[0].identifier

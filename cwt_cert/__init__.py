import os

os.environ['UVCDAT_ANONYMOUS_LOG'] = 'no'


def main():
    import sys
    import pytest

    install_path = os.path.dirname(os.path.realpath(__file__))

    result = pytest.main([install_path, '-v', '--ignore', 'test_base.py'] + sys.argv[1:])

    exit(result)

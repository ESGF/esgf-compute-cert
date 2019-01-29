import os

os.environ['UVCDAT_ANONYMOUS_LOG'] = 'no'

def main():
    import sys
    import pytest

    install_path = os.path.dirname(os.path.realpath(__file__))

    pytest.main([install_path, '-v'] + sys.argv[1:])

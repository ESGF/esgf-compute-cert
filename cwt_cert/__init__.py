import os
import sys

os.environ['UVCDAT_ANONYMOUS_LOG'] = 'no'

import pytest

def main():
    pytest.main(['cwt_cert/', '-v'] + sys.argv)

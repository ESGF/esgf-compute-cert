import os

os.environ['UVCDAT_ANONYMOUS_LOG'] = 'no'

tests = None

if tests is None:
    # TODO
    # Make this generation dynamic
    from cwt_cert import test_server
    from cwt_cert import process_base

    tests = []

    tests.extend([('test_server.py', x) 
                  for x in test_server.__dict__.keys() if 'test_' in x])

    tests.extend([('test_aggregate.TestAggregate.py', x)
                  for x in process_base.ProcessBase.__dict__.keys() if 'test_' in x])

    tests.extend([('test_subset.TestSubset.py', x) 
                  for x in process_base.ProcessBase.__dict__.keys() if 'test_' in x])

def print_tests():
    print 'Available tests'

    for x in tests:
        print '\t', '::'.join(x)

def main():
    import sys
    import pytest

    if '--list-tests' in sys.argv:
        print_tests()
    else:
        install_path = os.path.dirname(os.path.realpath(__file__))

        if '--test' in sys.argv:
            index = sys.argv.index('--test')

            sys.argv.pop(index)

            test = sys.argv.pop(index)

            install_path = os.path.join(install_path, test)

        print install_path

        pytest.main([install_path] + sys.argv[1:])

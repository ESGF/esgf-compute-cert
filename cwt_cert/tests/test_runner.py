import datetime
import unittest

import mock

from cwt_cert import actions
from cwt_cert import exceptions
from cwt_cert import runner
from cwt_cert import validators


class TestRunner(unittest.TestCase):

    def test_run_validator_missing(self):
        with mock.patch('cwt_cert.validators.REGISTRY', {}):
            with self.assertRaises(AssertionError):
                runner.run_validator(None, 'test')

    def test_run_validator_exception(self):
        error_message = 'something went wrong'

        mock_action = mock.MagicMock(side_effect=Exception(error_message))

        registry = {'test': mock_action}

        args = ['arg1']

        kwargs = {'key1': 'value1'}

        with mock.patch('cwt_cert.validators.REGISTRY', registry):
            with self.assertRaises(exceptions.CertificationError):
                runner.run_validator(None, 'test', args=args, kwargs=kwargs)

    def test_run_validator_no_arguments(self):
        mock_action = mock.MagicMock(return_value=validators.SUCCESS)

        registry = {'test': mock_action}

        with mock.patch('cwt_cert.validators.REGISTRY', registry):
            status = runner.run_validator(None, 'test')

        mock_action.assert_called_with(None)

    def test_run_validator(self):
        mock_action = mock.MagicMock(return_value=validators.SUCCESS)

        registry = {'test': mock_action}

        args = ['arg1']

        kwargs = {'key1': 'value1'}

        with mock.patch('cwt_cert.validators.REGISTRY', registry):
            result = runner.run_validator(None, 'test', args=args, kwargs=kwargs, test='test')

        mock_action.assert_called_with(None, *args, **kwargs)

        self.assertEqual(result, validators.SUCCESS)

    def test_run_action_missing(self):
        with mock.patch('cwt_cert.actions.REGISTRY', {}):
            with self.assertRaises(AssertionError):
                runner.run_action('test')

    def test_run_action_exception(self):
        error_message = 'something went wrong'

        mock_action = mock.MagicMock(side_effect=Exception(error_message))

        registry = {'test': mock_action}

        args = ['arg1']

        kwargs = {'key1': 'value1'}

        with mock.patch('cwt_cert.actions.REGISTRY', registry):
            with self.assertRaises(exceptions.CertificationError):
                runner.run_action('test', args=args, kwargs=kwargs)

    def test_run_action_no_arguments(self):
        action_result = {
            'data': 'some data',
        }

        mock_action = mock.MagicMock(return_value=action_result)

        registry = {'test': mock_action}

        with mock.patch('cwt_cert.actions.REGISTRY', registry):
            output = runner.run_action('test')

        mock_action.assert_called_with()

    def test_run_action(self):
        action_result = {
            'data': 'some data',
        }

        mock_action = mock.MagicMock(return_value=action_result)

        registry = {'test': mock_action}

        args = ['arg1']

        kwargs = {'key1': 'value1'}

        with mock.patch('cwt_cert.actions.REGISTRY', registry):
            output = runner.run_action('test', args=args, kwargs=kwargs,
                                       test='test')

        mock_action.assert_called_with(*args, **kwargs)

        self.assertEqual(output, action_result)

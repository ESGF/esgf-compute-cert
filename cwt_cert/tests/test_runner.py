import unittest

import mock

from cwt_cert import actions
from cwt_cert import runner
from cwt_cert import validators


class TestRunner(unittest.TestCase):
    def setUp(self):
        self.val_inp1 = {
            'type': 'type1',
            'args': ['args1'],
            'kwargs': {
                'keyword1': 'value1',
            }
        }

        self.val_inp2 = {
            'type': 'type2',
            'args': ['args2'],
            'kwargs': {
                'keyword2': 'value2',
            }
        }

    @mock.patch('cwt_cert.runner.run_validations')
    @mock.patch('cwt_cert.runner.run_action')
    def test_run_test_validation_failure(self, mock_action, mock_validations):
        mock_action.side_effect = Exception('something terrible went wrong')

        mock_validations.return_value = validators.FAILURE

        args = ['arg1']
        kwargs = {'keyword1': 'value1'}

        test1 = {'args': args, 'kwargs': kwargs}

        result = runner.run_test('verify this', [test1])

        mock_action.assert_called_with(args=args, kwargs=kwargs)

        self.assertEqual(result['name'], 'verify this')
        self.assertEqual(result['status'], validators.FAILURE)

        self.assertEqual(result['actions'][0]['status'], validators.FAILURE)
        self.assertEqual(result['actions'][0]['message'], 'something terrible'
                         ' went wrong')

    @mock.patch('cwt_cert.runner.run_validations')
    @mock.patch('cwt_cert.runner.run_action')
    def test_run_test_action_failure(self, mock_action, mock_validations):
        mock_action.side_effect = Exception('something terrible went wrong')

        mock_validations.return_value = validators.SUCCESS

        args = ['arg1']
        kwargs = {'keyword1': 'value1'}

        test1 = {'args': args, 'kwargs': kwargs}

        result = runner.run_test('verify this', [test1])

        mock_action.assert_called_with(args=args, kwargs=kwargs)

        self.assertEqual(result['name'], 'verify this')
        self.assertEqual(result['status'], validators.FAILURE)

        self.assertEqual(result['actions'][0]['status'], validators.FAILURE)
        self.assertEqual(result['actions'][0]['message'], 'something terrible'
                         ' went wrong')

    @mock.patch('cwt_cert.runner.run_validations')
    @mock.patch('cwt_cert.runner.run_action')
    def test_run_test(self, mock_action, mock_validations):
        mock_action.return_value = 'action output'

        mock_validations.return_value = validators.SUCCESS

        args = ['arg1']
        kwargs = {'keyword1': 'value1'}

        test1 = {'args': args, 'kwargs': kwargs}

        result = runner.run_test('verify this', [test1])

        mock_action.assert_called_with(args=args, kwargs=kwargs)

        mock_validations.assert_called_with('action output', args=args,
                                            kwargs=kwargs)

        self.assertEqual(result['name'], 'verify this')
        self.assertEqual(result['status'], validators.SUCCESS)

        self.assertEqual(result['actions'][0]['status'], validators.SUCCESS)

    @mock.patch('cwt_cert.runner.run_validation')
    def test_run_validations_failure(self, mock_run):
        mock_run.side_effect = ['validation result',
                                Exception('something wrong')]

        result = runner.run_validations('output', [
            self.val_inp1,
            self.val_inp2,
        ])

        mock_run.assert_any_call('output', type='type1', args=['args1'],
                                 kwargs={'keyword1': 'value1'})

        mock_run.assert_any_call('output', type='type2', args=['args2'],
                                 kwargs={'keyword2': 'value2'})

        self.assertIn('status', self.val_inp1)
        self.assertEqual(self.val_inp1['status'], validators.SUCCESS)
        self.assertIn('message', self.val_inp1)
        self.assertEqual(self.val_inp1['message'], 'validation result')

        self.assertIn('status', self.val_inp2)
        self.assertEqual(self.val_inp2['status'], validators.FAILURE)
        self.assertIn('message', self.val_inp2)
        self.assertEqual(self.val_inp2['message'], 'something wrong')

        self.assertEqual(result, validators.FAILURE)

    @mock.patch('cwt_cert.runner.run_validation')
    def test_run_validations(self, mock_run):
        mock_run.return_value = 'validation result'

        result = runner.run_validations('output', [
            self.val_inp1,
            self.val_inp2,
        ])

        mock_run.assert_any_call('output', type='type1', args=['args1'],
                                 kwargs={'keyword1': 'value1'})

        mock_run.assert_any_call('output', type='type2', args=['args2'],
                                 kwargs={'keyword2': 'value2'})

        self.assertIn('status', self.val_inp1)
        self.assertEqual(self.val_inp1['status'], validators.SUCCESS)
        self.assertIn('message', self.val_inp1)
        self.assertEqual(self.val_inp1['message'], 'validation result')

        self.assertIn('status', self.val_inp2)
        self.assertEqual(self.val_inp2['status'], validators.SUCCESS)
        self.assertIn('message', self.val_inp2)
        self.assertEqual(self.val_inp2['message'], 'validation result')

        self.assertEqual(result, validators.SUCCESS)

    def test_run_validation_missing(self):
        validators.REGISTRY = {}

        with self.assertRaises(runner.CertificationError):
            runner.run_validation('action_output', 'test')

    def test_run_validation(self):
        mock_validation = mock.MagicMock(return_value='output')

        validators.REGISTRY = {
            'test': mock_validation,
        }

        result = runner.run_validation('action_output', 'test', ['arg1'],
                                       {'keyword1': 'value'})

        self.assertEqual(result, 'output')

        mock_validation.assert_called_with('action_output', 'arg1',
                                           keyword1='value')

    def test_run_action_missing(self):
        actions.REGISTRY = {}

        with self.assertRaises(runner.CertificationError):
            runner.run_action('test')

    def test_run_action(self):
        mock_action = mock.MagicMock(return_value='output')

        actions.REGISTRY = {
            'test': mock_action,
        }

        result = runner.run_action('test', args=['arg1'],
                                   kwargs={'keyword1': 'value'})

        self.assertEqual(result, 'output')

        mock_action.assert_called_with('arg1', keyword1='value')

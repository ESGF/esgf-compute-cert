import unittest

import cwt
import mock

from cwt_cert import actions


class TestActions(unittest.TestCase):

    @mock.patch('cwt_cert.actions.cwt.WPSClient')
    def test_wps_capabilities_action(self, mock_client):
        document = 'capabilities document'

        mock_client.return_value.get_capabilities.return_value = document

        url = 'https://mythical:8080/wps/'

        result = actions.wps_capabilities_action(url)

        mock_client.assert_called_with(url, verify=False)

        self.assertEqual(result, document)

    @mock.patch('cwt_cert.actions.cwt.WPSClient')
    def test_wps_execute_action_missing_identifier(self, mock_client):
        url = 'https://mythical:8080/wps/'

        aggregate = '.*\.aggregate'

        api_key = 'unique_api_key'

        inputs = [
            cwt.Variable('file:///test1.nc', 'tas'),
            cwt.Variable('file:///test2.nc', 'tas'),
        ]

        with self.assertRaises(actions.ActionError):
            actions.wps_execute_action(url, aggregate, inputs, api_key)

    @mock.patch('cwt_cert.actions.cwt.WPSClient')
    def test_wps_execute_action(self, mock_client):
        mock_process = mock.MagicMock(identifier='CDAT.aggregate')

        type(mock_process).processing = mock.PropertyMock(side_effect=[True,
                                                                       True,
                                                                       False])

        output = cwt.Variable('file:///test_output.nc', 'tas')

        type(mock_process).output = mock.PropertyMock(return_value=output)

        mock_client.return_value.get_capabilities.return_value.processes = [
            mock_process,
        ]

        url = 'https://mythical:8080/wps/'

        aggregate = '.*\.aggregate'

        api_key = 'unique_api_key'

        inputs = [
            cwt.Variable('file:///test1.nc', 'tas'),
            cwt.Variable('file:///test2.nc', 'tas'),
        ]

        result = actions.wps_execute_action(url, aggregate, inputs, api_key)

        mock_client.assert_called_with(url, verify=False, api_key=api_key)

        mock_client.return_value.execute.assert_called_with(mock_process,
                                                            inputs=inputs)

        self.assertEqual(result, output)

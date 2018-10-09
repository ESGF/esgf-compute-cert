import unittest

import cdms2
import cwt
import mock

from cwt_cert import validators


class TestValidators(unittest.TestCase):

    def setUp(self):
        self.output = cwt.Variable('file:///test_output.nc', 'tas')

        self.operations = [
            mock.MagicMock(identifier='CDAT.aggregate'),
            mock.MagicMock(identifier='CDAT.average'),
        ]

        self.operation_checks = [
            '.*\.aggregate',
            '.*\.average',
        ]
        
    @mock.patch('cwt_cert.validators.isinstance')
    def test_check_capabilities_not_instance(self, mock_is):
        mock_is.return_value = False

        wrapper = mock.MagicMock()

        result = validators.check_wps_capabilities(wrapper,
                                                   self.operation_checks)

        expected = validators.format_failure("Expecting type <class"
                                             " 'cwt.wps_client.CapabilitiesWra"
                                             "pper'> got <class 'mock.mock.Mag"
                                             "icMock'>")

        self.assertEqual(result, expected)

    @mock.patch('cwt_cert.validators.isinstance')
    def test_check_capabilities_missing(self, mock_is):
        mock_is.return_value = True

        wrapper = mock.MagicMock()
        wrapper.processes = self.operations[:1]

        result = validators.check_wps_capabilities(wrapper,
                                                   self.operation_checks)

        expected = validators.format_failure(
            "Missing operations matching '.*\\\\.average'")

        self.assertEqual(result, expected)

    @mock.patch('cwt_cert.validators.isinstance')
    def test_check_capabilities(self, mock_is):
        mock_is.return_value = True

        wrapper = mock.MagicMock()
        wrapper.processes = self.operations

        result = validators.check_wps_capabilities(wrapper,
                                                   self.operation_checks)

        expected = validators.format_success(
            'Successfully identifier all required operators')

        self.assertEqual(result, expected)

    @mock.patch('cwt_cert.validators.cdms2.open')
    def test_check_shape_missmatch(self, mock_open):
        type(mock_open.return_value.__getitem__.return_value).shape = \
                mock.PropertyMock(return_value=(100, 90, 180))

        result = validators.check_shape(self.output, (120, 90, 180))

        expected = validators.format_failure(
            "Outputs shape (100, 90, 180) does not match the expected shape "
            "(120, 90, 180)")

        self.assertEqual(result, expected)

    @mock.patch('cwt_cert.validators.cdms2.open')
    def test_check_shape_variable_not_found(self, mock_open):
        mock_open.return_value.__getitem__.side_effect = AttributeError()

        result = validators.check_shape(self.output, (120, 90, 180))

        expected = validators.format_failure(
            "Variable 'tas' was not found in 'file:///test_output.nc'")

        self.assertEqual(result, expected)

    @mock.patch('cwt_cert.validators.cdms2.open')
    def test_check_shape_cdms2_error(self, mock_open):
        mock_open.side_effect = cdms2.CDMSError('')

        result = validators.check_shape(self.output, (120, 90, 180))

        expected = validators.format_failure(
            "Failed to open 'file:///test_output.nc'")

        self.assertEqual(result, expected)

    @mock.patch('cwt_cert.validators.cdms2.open')
    def test_check_shape(self, mock_open):
        type(mock_open.return_value.__getitem__.return_value).shape = \
                mock.PropertyMock(return_value=(120, 90, 180))

        result = validators.check_shape(self.output, (120, 90, 180))

        mock_open.assert_called_with(self.output.uri)

        mock_open.return_value.__getitem__.assert_called_with('tas')

        expected = validators.format_success(
            "Verified variable 'tas' shape is (120, 90, 180)")

        self.assertEqual(result, expected)

    def test_format_failure(self):
        result = validators.format_failure('message {}', 'test')

        expected = {
            'status': validators.FAILURE,
            'message': 'message test',
        }

        self.assertEqual(result, expected)

    def test_format_success(self):
        result = validators.format_success('message {}', 'test')

        expected = {
            'status': validators.SUCCESS,
            'message': 'message test',
        }

        self.assertEqual(result, expected)

    def test_format_result(self):
        status = validators.SUCCESS

        result = validators.format_result('message {}', 'test', status=status)

        expected = {
            'status': status,
            'message': 'message test',
        }

        self.assertEqual(result, expected)

#! /usr/bin/env python

import cdms2
import cwt
import pytest

class ProcessBase(object):
    def get_inputs(self, data):
        variable = data['variable']

        files = data['files']

        return [cwt.Variable(x, variable) for x in files]

    def get_domain(self, data):
        domain = data.get('domain', None)

        if domain is None:
            return

        return cwt.Domain(**domain)

    def validate_shape(self, output, expected_shape):
        with cdms2.open(output.uri) as infile:
            output_shape = infile[output.var_name].shape

        assert output_shape == expected_shape

    def run_validations(self, output, data):
        validations = data.get('validations', {})

        for name, value in validations.iteritems():
            if name.lower() == 'shape':
                self.validate_shape(output, value)

    def run_test(self, context, request, data):
        client = context.get_client_token()

        process = client.processes('.*\.{!s}'.format(self.identifier))[0]

        inputs = self.get_inputs(data)

        domain = self.get_domain(data)

        client.execute(process, inputs, domain)

        assert process.wait(timeout=20*60)

        self.run_validations(process.output, data)

        context.set_data_inputs(request, inputs, domain, process)

    @pytest.mark.stress
    def test_stress(self, context, request):
        self.run_test(context, request, self.stress)

    @pytest.mark.performance
    def test_performance(self, context, request):
        self.run_test(context, request, self.performance)

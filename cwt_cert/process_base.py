#! /usr/bin/env python

import cdms2
import cwt
import datetime

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

    def test_performance(self, context):
        client = context.get_client_token()

        process = client.processes('.*\.{!s}'.format(self.identifier))[0]

        inputs = self.get_inputs(self.performance)

        domain = self.get_domain(self.performance)

        start = datetime.datetime.now()

        client.execute(process, inputs, domain)

        assert process.wait(timeout=240)

        elapsed = datetime.datetime.now() - start

        self.run_validations(process.output, self.performance)

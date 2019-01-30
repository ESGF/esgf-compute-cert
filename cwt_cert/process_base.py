#! /usr/bin/env python

import cdms2
import cwt
import pytest

# https://aims3.llnl.gov/thredds/catalog/esgcet/239/CMIP6.CMIP.NASA-GISS.GISS-E2-1-G.amip.r1i1p1f1.Amon.tas.gn.v20181016.html#CMIP6.CMIP.NASA-GISS.GISS-E2-1-G.amip.r1i1p1f1.Amon.tas.gn.v20181016

TAS = [
    'https://aims3.llnl.gov/thredds/dodsC/css03_data/CMIP6/CMIP/NASA-GISS/GISS-E2-1-G/amip/r1i1p1f1/Amon/tas/gn/v20181016/tas_Amon_GISS-E2-1-G_amip_r1i1p1f1_gn_185001-190012.nc',
    'https://aims3.llnl.gov/thredds/dodsC/css03_data/CMIP6/CMIP/NASA-GISS/GISS-E2-1-G/amip/r1i1p1f1/Amon/tas/gn/v20181016/tas_Amon_GISS-E2-1-G_amip_r1i1p1f1_gn_190101-195012.nc',
    'https://aims3.llnl.gov/thredds/dodsC/css03_data/CMIP6/CMIP/NASA-GISS/GISS-E2-1-G/amip/r1i1p1f1/Amon/tas/gn/v20181016/tas_Amon_GISS-E2-1-G_amip_r1i1p1f1_gn_195101-200012.nc',
    'https://aims3.llnl.gov/thredds/dodsC/css03_data/CMIP6/CMIP/NASA-GISS/GISS-E2-1-G/amip/r1i1p1f1/Amon/tas/gn/v20181016/tas_Amon_GISS-E2-1-G_amip_r1i1p1f1_gn_200101-201412.nc',
]

TAS_SIZE = (1980, 90, 144)

# https://aims3.llnl.gov/thredds/catalog/esgcet/239/CMIP6.CMIP.NASA-GISS.GISS-E2-1-G.amip.r1i1p1f1.Amon.ta.gn.v20181016.html#CMIP6.CMIP.NASA-GISS.GISS-E2-1-G.amip.r1i1p1f1.Amon.ta.gn.v20181016

TA = [
    'https://aims3.llnl.gov/thredds/dodsC/css03_data/CMIP6/CMIP/NASA-GISS/GISS-E2-1-G/amip/r1i1p1f1/Amon/ta/gn/v20181016/ta_Amon_GISS-E2-1-G_amip_r1i1p1f1_gn_185001-190012.nc',
    'https://aims3.llnl.gov/thredds/dodsC/css03_data/CMIP6/CMIP/NASA-GISS/GISS-E2-1-G/amip/r1i1p1f1/Amon/ta/gn/v20181016/ta_Amon_GISS-E2-1-G_amip_r1i1p1f1_gn_190101-195012.nc',
    'https://aims3.llnl.gov/thredds/dodsC/css03_data/CMIP6/CMIP/NASA-GISS/GISS-E2-1-G/amip/r1i1p1f1/Amon/ta/gn/v20181016/ta_Amon_GISS-E2-1-G_amip_r1i1p1f1_gn_195101-200012.nc',
    'https://aims3.llnl.gov/thredds/dodsC/css03_data/CMIP6/CMIP/NASA-GISS/GISS-E2-1-G/amip/r1i1p1f1/Amon/ta/gn/v20181016/ta_Amon_GISS-E2-1-G_amip_r1i1p1f1_gn_200101-201412.nc',
]

TA_SIZE = (1980, 19, 90, 144)

# https://aims3.llnl.gov/thredds/catalog/esgcet/238/CMIP6.CMIP.NASA-GISS.GISS-E2-1-G.1pctCO2.r1i1p1f1.Amon.clt.gn.v20180905.html#CMIP6.CMIP.NASA-GISS.GISS-E2-1-G.1pctCO2.r1i1p1f1.Amon.clt.gn.v20180905

CLT = [
    'https://aims3.llnl.gov/thredds/dodsC/css03_data/CMIP6/CMIP/NASA-GISS/GISS-E2-1-G/1pctCO2/r1i1p1f1/Amon/clt/gn/v20180905/clt_Amon_GISS-E2-1-G_1pctCO2_r1i1p1f1_gn_185001-190012.nc',
    'https://aims3.llnl.gov/thredds/dodsC/css03_data/CMIP6/CMIP/NASA-GISS/GISS-E2-1-G/1pctCO2/r1i1p1f1/Amon/clt/gn/v20180905/clt_Amon_GISS-E2-1-G_1pctCO2_r1i1p1f1_gn_190101-195012.nc',
    'https://aims3.llnl.gov/thredds/dodsC/css03_data/CMIP6/CMIP/NASA-GISS/GISS-E2-1-G/1pctCO2/r1i1p1f1/Amon/clt/gn/v20180905/clt_Amon_GISS-E2-1-G_1pctCO2_r1i1p1f1_gn_195101-200012.nc',
]

CLT_SIZE = (1812, 90, 144)

class ProcessBase(object):
    def validate_shape(self, output, expected_shape):
        with cdms2.open(output.uri) as infile:
            output_shape = infile[output.var_name].shape

        assert output_shape == expected_shape

    def run_validations(self, output, validations):
        for name, value in validations.iteritems():
            if name.lower() == 'shape':
                self.validate_shape(output, value)

    def execute(self, context, request, client, identifier, files, variable, domain, **kwargs):
        process = client.processes(identifier)[0]

        domain = None if domain is None else cwt.Domain(**domain)

        inputs = [cwt.Variable(x, variable) for x in files]

        client.execute(process, inputs, domain)

        context.set_data_inputs(request, inputs, domain, process)

        return process

    def run_test(self, context, request, identifier, files, variable, domain, validations):
        client = context.get_client_token()

        process = self.execute(context, request, client, identifier, files, variable, domain)

        assert process.wait(timeout=20*60)

        self.run_validations(process.output, validations)

    @pytest.mark.stress
    def test_stress(self, context, request):
        self.run_test(context, request, self.identifier, **self.stress)

    @pytest.mark.performance
    def test_performance(self, context, request):
        self.run_test(context, request, self.identifier, **self.performance)

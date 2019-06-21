#! /usr/bin/env python

# flake8: noqa: E501

from builtins import object
import contextlib
from collections import OrderedDict

import cdms2
import cwt
import numpy as np
import pytest

# https://aims3.llnl.gov/thredds/catalog/esgcet/239/CMIP6.CMIP.NASA-GISS.GISS-E2-1-G.amip.r1i1p1f1.Amon.tas.gn.v20181016.html#CMIP6.CMIP.NASA-GISS.GISS-E2-1-G.amip.r1i1p1f1.Amon.tas.gn.v20181016
# 1980, 90, 144

TAS = [
    'https://aims3.llnl.gov/thredds/dodsC/css03_data/CMIP6/CMIP/NASA-GISS/GISS-E2-1-G/amip/r1i1p1f1/Amon/tas/gn/v20181016/tas_Amon_GISS-E2-1-G_amip_r1i1p1f1_gn_185001-190012.nc',
    'https://aims3.llnl.gov/thredds/dodsC/css03_data/CMIP6/CMIP/NASA-GISS/GISS-E2-1-G/amip/r1i1p1f1/Amon/tas/gn/v20181016/tas_Amon_GISS-E2-1-G_amip_r1i1p1f1_gn_190101-195012.nc',
    'https://aims3.llnl.gov/thredds/dodsC/css03_data/CMIP6/CMIP/NASA-GISS/GISS-E2-1-G/amip/r1i1p1f1/Amon/tas/gn/v20181016/tas_Amon_GISS-E2-1-G_amip_r1i1p1f1_gn_195101-200012.nc',
    'https://aims3.llnl.gov/thredds/dodsC/css03_data/CMIP6/CMIP/NASA-GISS/GISS-E2-1-G/amip/r1i1p1f1/Amon/tas/gn/v20181016/tas_Amon_GISS-E2-1-G_amip_r1i1p1f1_gn_200101-201412.nc',
]

# https://aims3.llnl.gov/thredds/catalog/esgcet/239/CMIP6.CMIP.NASA-GISS.GISS-E2-1-G.amip.r1i1p1f1.Amon.ta.gn.v20181016.html#CMIP6.CMIP.NASA-GISS.GISS-E2-1-G.amip.r1i1p1f1.Amon.ta.gn.v20181016
# 1980, 90, 144

TA = [
    'https://aims3.llnl.gov/thredds/dodsC/css03_data/CMIP6/CMIP/NASA-GISS/GISS-E2-1-G/amip/r1i1p1f1/Amon/ta/gn/v20181016/ta_Amon_GISS-E2-1-G_amip_r1i1p1f1_gn_185001-190012.nc',
    'https://aims3.llnl.gov/thredds/dodsC/css03_data/CMIP6/CMIP/NASA-GISS/GISS-E2-1-G/amip/r1i1p1f1/Amon/ta/gn/v20181016/ta_Amon_GISS-E2-1-G_amip_r1i1p1f1_gn_190101-195012.nc',
    'https://aims3.llnl.gov/thredds/dodsC/css03_data/CMIP6/CMIP/NASA-GISS/GISS-E2-1-G/amip/r1i1p1f1/Amon/ta/gn/v20181016/ta_Amon_GISS-E2-1-G_amip_r1i1p1f1_gn_195101-200012.nc',
    'https://aims3.llnl.gov/thredds/dodsC/css03_data/CMIP6/CMIP/NASA-GISS/GISS-E2-1-G/amip/r1i1p1f1/Amon/ta/gn/v20181016/ta_Amon_GISS-E2-1-G_amip_r1i1p1f1_gn_200101-201412.nc',
]

# https://aims3.llnl.gov/thredds/catalog/esgcet/238/CMIP6.CMIP.NASA-GISS.GISS-E2-1-G.1pctCO2.r1i1p1f1.Amon.clt.gn.v20180905.html#CMIP6.CMIP.NASA-GISS.GISS-E2-1-G.1pctCO2.r1i1p1f1.Amon.clt.gn.v20180905
# 1812, 90, 144

CLT = [
    'https://aims3.llnl.gov/thredds/dodsC/css03_data/CMIP6/CMIP/NASA-GISS/GISS-E2-1-G/1pctCO2/r1i1p1f1/Amon/clt/gn/v20180905/clt_Amon_GISS-E2-1-G_1pctCO2_r1i1p1f1_gn_185001-190012.nc',
    'https://aims3.llnl.gov/thredds/dodsC/css03_data/CMIP6/CMIP/NASA-GISS/GISS-E2-1-G/1pctCO2/r1i1p1f1/Amon/clt/gn/v20180905/clt_Amon_GISS-E2-1-G_1pctCO2_r1i1p1f1_gn_190101-195012.nc',
    'https://aims3.llnl.gov/thredds/dodsC/css03_data/CMIP6/CMIP/NASA-GISS/GISS-E2-1-G/1pctCO2/r1i1p1f1/Amon/clt/gn/v20180905/clt_Amon_GISS-E2-1-G_1pctCO2_r1i1p1f1_gn_195101-200012.nc',
]


def build_time_axis(axis_id, vars):
    axis_data = []
    units = None
    attributes = None

    for var in vars:
        axis_index = var.getAxisIndex(axis_id)

        axis = var.getAxis(axis_index)

        if units is None:
            units = axis.units

        if attributes is None:
            attributes = axis.attributes.copy()

        axis = axis.clone()

        axis.toRelativeTime(units)

        axis_data.append(axis)

    return cdms2.MV2.axisConcatenate(axis_data, id=axis_id, attributes=attributes)

def validate_axes(context, files, variable, domain, output):
    with contextlib.ExitStack() as stack:
        handles = [stack.enter_context(cdms2.open(x)) for x in files]

        vars = [x[variable] for x in handles]

        axes = []

        for axis in vars[0].getAxisList():
            if axis.isTime():
                axis_data = build_time_axis(axis.id, vars)
            else:
                axis_data = axis.clone()

            try:
                dim = domain.get(axis.id, None)
            except AttributeError:
                dim = None

            if dim is None:
                axes.append(axis_data)
            elif isinstance(dim, slice):
                axes.append(axis_data.subAxis(dim.start, dim.stop, dim.step or 1))
            elif isinstance(dim, (list, tuple)):
                mapped = axis_data.mapInterval((dim[0], dim[1]))

                try:
                    step = dim[2]
                except IndexError:
                    step = 1

                axes.append(axis_data.subAxis(mapped[0], mapped[1], step or 1))

    with cdms2.open(output.uri) as remote:
        output_shape = remote[output.var_name].shape

        output_axes = [x.clone()[:] for x in remote[output.var_name].getAxisList()]

    for x, y in zip(axes, output_axes):
        assert np.all(x == y)

class TestBase(object):
    def execute(self, context, request, client, identifier, files, variable, domain, **kwargs):
        identifier = context.format_identifier(identifier)

        process = client.process_by_name(identifier)

        assert process is not None, 'Missing process {!r}'.format(identifier)

        domain = None if domain is None else cwt.Domain(**domain)

        inputs = [cwt.Variable(x, variable) for x in files]

        client.execute(process, inputs, domain)

        context.set_data_inputs(request, inputs, domain, process)

        return process

    def run_test(self, context, request, identifier, files, variable, domain, validations):
        client = context.get_client_token()

        process = self.execute(context, request, client, identifier, files, variable, domain)

        assert process.wait(timeout=20*60)

        for validation in validations:
            validation(context, files, variable, domain, process.output)

    def run_multiple_tests(self, context, request, identifier, tests):
        for test in tests:
            self.run_test(context, request, identifier, **test)

    @pytest.mark.api_compliance
    def test_api_compliance(self, context, request):
        self.run_multiple_tests(context, request, self.identifier, self.api_compliance)

    @pytest.mark.performance
    def test_performance(self, context, request):
        self.run_test(context, request, self.identifier, **self.performance)

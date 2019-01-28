#! /usr/bin/env python

from process_base import ProcessBase

# Source THREDDS Catalogs
# https://aims3.llnl.gov/thredds/catalog/esgcet/239/CMIP6.CMIP.NASA-GISS.GISS-E2-1-G.amip.r1i1p1f1.Amon.ta.gn.v20181016.html#CMIP6.CMIP.NASA-GISS.GISS-E2-1-G.amip.r1i1p1f1.Amon.ta.gn.v20181016
# https://aims3.llnl.gov/thredds/catalog/esgcet/238/CMIP6.CMIP.NASA-GISS.GISS-E2-1-G.1pctCO2.r1i1p1f1.Amon.clt.gn.v20180905.html#CMIP6.CMIP.NASA-GISS.GISS-E2-1-G.1pctCO2.r1i1p1f1.Amon.clt.gn.v20180905
# https://aims3.llnl.gov/thredds/catalog/esgcet/239/CMIP6.CMIP.NASA-GISS.GISS-E2-1-G.amip.r1i1p1f1.Amon.tas.gn.v20181016.html#CMIP6.CMIP.NASA-GISS.GISS-E2-1-G.amip.r1i1p1f1.Amon.tas.gn.v20181016

class TestSubset(ProcessBase):
    identifier = 'subset'

    performance = {
        'variable': 'ta',
        'files': [
            'https://aims3.llnl.gov/thredds/dodsC/css03_data/CMIP6/CMIP/NASA-GISS/GISS-E2-1-G/amip/r1i1p1f1/Amon/ta/gn/v20181016/ta_Amon_GISS-E2-1-G_amip_r1i1p1f1_gn_185001-190012.nc',
        ],
        'domain': {
            'lat': (-45, 45),
            'lon': (0, 180),
            'time': (10000, 11000),
            'plev': (40000, 20000),
        },
        'validations': {
            'shape': (33, 4, 46, 72)
        }
    }

    stress = [
        {
            'variable': 'ta',
            'files': [
                'https://aims3.llnl.gov/thredds/dodsC/css03_data/CMIP6/CMIP/NASA-GISS/GISS-E2-1-G/amip/r1i1p1f1/Amon/ta/gn/v20181016/ta_Amon_GISS-E2-1-G_amip_r1i1p1f1_gn_185001-190012.nc',
            ],
            'domain': {
                'lat': (-45, 45),
                'lon': (0, 180),
                'time': (10000, 11000),
                'plev': (40000, 20000),
            },
            'validations': {
                'shape': (33, 4, 46, 72)
            }
        },
        {
            'variable': 'clt',
            'files': [
                'https://aims3.llnl.gov/thredds/dodsC/css03_data/CMIP6/CMIP/NASA-GISS/GISS-E2-1-G/1pctCO2/r1i1p1f1/Amon/clt/gn/v20180905/clt_Amon_GISS-E2-1-G_1pctCO2_r1i1p1f1_gn_195101-200012.nc',
            ],
            'domain': {
                'lat': (-45, 45),
                'lon': (0, 180),
                'time': (44000, 47000),
            },
            'validations': {
                'shape': (98, 46, 72)
            }
        },
        {
            'variable': 'tas',
            'files': [
                'https://aims3.llnl.gov/thredds/dodsC/css03_data/CMIP6/CMIP/NASA-GISS/GISS-E2-1-G/amip/r1i1p1f1/Amon/tas/gn/v20181016/tas_Amon_GISS-E2-1-G_amip_r1i1p1f1_gn_185001-190012.nc',
            ],
            'domain': {
                'lat': (-45, 45),
                'lon': (0, 180),
                'time': (10000, 11000),
            },
            'validations': {
                'shape': (33, 46, 72)
            }
        },
    ]

#! /usr/bin/env python

from process_base import ProcessBase

# Source
# https://aims3.llnl.gov/thredds/catalog/esgcet/122/cmip3.NCAR.ncar_ccsm3_0.historical.mon.atmos.run1.tas.v1.html#cmip3.NCAR.ncar_ccsm3_0.historical.mon.atmos.run1.tas.v1

class TestAggregate(ProcessBase):
    identifier = 'aggregate'

    performance = {
        'variable': 'tas',
        'files': [
            'https://aims3.llnl.gov/thredds/dodsC/cmip3_data/data2/20c3m/atm/mo/tas/ncar_ccsm3_0/run1/tas_A1.20C3M_1.CCSM.atmm.1870-01_cat_1879-12.nc',
            'https://aims3.llnl.gov/thredds/dodsC/cmip3_data/data2/20c3m/atm/mo/tas/ncar_ccsm3_0/run1/tas_A1.20C3M_1.CCSM.atmm.1880-01_cat_1889-12.nc',
            'https://aims3.llnl.gov/thredds/dodsC/cmip3_data/data2/20c3m/atm/mo/tas/ncar_ccsm3_0/run1/tas_A1.20C3M_1.CCSM.atmm.1890-01_cat_1899-12.nc',
            'https://aims3.llnl.gov/thredds/dodsC/cmip3_data/data2/20c3m/atm/mo/tas/ncar_ccsm3_0/run1/tas_A1.20C3M_1.CCSM.atmm.1900-01_cat_1909-12.nc',
            'https://aims3.llnl.gov/thredds/dodsC/cmip3_data/data2/20c3m/atm/mo/tas/ncar_ccsm3_0/run1/tas_A1.20C3M_1.CCSM.atmm.1910-01_cat_1919-12.nc',
            'https://aims3.llnl.gov/thredds/dodsC/cmip3_data/data2/20c3m/atm/mo/tas/ncar_ccsm3_0/run1/tas_A1.20C3M_1.CCSM.atmm.1920-01_cat_1929-12.nc',
        ],
        'validations': {
            'shape': (720, 128, 256),
        }
    }

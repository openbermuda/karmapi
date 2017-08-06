"""
Interface to netcdf files
"""

import netCDF4

def load(path):

    return netCDF4.DataSet(path)

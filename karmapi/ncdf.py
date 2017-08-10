"""
Interface to netcdf files
"""
import datetime
import math

import netCDF4


def load(path):

    return netCDF4.Dataset(path)


def images(path, folder):

    df = load(path)

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

def generate_data(stamps, values):

    epoch = datetime.datetime(1900, 1, 1)
    
    for ix, stamp in enumerate(stamps):

        date = epoch + datetime.timedelta(hours=int(stamp))

        yield values[ix], date
    

        

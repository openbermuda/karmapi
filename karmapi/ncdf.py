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

    stamps = df.variables['time']

    epoch = datetime.date(1900, 1, 1)
    
    for ix, stamp in enumerate(stamps):

        date = epoch + datetime.timedelta(hours=stamp)

        yield values[ix], date
    

        

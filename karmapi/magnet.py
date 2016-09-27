"""
Geomagnetic data

ftp://ftp.ngdc.noaa.gov/STP/GEOMAGNETIC_DATA/INDICES/KP_AP/MONTHLY.FMT

"""

import datetime

import pandas

def timestamp(x):

    ym = int(x.yearmonth)

    return datetime.datetime(
        ym // 100, ym % 100, 1)
    

def load(infile):

    names = ['yearmonth', 'value']

    names += ['h{}'.format(x) for x in range(0, 24, 3)]

    names += ['character']


    df = pandas.read_csv(infile, sep='\s+', names=names,
                         header=None, index_col=False)

    df.index = df.apply(timestamp, axis=1)
    return df

"""
Working with USGS data

Raw data:

http://earthquake.usgs.gov/data/centennial/centennial_Y2K.CAT

README:  http://earthquake.usgs.gov/data/centennial/centennial_README.rtf

Stable Continental Regions:

http://earthquake.usgs.gov/data/scr_catalog.txt
"""
import datetime
import requests

URL = 'http://earthquake.usgs.gov/data/centennial/centennial_Y2K.CAT'

import pandas

def parse(record):
    """ Parse a record 

    For now, only picks up part of the data
    """

    casts = ([int] * 5) + ([float] * 7)

    fields = record[12:44].split()

    fields += record[44:70].split()

    row = []
    for field, cast in zip(fields, casts):
        row.append(cast(field))

    return row

def timestamp(x):

    if x.day == 0:
        x.day = 1
        
    return datetime.datetime(int(x.year), int(x.month), int(x.day),
                             int(x.hour), int(x.minute), int(x.second))

def load(infile):

    data = []
    for line in infile:
        data.append(parse(line))

    columns = ['year', 'month', 'day', 'hour', 'minute', 'second',
               'lat', 'lon', 'foo', 'bar', 'foobar', 'severity']

    df = pandas.DataFrame(data, columns=columns)

    # at least one date has 0 for the day :(
    df.day = df.day.clip_lower(1)

    fields = ['year', 'month', 'day', 'hour', 'minute', 'second']
    df.index = pandas.to_datetime(df[fields])
    
    return df

def get():

    data = requests.get(URL).content.decode()

    return load(data.split('\n')[:-1])
    

"""
Working with USGS data

Raw data:

http://earthquake.usgs.gov/data/centennial/centennial_Y2K.CAT

README:  http://earthquake.usgs.gov/data/centennial/centennial_README.rtf

Stable Continental Regions:

http://earthquake.usgs.gov/data/scr_catalog.txt
"""
import math
import datetime
import requests

URL = 'http://earthquake.usgs.gov/data/centennial/centennial_Y2K.CAT'

import pandas
import ephem

from karmapi import base

EPOCH = datetime.datetime(1900, 1, 1)

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

def timewarp(df):

    # at least one date has 0 for the day :(
    df.day = df.day.clip_lower(1)

    fields = ['year', 'month', 'day', 'hour', 'minute', 'second']
    df.index = pandas.to_datetime(df[fields])
    
    return df

def get():

    data = requests.get(URL).content.decode()

    return load(data.split('\n')[:-1])

def rows(df):
    """ generate observations """

    for row in df.itertuples():
        yield row

def moontime(dates, epoch=EPOCH):
    """ Convert dates to moontime 
    
    FIXME; calulate number of full moons since some epoch
    """
    return dates

def load(path):

    df = base.load(path)

    return timewarp(df)


def moon_phase(when):

    nmoon = ephem.next_full_moon(when).datetime()
    pmoon = ephem.previous_full_moon(when).datetime()
    
    month_seconds = (nmoon - pmoon).total_seconds()

    phase = (when - pmoon).total_seconds() / month_seconds

    return phase

def observation(row):
    """Turn a row into an observation 

    That is just a list of integers.

    Shorter vectors with the same information content a bonus.

    Or maybe a lack of variability giving a false confidence in the true information?

    For now, aim that each variable should have p states.  Primes might
    be good choices for number of states.

    """
    obs = []
    pi = math.pi

    # throw the year in, so we can sort of track time
    #obs.append(row.year)

    # now month, would be good to use new moon count + current phase?
    ix = row.Index
    
    obs.append(moon_phase(ix))

    # Conjure up time of day stamp
    otime = row.hour + ((row.minute) / 60)

    otime += row.second / (60 * 60)

    otime = int(otime)

    obs.append(otime)

    # ok now where?
    lat = row.lat
    lat = (lat + 90) / 15
    obs.append(int(lat))

    lon = row.lon
    lon = (lon + 180) / 15
    obs.append(int(lon))

    # how much?
    severity = row.severity
    obs.append(severity)
    
    #for x in dir(row.Index): print(x)
    #print(row.Index.toordinal())
    #obs.append(row.month)

    
    return obs

def main():

    import argparse
    from karmapi import tpot, sonogram

    Path = base.Path
    
    parser = argparse.ArgumentParser()

    parser.add_argument('--path', default='karmapi/data/quake/')
    parser.add_argument('--value', default='t2m')
    parser.add_argument('--raw', default='centennial')
    parser.add_argument('--date')
    parser.add_argument(
        '--pc', action='store_true',
        help='do principal components')

    parser.add_argument('--delta', action='store_true')
    parser.add_argument('--model', action='store_true')
    parser.add_argument('--offset', type=int, default=0)

    args = parser.parse_args()

    path = Path(args.path)

    df = load(path / args.raw)

    print(df.describe())
    print(df.info())
    print()

    observations = [observation(x) for x in rows(df)]

    print(len(observations))
    print(type(observations))

    data = []
    for row in rows(df):
        obs = observation(row)
        print(obs)
        data.append(tuple(obs))

    items = set()
    for item in data:
        items.add(tuple(item))

    print('number of items', len(items))

    # Build A, B, P0 and fill the tpot
    

        
    exit()


if __name__ == '__main__':


    main()

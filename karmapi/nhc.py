"""
ENSO

http://www.esrl.noaa.gov/psd/enso/mei/#content

"""
HURDAT = 'http://www.nhc.noaa.gov/data/hurdat/hurdat2-1851-2015-070616.txt'

import csv
import datetime

import pandas

BASINS = set(['AL', 'EP', 'CP'])

def hurdle(raw):
    """ Take a raw csv hurdat and convert into dataframe format

    Two types of records:

    header: name of storm, date, basin, number of records.
            becomes event info.

            Add an event id so we can go between that and the 
            remaining data

    Records:  Lots of fields all beautifully documented.
   
    """

    data = []
    events = []
    with raw.open() as infile:
        for row in csv.reader(infile):
            if row[0][:2] in BASINS:
                # header record for storm
                info = event_info(row)
                stormid = info['stormid']
                events.append(info)

            else:
                observation = observation_info(row)
                observation['stormid'] = stormid
                data.append(observation)

    events = pandas.DataFrame(events)
    data = pandas.DataFrame(data)

    return events, data     


def event_info(row):
    """ Parse out event meta data """
    basin = row[0][:2]
    stormid = int(row[0][2:])
    name = row[1].strip()
    observations = int(row[2])

    return dict(basin=basin, stormid=stormid,
                name=name, observations=observations)

def observation_info(row):
    """ Parse out observation data """

    date = row[0].strip()
    year = int(date[:4])
    month = int(date[4:6])
    day = int(date[6:8])

    time = row[1].strip()
    hour = int(time[:2])
    minute = int(time[2:4])

    timestamp = datetime.datetime(year, month, day, hour, minute)

    kind = row[2].strip()
    status = row[3].strip()
    
    # Fix the lat lon
    lat = float(row[4][:-1])
    if row[4][-1] == 'S':
        lat *= -1

    lon = float(row[5][:-1])
    if row[5][-1] == 'W':
        lon *= -1

    windspeed = get_value(row[6])
    pressure = get_value(row[7])

    info = dict(timestamp=timestamp,
                kind=kind,
                status=status,
                lat=lat,
                lon=lon,
                windspeed=windspeed,
                pressure=pressure)

    ix = 8
    template = '{quad}{radius}kt'
    for radius in (34, 50, 64):
        for quad in ('ne', 'se', 'sw', 'nw'):
            value = get_value(row[ix])

            info[template.format(**locals())] = value
            
    return info
                
def get_value(field):

    value = float(field)
    if value == -999:
        value = None
    return value


def read_raw_mei(path):

    df = pandas.read_csv(path, sep=' ')

    return df

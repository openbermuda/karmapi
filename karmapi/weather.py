""" Load weather data into karma pi

Creates meta data too.

Start date:

1979-1-1

lat 90.0 to -90.0, 0.75

lon 0 to 359.25, 0.75

Year, day, month.
"""
import os
import datetime
import struct
from io import StringIO
from functools import wraps
from pathlib import Path

import numpy

from .base import (
    get, build, match_path, Parms, get_all_meta_data,
    create_folder_if_missing, day_range)

from .locations import Location
from .maps import location

# FIXME -- the following constants belong in meta data

# First data in the raw data
START_DAY = datetime.date(1979, 1, 1)

# End day is first day not in the raw data
END_DAY = datetime.date(2016, 1, 1)

DELTA = 0.75
DELTA_LATITUDE = DELTA_LONGITUDE = DELTA

LATITUDE_START = 90.0
LONGITUDE_START = 0.0


class RawWeather:

    def __init__(self,
                 start_day=START_DAY,
                 end_day=END_DAY,
                 delta_latitude=DELTA_LATITUDE,
                 delta_longitude=DELTA_LONGITUDE,
                 latitude_start=LATITUDE_START,
                 longitude_start=LONGITUDE_START):
        """ Set parameters """
        self.start_day = start_day
        self.end_day = end_day
        self.delta_longitude = delta_longitude
        self.delta_latitude = delta_latitude
        self.longitude_start = longitude_start
        self.latitude_start = latitude_start


    def from_dict(self, data):
        """ Hack to build from meta data """
        self.__dict__.update(data)
        
        if type(self.start_day) == int:
            self.start_day = datetime.date(
                self.start_year,
                self.start_month,
                self.start_day)
            
        if type(self.end_day) == int:
            self.end_day = datetime.date(
                self.end_year,
                self.end_month,
                self.end_day)

    
    def records_per_day(self):
        """ One record per lat and lon """
        
        return self.number_of_longitudes() * self.number_of_latitudes()

    def number_of_longitudes(self):
        """ Number of longitudes in the grid """
        return int(360 / self.delta_longitude)
     
    def number_of_latitudes(self):
        """ Number of latitudes in the grid """
        return int(1 + (180 / self.delta_latitude))

    def longitudes(self):
        """ Return list of longitudes """
        lons = []

        lon = 0.0
        while lon < 360.0:
            lons.append(lon)
            lon += self.delta_longitude
        return lons

    def latitudes(self):
        """ Return list of longitudes """
        lats = []

        lat = 90.0
        while lat >= -90.0:
            lats.append(lat)
            lat -= self.delta_latitude
        return lats

    def latitude_index(self, lat):
        """ Convert a latitude to index in the grid 

        Returns index of nearest grid latitude to the 
        north of given lat.
        """
        return int((self.latitude_start - lat) / self.delta_latitude)

    def longitude_index(self, lon):
        """ Convert a longitude to index in the grid

        Returns index of nearest grid longitude to the 
        west of given lon.
        """

        return int((lon - self.longitude_start) / self.delta_longitude)

    def calculate_record_number(self, date, lat=90, lon=0.0,
                                start=None):
        """  Calculate the record number for given date, lat, lon """
        if start is None:
            start = self.start_day

        days = (date - start).days

        lat_index = self.latitude_index(lat)

        lon_index = self.longitude_index(lon)

        number = days * self.records_per_day()
        number += lon_index * self.number_of_latitudes()
        number += lat_index

        return number

    def get_data(self, date, infile, size=9):
        """ Pull out all data for the given date

        date: the date to pull data for

        infile: file object containing the data

        size: number of bytes per value.
        """
        pos = self.calculate_record_number(date)

        infile.seek(pos * size)

        # data is one value per csv line
        data = infile.read(size * self.records_per_day())

        return [float(x) for x in data.split()]


    def day_to_numpy(self, data):
    
        ndata = numpy.array(data)
        ndata = ndata.reshape(self.number_of_longitudes(),
                              self.number_of_latitudes()).T
        return ndata


def build_day(parms):
    """ Copy data over from raw files into day folders 

    Assume path is relative to current working directory.
    """
    base_path = Path(parms.base)

    path = base_path / parms.path
    create_folder_if_missing(path)

    # now do what we have to do
    day = datetime.date(int(parms.year),
                        int(parms.month),
                        int(parms.day))

    # extract the source data from the parms
    source = parms.target['source'].format(field=parms.field)
    fsource = base_path / source

    # get the meta data for the source
    source_meta = get_all_meta_data(fsource)
    raw = RawWeather()
    raw.from_dict(source_meta)

    # Read the source data
    with fsource.open() as infile:
        data = raw.get_data(day, infile)

    # Write the data out
    with path.open('wb') as outfile:
        write_array(outfile, data)

def build_time(parms):
    """ Copy data over from raw files into day folders 

    Assume path is relative to current working directory.
    """
    meta = get_all_meta_data(parms.base)

    raw = RawWeather()
    raw.from_dict(meta)
        
    for day in day_range(raw.start_day, raw.end_day):
        print(day)
        parms.year = day.year
        parms.month = day.month
        parms.day = day.day

        parms.path = "time/{day:%Y/%m/%d}/{field}".format(
            day=day,
            field=parms.field)
        print(parms.path)
        build_day(parms)

def next_month(date):
    
    year = date.year
    month = date.month
    
    month += 1
    if month > 12:
        year +=1
        month = 1
        
    return datetime.date(year, month, 1)

def build_month(parms):
    """ Sum all the days in the month 

    Create some stats on the totals
    """
    meta = Parms(get_all_meta_data(parms.base))
    base_path = Path(parms.base)

    start = datetime.date(parms.year, parms.month, 1)
    end = next_month(start)

    totals = numpy.zeros(len(meta.lats) * len(meta.lons))
    path = 'time/{}/{:02d}/{:02d}/{}'
    aday = datetime.timedelta(days=1)

    for day in day_range(start, end):
        data = get_array_for_path(base_path /
                path.format(day.year, day.month, day.day, parms.field))
        totals += data

    totals /= (end - start).days

    # save totals
    path = base_path / parms.path
    create_folder_if_missing(path)

    with path.open('wb') as outfile:
        
        write_array(outfile, totals)

def build_months(parms):
    """ Create monthly totals for each month of data
    """
    meta = Parms(get_all_meta_data(parms.base))

    month = datetime.date(meta.start_year, meta.start_month, 1)
    end = datetime.date(meta.end_year, meta.end_month, 1)
    while month < end:
        print(month)
        parms.month = month.month
        parms.year = month.year

        parms.path = "month/{month:%Y/%m}/{field}".format(
            month=month,
            field=parms.field)

        build_month(parms)

        month = next_month(month)
        

def build_year(path):
    """ Sum all the days in the year """
    raise NotImplemented

def build_latitude(parms):
    """ Extract all the data for a given latitude.

    This then allows us to get the data for any lat/lon
    quickly.

    Alternatively, use build_space and do everythng in one.
    """
    base_path = Path(parms.base)
    
    path = base_path / parms.path
    create_folder_if_missing(path)

    # now do what we have to do
    lat = int(parms.lat)

    # get raw weather object
    meta = get_all_meta_data('.')
    raw = RawWeather()
    raw.from_dict(meta)
    
    lat_index = raw.latitude_index(parms.lat)

    # this is going to be slow, we have to read
    # the data for every day to get all the data for a latitude
    # figure out a template for the path to day data
    path_parts = path.parts

    stride = raw.number_of_latitudes()
    with path.open('wb') as outfile:

        for day in day_range(raw.start_day, raw.end_day):
            print(day)
            # Get the day's data
            day_path = "{base}/time/{day:%Y/%m/%d}/{field}".format(
                base=parms.base,
                day=day,
                field=parms.field)

            data = get_array_for_path(day_path)

            # extract stuff for this latitude
            lat_data = data[lat_index::stride]

            # format it with struct and write to outfile
            write_array(outfile, lat_data)


def build_space(parms):
    """ Extract all the data for all latitudes.

    This then allows us to get the data for any lat/lat
    quickly
    """
    base_path = Path(parms.base)
    path = parms.path
    create_folder_if_missing(base_path / path)

    # get raw weather object
    meta = get_all_meta_data('.')
    raw = RawWeather()
    raw.from_dict(meta)

    # create all the folders we need
    paths = []
    for lat in raw.latitudes():

        path = "space/{lat:.2f}/{field}".format(
            lat=lat, field=parms.field)
        fpath = base_path / path
        create_folder_if_missing(fpath)
        paths.append(fpath)
    
    nlats = raw.number_of_latitudes()

    # this is going to be slow, we have to read
    # the data for every day to get all the data for a latitude

    # figure out a template for the path to day data
    path_parts = path.parts

    outfiles = [path.open('wb') for path in paths]

    for day in day_range(raw.start_day, raw.end_day):

        print(day)
        # Get the day's data
        day_path = "time/{day:%Y/%m/%d}/{field}".format(
            base=parms.base,
            day=day,
            field=parms.field)

        data = get_array_for_path(base_path / day_path)

        # extract stuff for this latitude
        for (outfile, lat) in zip(outfiles, raw.latitudes()):
            lat_index = raw.latitude_index(lat)
            lat_data = data[lat_index::nlats]

            # format it with struct and write to outfile
            write_array(outfile, lat_data)

    # now close the outfiles
    for outfile in outfiles:
        outfile.close()


def get_lat(lat, field, base):
    """  Get all the data for a given latitude and field """

    # Read the data for the lat
    path = "space/{lat:.2f}/{field}".format(
        lat=lat, field=field)

    return get_array_for_path(Path(base) / path)

            
def get_lat_lon(parms):
    """  Get all the data for a given lat/lon and field """

    data = get_lat(parms.lat, parms.field, parms.base)

    # Now find the index for this lat
    # get raw weather object
    meta = get_all_meta_data('.')
    raw = RawWeather()
    raw.from_dict(meta)

    longitude_index = raw.longitude_index(parms.lon)

    return data[longitude_index::raw.number_of_longitudes()]

def get_grid(parms):
    """ Get all the data for a lat/lon grid """
    # get raw weather object
    meta = get_all_meta_data('.')
    raw = RawWeather()
    raw.from_dict(meta)

    # extract parameters and convert lats/lons to indices
    min_lat = raw.latitude_index(parms.min_lat)
    max_lat = raw.latitude_index(parms.max_lat)
    min_lon = raw.longitude_index(parms.min_lon)
    max_lon = raw.longitude_index(parms.max_lon)

    if min_lat > max_lat:
        min_lat, max_lat = max_lat, min_lat

    if min_lon > max_lon:
        min_lon, max_lon = max_lon, min_lon

    field = parms.field

    result = {}
    result['field'] = field
    result['start_day'] = raw.start_day
    result['end_day'] = raw.end_day
    result['lats'] = raw.latitudes()[min_lat:max_lat]
    result['lons'] = raw.longitudes()[min_lon:max_lon]

    # loop round required latitudues
    data = []
    for lat in raw.latitudes()[min_lat:max_lat]:
        lat_data = get_lat(lat, field, parms.base)

        for lon in range(min_lon, max_lon):
            data += lat_data[lon::raw.number_of_longitudes()]

    result['values'] = data

    return result

def array_to_dict(f, keyword='data', *args, **kwargs):
    """ Decorator that wraps a function that returns an array 

    This is just a utility that allows us to wrap functions
    that return arrays but have the docstring of the original
    function to be preserved.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):

        result = f(*args, **kwargs)

        return {keyword: result}
    
    return wrapper

get_lat_lon_field = array_to_dict(get_lat_lon)

def get_all_for_lat_lon(parms):
    """ Get all fields for a specific lat/lon """
    meta = get_all_meta_data(parms.base)

    data = {}
    for field in meta['fields']:
        parms.field = field
        data[field] = get_lat_lon(parms)

    return data

def get_all_for_day(parms):
    """ Get all fields for a specific date """
    meta = get_all_meta_data(parms.base)

    data = {}
    path = parms.path
    for field in meta['fields']:
        parms.path = '/'.join([path, field])
        data[field] = get_array(parms)

    return data

def get_array(parms):

    return get_array_for_path(Path(parms.base) / parms.path)

def get_array_as_dict(parms):
    """ Returns data for a path 

    Assumes the data is just an array of floats.
    """
    return dict(data=get_array_for_path(
        Path(parms.base) / parms.path))

def get_array_for_path(path):
    """ Return data as an array """
    with open(str(path), 'rb') as infile:
        data = infile.read()

    unpack = struct.Struct("{}f".format(int(len(data)/4)))

    return unpack.unpack(data)


def write_array(outfile, data):
    """ Write out an array of floats """
    
    pack = struct.Struct("{}f".format(len(data)))
    outfile.write(pack.pack(*data))

def write_lats_for_day(data, date, outfiles):
    
    packer = struct.Struct('{}f'.format(weather.latitudes()))

    for ix in range(weather.latitudes()):
    
        col = data[:, ix]
        pdata = packer.pack(*col)
    
        outfiles[ix].write(pdata)


    

    
    

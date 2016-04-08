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
import numpy

from .base import (
    build, match_path, Parms, get_all_meta_data,
    create_folder_if_missing)
                   

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
    path = parms.path
    create_folder_if_missing(path)

    # now do what we have to do
    day = datetime.date(int(parms.year),
                        int(parms.month),
                        int(parms.day))

    # extract the source data from the parms
    source = parms.target['source'].format(field=parms.field)

    # get the meta data for the source
    source_meta = get_all_meta_data(source)
    raw = RawWeather(**source_meta)

    # Read the source data
    with open(source) as infile:
        data = raw.get_data(day, infile)

    # Write the data out
    with open(path, 'wb') as outfile:
        write_array(outfile, data)

def build_time(parms):
    """ Copy data over from raw files into day folders 

    Assume path is relative to current working directory.
    """
    meta = get_all_meta_data('.')

    raw = RawWeather()
    raw.from_dict(meta)
        
    aday = datetime.timedelta(days=1)
    day = raw.start_day
    while day < raw.end_day:
        print(day)
        parms.year = day.year
        parms.month = day.month
        parms.day = day.day

        parms.path = "time/{day:%Y/%m/%d}/{field}".format(
            day=day,
            field=parms.field)
        print(parms.path)
        build_day(parms)

        # go to next day
        day += aday


def build_month(path):
    """ Sum all the days in the month 

    Create some stats on the totals
    """
    target = "year/{year}/{month}/{day}/{field}"
    # load meta data for raw file
    parms, path = match_path(path, target)

    raise NotImplemented


def build_year(path):
    """ Sum all the days in the year """
    raise NotImplemented

def build_latitude(parms):
    """ Extract all the data for a given latitude.

    This then allows us to get the data for any lat/lon
    quickly.

    Alternatively, use build_space and do everythng in one.
    """
    path = parms.path
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
    day = raw.start_day
    aday = datetime.timedelta(days=1)

    # figure out a template for the path to day data
    path_parts = path.split('/')
    inpath = '/'.join(path_parts[:-3])

    stride = raw.number_of_longitudes()
    with open(path, 'wb') as outfile:

        while day < raw.end_day:
            print(day)
            # Get the day's data
            day_path = "time/{day:%Y/%m/%d}/{field}".format(
                base=parms.base,
                day=day,
                field=parms.field)

            data = get_array_for_path(day_path)

            # extract stuff for this latitude
            lat_data = data[lat_index::stride]

            # format it with struct and write to outfile
            write_array(outfile, lat_data)

            # go to next day
            day += aday

def build_space(parms):
    """ Extract all the data for all latitudes.

    This then allows us to get the data for any lat/lat
    quickly
    """
    path = parms.path
    create_folder_if_missing(path)

    # get raw weather object
    meta = get_all_meta_data('.')
    raw = RawWeather()
    raw.from_dict(meta)

    # create all the folders we need
    paths = []
    for lat in raw.latitudes():

        path = "space/{lat:.2f}/{field}".format(
            lat=lat, field=parms.field)
        create_folder_if_missing(path)
        paths.append(path)
    
    nlats = raw.number_of_latitudes()

    # this is going to be slow, we have to read
    # the data for every day to get all the data for a latitude
    day = raw.start_day
    aday = datetime.timedelta(days=1)

    # figure out a template for the path to day data
    path_parts = path.split('/')
    inpath = '/'.join(path_parts[:-3])

    outfiles = [open(path, 'wb') for path in paths]

    while day < raw.end_day:

        print(day)
        # Get the day's data
        day_path = "time/{day:%Y/%m/%d}/{field}".format(
            base=parms.base,
            day=day,
            field=parms.field)

        data = get_array_for_path(day_path)

        # extract stuff for this latitude
        for (outfile, lat) in zip(outfiles, raw.latitudes()):
            lat_index = raw.latitude_index(lat)
            lat_data = data[lat_index::nlats]

            # format it with struct and write to outfile
            write_array(outfile, lat_data)

        # go to next day
        day += aday

    # now close the outfiles
    for outfile in outfiles:
        outfile.close()

            
def get_lat_lon(parms):
    """  Get all the data for a given lat/lon and field """

    # Read the data for the lat
    path = "space/{lat:.2f}/{field}".format(
        lat=parms.lat, field=parms.field)

    data = get_array_for_path(path)

    # Now find the index for this lat
    # get raw weather object
    meta = get_all_meta_data('.')
    raw = RawWeather()
    raw.from_dict(meta)

    latitude_index = raw.latitude_index(parms.lat)

    return data[latitude_index::raw.number_of_latitudes()]

def get_all_for_lat_lon(parms):
    """ Get all fields for a specific lat/lon """
    meta = get_all_meta_data('.')

    data = {}
    for field in meta['fields']:
        parms.field = field
        data[field] = get_lat_lon(parms)

    return data

def get_all_for_day(parms):
    """ Get all fields for a specific date """
    meta = get_all_meta_data('.')

    data = {}
    for field in meta['fields']:
        parms.field = field
        data[field] = get_day(parms)

    return data

def get_array(parms):

    return get_array_for_path(parms.path)

def get_array_as_dict(parms):

    return dict(data=get_array_for_path(parms.path))

def get_array_for_path(path):
    """ Return data as an array """
    with open(path, 'rb') as infile:
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

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
    get, build, match_path, Parms, get_all_meta_data,
    create_folder_if_missing, full_path)
                   

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
    path = full_path(parms.base, parms.path)
    create_folder_if_missing(path)

    # now do what we have to do
    day = datetime.date(int(parms.year),
                        int(parms.month),
                        int(parms.day))

    # extract the source data from the parms
    source = parms.target['source'].format(field=parms.field)

    # get the meta data for the source
    source_meta = get_all_meta_data(full_path(parms.base, source))
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
    meta = get_all_meta_data(parms.base)

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
    path = full_path(parms.base, parms.path)
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
        paths.append(full_path(parms.base, path))
    
    nlats = raw.number_of_latitudes()

    # this is going to be slow, we have to read
    # the data for every day to get all the data for a latitude
    day = raw.start_day
    aday = datetime.timedelta(days=1)

    # figure out a template for the path to day data
    path_parts = path.split('/')

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

    data = get_array_for_path(full_path(parms.base, path))

    # Now find the index for this lat
    # get raw weather object
    meta = get_all_meta_data('.')
    raw = RawWeather()
    raw.from_dict(meta)

    latitude_index = raw.latitude_index(parms.lat)

    return data[latitude_index::raw.number_of_latitudes()]

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
    meta = get_all_meta_data('.')

    data = {}
    for field in meta['fields']:
        parms.field = field
        data[field] = get_day(parms)

    return data

def get_array(parms):

    return get_array_for_path(parms.path)

def get_array_as_dict(parms):

    return dict(data=get_array_for_path(
        full_path(parms.base, parms.path)))

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


def location(parms):
    """Rough notes on how to plot centred on a location using basemap

    What I really want to do is implement a Karma Pi path something like
    this:

    locations/{location}/{item}

    That will show you {item} from location's point of view.

    Now {item} works best if it does not have and /'s, so for
    the item parameter we'll convert /'s to ,'s and see how that looks.

    The idea is {item} will be a path to something in Karma Pi.

    So here is how it might go:

    >>> parms = base.Parms()
    >>> parms.path = "locations/bermuda"
    >>> parms.item = "time,2015,11,01,precipitation,image"

    >>> data = location(parms)

    In the background, some magic will read lat/lon for 
    locations/bermuda, or rather read the meta data and hope the 
    info is there.

    It will find the data for the precipitation image and use it to 
    create an image of the data using the "ortho" projection in basemap.

    This shows a hemisphere of the world, centered on the location.

    It would be good to offer other views.

    This can be supported by adding different end points for each view

    Eg:

    >>> parms = base.Parms()
    >>> parms.path = "locations/bermuda"
    >>> parms.item = "time,2015,11,01,precipitation,mercator"
    
    Might return a mercator projection.

    >>> parms = base.Parms()
    >>> parms.path = "locations/bermuda"
    >>> parms.item = "time,2015,11,01,precipitation,tendegree"

    Might return a 10 degree window around the location.
    """
    
    # get data for path
    item_path = parms.item.split(',')
    
    version = item_path[-1]
    item = '/'.join(item_path[:-1])

    #print(full_path(parms.base, item))
    data = get(item)

    location = get_all_meta_data(full_path(parms.base, parms.path))

    builder = image_makers(version)

    return builder(data['data'], location)


class Location:
    """ A location

    Should have a lat, lon, assuming we are on earth.
    """

    def __init__(self, meta):

        self.__dict__.update(meta)

        if 'latlon_degrees' in meta:
            self.lat_lon_from_degrees()

    def lat_lon_from_degrees(self):
        """ Return lat lon from degrees
        
        Degrees is somethng like "32 18 N 64 47 W"
        """

        fields = self.latlon_degrees.split()

        lat = float(fields[0])
        lat += float(fields[1]) / 60.0

        if fields[2].lower() == 's':
            lat *= -1.0

        lon = float(fields[3])
        lon += float(fields[4]) / 60.0

        if fields[5].lower() == 'w':
            lon = 360.0 - lon

        self.lat = lat
        self.lon = lon
        
        return lat, lon


def build_image(data, location):
    """ Build an image for a location """
    from mpl_toolkits import basemap

    m = basemap.Basemap(projection='ortho',
                        lat_0=location['lat'], lon_0=location['lon'])

    m.drawcoastlines()

    lons, lats = numpy.meshgrid(meta['lons'], meta['lats'])

    m.pcolor(lons, lats, data, latlon=True)

    return m

def image_makers(version):

    versions = dict(
        image=build_image,
        )

    return versions.get(version)
    

    
print('Importing weather')

    
    

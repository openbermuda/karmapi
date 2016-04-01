""" Load weather data into karma pi

Creates meta data too.

Start date:

1979-1-1

lat 90.0 to -90.0, 0.75

lon 0 to 359.25, 0.75

Year, day, month.
"""
import datetime

from .base import build, match_path, Parms, get_meta_data

# FIXME -- the following constants belong in meta data

# First data in the raw data
START_DAY = datetime.date(1979, 1, 1)

# End day is first day not in the raw data
END_DAY = datetime.date(2016, 1, 1)

DELTA = 0.75
DELTA_LATITUDE = DELTA_LONGITUDE = DELTA

LATITUDE_START = 90.0
LONGITUDE_START = 0.0


def not_yet_implemented(path):
    
    raise NotImplemented(path)

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
    
    def records_per_day(self):
        """ One record per lat and lon """
        
        return number_of_longitudes() * number_of_latitudes()

    def number_of_longitudes():
        """ Number of longitudes in the grid """
        return int(360 / self.delta_longitude)
     
    def number_of_latitudes():
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

    def latitude_index(lat):
        """ Convert a latitude to index in the grid 

        Returns index of nearest grid latitude to the north of given lat.
        """
        return int((self.latitude_start - lat) / self.delta_latitude)

    def longitude_index(lon):
        """ Convert a longitude to index in the grid

        Returns index of nearest grid longitude to the west of given lon.
        """

        return int((lon - self.longitude_start) / self.delta_longitude)

    def calculate_record_number(date, lat=90, lon=0.0, start=None):
        """  Calculate the record number for given date, lat, lon """
        if start is None:
            start = self.START_DAY

        days = (date - start).days

        lat_index = latitude_index(lat)

        lon_index = longitude_index(lon)

        number = days * records_per_day()
        number += lon_index * latitudes()
        number += lat_index

        return number

    def get_data(date, infile, size=9):
        """ Pull out all data for the given date

        date: the date to pull data for

        infile: file object containing the data

        size: number of bytes per value.
        """
        pos = calculate_record_number(date)

        infile.seek(pos * size)

        # data is one value per csv line
        data = infile.read(size * records_per_day())

        return [float(x) for x in data.split()]


def day_to_numpy(data):
    
    ndata = numpy.array(data)
    ndata = ndata.reshape(longitudes(), latitudes()).T
    return ndata

    
def build_day_folders(start, end, path='.'):

    dday = datetime.timedelta(days=1)
    while day < end:

        os.makedirs('{}/{}/{}/{}'.format(
            path,
            day.year,
            day.month,
            day.day))

    return

def build_day(path):
    """ Copy data over from raw files into day folders """
    target = "year/{year}/{month}/{day}/{field}"
    # load meta data for raw file
    parms, path = match_path(path, target)

    # read meta data
    meta = get_meta_data(path)

    # now do what we have to do
    year = int(parms.year)
    month = int(parms.month)
    day = int(parms.day)

    # find info about source
    source = meta.get('source', 'raw/{field}'.format(parms.field))

    # get the meta data for the source
    source_meta = get_meta_data(source)

    print(source_meta)

    raw = RawWeather(source_meta)

    data = raw.get_data(datetime.date(year, month, day), open(source))

    # Write the data out
    pack = stuct.Struct("{}f".format(len(data)))
    with open(path, 'wb') as outfile:
        outfile.write(pack.pack(data))


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


    
def create_meta_data(path):
    """ Create meta data for top level folder 

    FIXME
    """
    meta = {}

    meta['start'] = start
    meta['end'] = start

    meta['parent'] = 'raw'
        

def create_meta_data(start, end, fields=[]):
    """ Create meta data for top level folder """
    meta = {}

    meta['start'] = start
    meta['end'] = start

    meta['parent'] = 'raw'

def create_day_meta_data(start, end, path='.'):

    pass

def write_lons_for_day(data, date, outfiles):
    
    packer = struct.Struct('{}f'.format(weather.latitudes()))

    for ix in range(weather.longitudes()):
    
        col = data[:, ix]
        pdata = packer.pack(*col)
    
        outfiles[ix].write(pdata)

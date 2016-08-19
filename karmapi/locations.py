"""
Locations
=========

Theae should be lat, lon on planet earth.

"""
from collections import Counter

import pandas
import numpy as np

from matplotlib import pyplot
from mpl_toolkits import basemap

from karmapi.base import Parms, get

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

class BBox(Parms):

    @property
    def height(self):
        return (4e7 * (self.maxlat - self.minlat) / 180.0)

    @property
    def width(self):
        return (4e7 * (self.maxlon - self.minlon) / 360.0)

    def update(self, box):

        self.minlat = min(self.minlat, box.minlat)
        self.minlon = min(self.minlon, box.minlon)
        self.maxlat = max(self.maxlat, box.maxlat)
        self.maxlon = max(self.maxlon, box.maxlon)



def get_bounding_box(lats, lons):
    """ Get the bounding box for the lats and lons 

    This gets tricky when the area being plotted straddles
    longitude 180 degrees.  
    """
    # if no data, return entire world
    if len(lats) == 0 or len(lons) == 0:
        return  Parms(dict(
            minlon=-180, maxlon=180, minlat=-90, maxlat=90))
    
    # First guess, just take max and mins
    maxlon, minlon = find_biggest_gap(lons)
    minlat, maxlat = min(lats), max(lats)

    if minlon > maxlon:
        maxlon += 360.0

    box = BBox(dict(
        minlat=minlat,
        maxlat=maxlat,
        minlon=minlon,
        maxlon=maxlon))

    return box

def find_biggest_gap(lons):
    """ Find the biggest gap between items in lons 

    Returns lons either side of the gap
    """
    # create a list and sort
    lons = [x for x in lons]

    if not lons: return -180.0, 180.0
    if len(lons) == 1: return lons[0], lons[0]
    lons.sort()

    max_delta = 0.0
    gapa = None
    gapb = None
    for a, b in zip(lons, lons[1:] + [360.0 + lons[0]]):
        delta = b - a

        if delta >= max_delta:
            max_delta = delta
            gapa = a
            gapb = b

    if gapb > 180:
        gapb -= 360.0
            
    return gapa, gapb
           

def translate(value, offset=180):
    """ Transform values to shift origin 

    Intended for longitudes in range (-180, 180)
    to shift the 0 meridian to the 180 degree point.
    """
    if value <= 0.0:
        return value + offset

    if value > 0.0:
        return value - offset

def lats_and_lons_are_transposed(lats, lons, thresh=40.0):
    """ Sometimes lats and lons are mixed up.

    Lats are lons and vice versa.

    This utility tries to spot when things are mixed up and returns
    True if things look broken.

    """
    if not len(lats): return None

    minlon = min(lons)
    maxlon = max(lons)
    minlat = min(lats)
    maxlat = max(lats)

    # if lats are outside range -90.0 to 90.0, they are probably lons
    if minlat < -90.0 or maxlat > 90.0:
        return True

    # if lons are outside range -89.0 to 89.0, they are probably lons
    if minlon < -90.0 or maxlon > 90.0:
        return False

    # If lons have less range than lats, may be reversed
    return range_test(minlat, maxlat, minlon, maxlon, thresh)

def range_test(minlat, maxlat, minlon, maxlon, thresh=40.0):
    """ Test if there is more range of lats than lons.

    If so, it may be they are transposed, unless the range is small.

    Setting thresh to 180.0 + epsilon ensures this only triggers when
    things are clearly messed up.

    Default, thresh = 40.0 may be a little over-aggressive.
    """
    latrange = maxlat - minlat
    lonrange = maxlon - minlon
    if lonrange < latrange and latrange > thresh:
        return True

    return False
    


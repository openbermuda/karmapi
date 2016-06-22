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


    location = get_all_meta_data(
        full_path(parms.base, 'locations/' + parms.location))

    print(location.keys())
    location = Location(location)

    # wrangle the data into a numpy grid
    ndata = numpy.array(data['data']).reshape(
        len(location.lons), len(location.lats)).T

    builder = image_makers(version)

    return builder(ndata, location)

def get_bounding_box(lats, lons):
    """ Get the bounding box for the lats and lons 

    This gets tricky when the area being plotted straddles
    longitude 180 degrees.  
    """
    # if no data, return entire world
    if len(lats) == 0 or len(lons) == 0:
        return  -180, 180, -90, 90
    
    # First guess, just take max and mins
    maxlon, minlon = find_biggest_gap(lons)
    minlat, maxlat = min(lats), max(lats)

    if minlon > maxlon:
        maxlon += 360.0

    return minlat, maxlat, minlon, maxlon

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

def create_map(lats, lons, proj='cyl', border=1.0, **kwargs):
    """ Create a base map appropriate for lats and lons """

    if len(lats) == 0:
        return world_map()

    minlat, maxlat, minlon, maxlon = get_bounding_box(lats, lons)

    # find 50th percentile of lats/lons and centre the map there.
    lat = pandas.Series(lats).quantile()
    lon = pandas.Series(lons).quantile()

    #print(minlon, maxlon)
    if minlon > maxlon:
        # this case probably means we are straddling the international
        # dateline.  Basemap gets dazed and confused, so just return
        # a world map
        print("ortho: {} {}".format(lat, lon))
        return world_map_centre_at(lat, lon)

    box = dict(minlat=minlat, minlon=minlon,
               maxlat=maxlat, maxlon=maxlon)
    
    return create_map_for_box(box, proj, border,
                              #lat_0=lat, lon_0=lon,
                              **kwargs)
    

def create_map_for_box(box, proj='lcc', border=1.0,
                       lat_0=None, lon_0=None, **kwargs):
    """ Create map for given bounding box """
    
    minlat = box['minlat'] - border
    minlon = box['minlon'] - border
    maxlat = box['maxlat'] + border
    maxlon = box['maxlon'] + border

    if lat_0 is None:
        lat_0 = (minlat + maxlat) / 2.

    if lon_0 is None:
        lon_0 = (minlon + maxlon) / 2.

    print(minlat, maxlat, minlon, maxlon)

    if minlon > maxlon:
        # this case probably means we are straddling the international
        # dateline.  Basemap gets dazed and confused, so just return
        # a world map
        print("ortho: {} {}".format(lat_0, lon_0))
        return world_map_centre_at(lat_0, lon_0)

    return basemap.Basemap(projection=proj,
                           lat_0 = lat_0,
                           lon_0 = lon_0,
                           llcrnrlat = minlat,
                           urcrnrlat = maxlat,
                           llcrnrlon = minlon,
                           urcrnrlon = maxlon,
                           **kwargs                           
                          )

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
    


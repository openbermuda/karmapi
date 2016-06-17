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

def create_map(lats, lons, proj='lcc', border=1.0, **kwargs):
    """ Create a base map appropriate for lats and lons """

    if len(lats) == 0:
        return world_map()

    minlat, maxlat, minlon, maxlon = get_bounding_box(lats, lons)
    
    lat_0 = (minlat + maxlat) / 2.
    lon_0 = (minlon + maxlon) / 2.

    minlat -= border
    maxlat += border
    minlon -= border
    maxlon += border

    print(minlat, maxlat, minlon, maxlon)
    
    return basemap.Basemap(projection=proj,
                           lat_0 = lat_0,
                           lon_0 = lon_0,
                           llcrnrlat = minlat,
                           urcrnrlat = maxlat,
                           llcrnrlon = minlon,
                           urcrnrlon = maxlon,
                           **kwargs                           
                          )

def lats_and_lons_are_transposed(lats, lons):
    """ Sometimes lats and lons are mixed up.

    Lats are lons and vice versa.

    This utility tries to spot when things are mixed up and returns
    True if things looked broken.

    """
    if not len(lats): return None

    minlon = min(lons)
    maxlon = max(lons)
    minlat = min(lats)
    maxlat = max(lats)

    # if lats are outside range -89.0 to 89.0, they are probably lons
    if minlat < -89.0 or maxlat > 89.0:
        return True

    # if lons are outside range -89.0 to 89.0, they are probably lons
    if minlon < -89.0 or maxlon > 89.0:
        return False

    # If lons have less range than lats, may be reversed
    latrange = maxlat - minlat
    lonrange = maxlon - minlon
    if lonrange < latrange and latrange > 40.0:
        return True

    return False


def plot_points_on_map(lats, lons,
                       m = None,
                       color=None, size=None, alpha=0.1,
                       colorbar=False, border=0.0, **kwargs):
    """ Plot event locations on a map """
    if m is None:
        m = create_map(lats, lons, border=border)

    x, y = m(lons, lats)
    #m.drawcoastlines()
    m.drawmapboundary()
    m.drawlsmask(alpha=1.)
    
    pts = m.scatter(x, y, alpha=alpha, c=color, edgecolors='none',
                    **kwargs)

    if colorbar:
        print('adding colorbar for {}'.format(pts))
        m.colorbar(pts)
    
    return m

def draw_grid_on_map(m):
    """ Draw parallels and meridians """
    m.drawparallels(range(-90, 90, 10), labels=[1, 0, 0, 1])
    m.drawmeridians(range(0, 350, 10), labels=[1, 0, 0, 1])
    

def us_map():
    """ Return a map suitable for the US 

    FIXME: find a way to return good maps based on a region.
    """

    return basemap.Basemap(projection='stere',
                           lat_0=10.0, lon_0=-80.0,
                           llcrnrlat=10, llcrnrlon=-120,
                           urcrnrlat=60, urcrnrlon=-40)


def world_map():
    """ Return a map suitable for the world

    FIXME: find a way to return good maps based on a region.
    """

    return basemap.Basemap(projection='robin',
                           lat_0=0.0, lon_0=0.0)



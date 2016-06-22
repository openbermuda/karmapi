"""
Maps
====

A wrapper around Basemap.

Basemap supports a plethora of projections.

Each projection requires different parameters to specify the map.
"""
import pandas
import numpy as np

from mpl_toolkits import basemap

from karmapi.locations import get_bounding_box, find_biggest_gap

# projections centred on north or south pole
POLAR = set([
    'npstere', 
    'spstere',
    'nplaea',
    'splaea',
    'npaeqd',
    'spaeqd'])

# projections showing the whole world
WORLD = set([
    'vandg',
    'sinu',
    'moll',
    'kav7',
    'robin',
    'eck4',
    'mbtfpq',
    'hammer'])


CYLINDER = set(basemap._cylproj)

CENTRE = set([
    'stere',
    'laea',
    'aeqd',
    'ortho'])
    

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

    return cylinder(latmin, lonmin, latmax, lonmax, proj)

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

def draw_grid_on_map(m, plabels=True, mlabels=True, step=15):
    """ Draw parallels and meridians 
    
    [mp]labels indicate if labels should be printed on
               left, right, top, bottom.
    """

    if plabels == True:
        plabels = [1, 1, 0, 0]
    if mlabels == True:
        mlabels = [0, 0, 1, 1]

    if not plabels:
        plabels = [0, 0, 0, 0]
    if not mlabels:
        mlabels = [0, 0, 0, 0]
        
    m.drawparallels(range(-90, 90, step), labels=plabels)
    m.drawmeridians(range(0, 360, step), labels=mlabels)
    

def us_map():
    """ Return a map suitable for the US 

    FIXME: find a way to return good maps based on a region.
    """

    return basemap.Basemap(projection='stere',
                           lat_0=10.0, lon_0=-80.0,
                           llcrnrlat=10, llcrnrlon=-120,
                           urcrnrlat=60, urcrnrlon=-40)


def world(lat=0.0, lon=0.0, proj='mill'):
    """ Return a map suitable for the world """

    assert(proj in WORLD)
    
    return basemap.Basemap(projection=proj,
                           lat_0=lat, lon_0=lon)


def world_centre_at(lat, lon, proj='stere'):
    """ Return a map centred on given lat, lon """

    assert(proj in CENTRE)

    return basemap.Basemap(projection='ortho',
                           lat_0=lat, lon_0=lon)


def polar(lat=0.0, lon=0.0, boundinglat=None, proj='spstere'):
    """ Return a map suitable for the world """

    assert(proj in POLAR)

    if boundinglat is None:
        boundinglat = 1.0
        if proj[0] == 's':
            boundinglat = -1.0
    
    return basemap.Basemap(projection=proj,
                           lat_0=lat, lon_0=lon,
                           boundinglat=boundinglat)


def cylinder(latmin, lonmin, latmax, lonmax, proj='mill'):
    """ Cylindrical projection 

    These are simplest if you want to make sure the map 
    covers all lat/lon points to be plotted.

    Just use the min and max lats/lons as the corners.
    """

    assert(proj in CYLINDER)

    lat_ts = (latmin + latmax) / 2.0

    return basemap.Basemap(projection = proj,
                           llcrnrlat = latmin,
                           urcrnrlat = latmax,
                           llcrnrlon = lonmin,
                           urcrnrlon = lonmax,
                           lat_ts = lat_ts)



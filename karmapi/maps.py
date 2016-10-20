"""
Maps
====

A wrapper around Basemap.

Basemap supports a plethora of projections.

Each projection requires different parameters to specify the map.
"""
from pathlib import Path
from collections import defaultdict

import pandas
import numpy as np

from mpl_toolkits import basemap
from matplotlib import pyplot
from matplotlib.patches import Polygon

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


# Cylindrical projections. Lat/lons form a grid of rectangles.
CYLINDER = set(basemap._cylproj)

# Projections centred on a point
CENTRE = set([
    'stere',
    'laea',
    'aeqd'])

# Projections from the perspective of a satellite in orbit.
SATELLITE = set([
    'ortho',
    'geos',
    'nsper'])
    

def create_map(lats, lons, proj='cyl', border=1.0, **kwargs):
    """ Create a base map appropriate for lats and lons """

    if len(lats) == 0:
        return world()

    box = get_bounding_box(lats, lons)

    # find 50th percentile of lats/lons and centre the map there.
    lat = pandas.Series(lats).quantile()
    lon = pandas.Series(lons).quantile()

    #print(minlon, maxlon)
    if box.minlon > box.maxlon:
        # this case probably means we are straddling the international
        # dateline.  Basemap gets dazed and confused, so just return
        # a world map
        print("world_centre_at: {} {}".format(lat, lon))
        return world_centre_at(lat, lon, width=box.widht, height=box.height)

    return create_map_for_box(box, proj, border,
                              #lat_0=lat, lon_0=lon,
                              **kwargs)
    

def create_map_for_box(box, proj='cyl', border=1.0,
                       lat_0=None, lon_0=None, **kwargs):
    """ Create map for given bounding box """
    
    minlat = box.minlat - border
    minlon = box.minlon - border
    maxlat = box.maxlat + border
    maxlon = box.maxlon + border

    if lat_0 is None:
        lat_0 = (minlat + maxlat) / 2.

    if lon_0 is None:
        lon_0 = (minlon + maxlon) / 2.

    if minlon > maxlon:
        # this case probably means we are straddling the international
        # dateline.  Basemap gets dazed and confused, so just return
        # a world map
        print("ortho: {} {}".format(lat_0, lon_0))
        return world_centre_at(lat_0, lon_0,
                               width=box.width,
                               height=box.height)

    return cylinder(minlat, minlon, maxlat, maxlon, proj, **kwargs)

def plot_points_on_map(lats, lons,
                       m = None,
                       color=None, size=None, alpha=0.1,
                       colorbar=False, border=0.0, **kwargs):
    """ Plot event locations on a map """
    if m is None:
        m = create_map(lats, lons, border=border)

    box = get_bounding_box(lats, lons)

    xlons = []
    for lon in lons:
        if lon < box.minlon:
            lon += 360.0
        xlons.append(lon)
        
    x, y = m(xlons, lats)
    #m.drawcoastlines()
    m.drawmapboundary()
    m.drawlsmask(alpha=1.)
    
    pts = m.scatter(x, y, alpha=alpha, c=color, edgecolors='none',
                    **kwargs)

    if colorbar:
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


def world(lat=0.0, lon=0.0, proj='robin', **kwargs):
    """ Return a map suitable for the world """

    assert(proj in WORLD)
    
    return basemap.Basemap(projection=proj,
                           lat_0=lat, lon_0=lon, **kwargs)


def world_centre_at(lat, lon, width=None, height=None, proj='stere', **kwargs):
    """ Return a map centred on given lat, lon """

    assert(proj in CENTRE)

    return basemap.Basemap(projection=proj,
                           width=width, height=height,
                           lat_0=lat, lon_0=lon, **kwargs)

def satellite(lat, lon, satellite_height=None, proj='ortho', **kwargs):
    """ Return map showing view from a satellite """
    if proj == 'geos':
        lat = 0

    if satellite_height is None:
        return basemap.Basemap(projection=proj,
                               lat_0=lat, lon_0=lon, **kwargs)
        

    return basemap.Basemap(projection=proj,
                           lat_0=lat, lon_0=lon,
                           satellite_height=satellite_height, *kwargs)

def polar(lat=0.0, lon=0.0, boundinglat=None, proj='spstere', **kwargs):
    """ Return a map centred on North or South pole """

    assert(proj in POLAR)

    if boundinglat is None:
        boundinglat = 1.0
        if proj[0] == 's':
            boundinglat = -1.0
    
    return basemap.Basemap(projection=proj,
                           lat_0=lat, lon_0=lon,
                           boundinglat=boundinglat, **kwargs)


def cylinder(minlat, minlon, maxlat, maxlon, proj='mill', **kwargs):
    """ Cylindrical projection 

    These are simplest if you want to make sure the map 
    covers all lat/lon points to be plotted.

    Just use the min and max lats/lons as the corners.
    """

    assert(proj in CYLINDER)

    lat_ts = (minlat + maxlat) / 2.0

    return basemap.Basemap(projection = proj,
                           llcrnrlat = minlat,
                           urcrnrlat = maxlat,
                           llcrnrlon = minlon,
                           urcrnrlon = maxlon,
                           lat_ts = lat_ts, **kwargs)


# Older debris from weather module

def location(parms):
    """Rough notes on how to plot centred on a location using basemap

    What I really want to do is implement a Karma Pi path something like
    this:

    locations/{location}/{item}

    That will show you {item} from location's point of view.

    Now {item} works best if it does not have any /'s, so for
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
    item = Path(item_path[:-1])

    #print(full_path(parms.base, item))
    data = get(item)

    location = get_all_meta_data(
        Path(parms.base) / 'locations' / parms.location)

    print(location.keys())
    location = Location(location)

    # wrangle the data into a numpy grid
    ndata = numpy.array(data['data']).reshape(
        len(location.lons), len(location.lats)).T

    builder = maps.image_makers(version)

    return builder(ndata, location)


def image_makers(version):

    versions = dict(
        image=build_image,
        )

    return versions.get(version)

def build_image(data, location):
    """ Build an image for a location """
    from matplotlib import pyplot
    from mpl_toolkits import basemap

    m = basemap.Basemap(projection='ortho',
                        lat_0=location.lat, lon_0=location.lon)

    m.drawcoastlines()

    lons, lats = numpy.meshgrid(location.lons, location.lats)

    
    m.pcolor(lons, lats, data, latlon=True)

    return m, lats, lons, data
    
    img = StringIO()
    pyplot.savefig(img)

    result = img.getvalue()
    img.close()
    return result

class CountyPlotter:

    def __init__(self):
        """ Reads county shapefiles 

        Shapes is list of (lat/lons) making up the shapes.

        info is list of info about each shape.
        """

        mm = basemap.Basemap()

        gis_file = Path(basemap.basemap_datadir) / 'UScounties'
        if not gis_file.with_suffix('.shp').exists():
            msg = ('Cannot find {}.shp\nYou can install it with'
                    '`conda install -c conda-forge basemap-data-hires`').format
            raise IOError(msg(str(gis_file)))

        county_info = mm.readshapefile(
            str(gis_file), 'counties',
            default_encoding='latin-1', drawbounds=False, linewidth=0.1)

        self.shapes = mm.counties

        self.info = mm.counties_info

        self._build_shape_lookup()

        self.cmap = pyplot.get_cmap('rainbow')

    def _build_shape_lookup(self):
        """ Spin through shape info creating lookup table """
        lookup = defaultdict(list)

        for shape, info in zip(self.shapes, self.info):
            key = info['STATE'].lower(), int(info['COUNTY_FIP'])
            lookup[key].append(shape)

        self.lookup = lookup

    def translate(self, m, patch):

        return [m(x, y) for (x, y) in patch]

    def plot(self, data, m):
        """ Plot data in data on map m 

        Data is dictionary with (state, cty) as key
        and value as value.
        """
        norm = max(data.values())
        ax = pyplot.gca()

        for key, value in data.items():
            color = self.cmap(value/norm)
            for patch in self.lookup[key]:
                mpatch = self.translate(m, patch)
                poly = Polygon(mpatch, facecolor=color, edgecolor=color)
                ax.add_patch(poly)

        m.set_axes_limits()


    def state_bounds(self):
        """ Return bounding boxes for states """
        boxes = {}
        for (state, county), shapes in self.lookup.items():
            for shape in shapes:
                box = get_bounding_box([x[1] for x in shape],
                                       [x[0] for x in shape])
                
                sbox = boxes.get(state)
                if sbox:
                    sbox.update(box)
                else:
                    boxes[state] = box

        self.boxes = boxes


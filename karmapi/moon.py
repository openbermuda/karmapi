"""
Moon or moai

Electromagnetic balls of wonder dancing together.

Ahu bus stops

and the number 7 bus.

May Day Parade

Winter Solstice

Spring Tide Mays

And October blaze.


So far now, simulate moai.  

And orongo.


"""
from pathlib import Path
from matplotlib import pyplot as plt

from blume import magic, farm

import datetime

import netCDF4

def puzzle():
    """ No idea what this is about 
    
    New moons?
    """
    NEW = datetime.datetime(1900, 1, 1, 5, 50)

    NEXTNEW = datetime.datetime(1900, 1, 30, 5, 22)


    delta = (NEXTNEW - NEW)

    deltas = delta.days * 24 * 3600

    print(delta.days)

    deltas += delta.seconds

    print(deltas)


    latest = datetime.datetime(2017, 11, 18, 3, 43)

    ldelta = latest - NEW


    seconds = ldelta.days * 24 * 3600
    seconds += ldelta.seconds

    print(seconds, seconds / deltas)

    current = NEW
    for x in range(100):
        print(current)

        current += delta

from collections import deque
from math import pi

class queue(deque):

    def __init__(self):

        super().__init__(self)

        self.value = 0.0
    
    def value(self):

        return self.value

    def tick(self):

        self.value /= pi
    
class stop:
    """ Or Ahu, a bus depot """

    def __init__(self, x=None, y=None):

        self.queue = queue()

        self.x = x
        self.y = y

    async def echo(self, depot=None):

        value = 0.0
        for item in depot:
            value += depot.value()

        self.value += value / 2
        return self.value

    def add(self, moai):

        # fixme push according to direction of travel
        self.queue.push(moai)

def data_to_rows(data):
    
    # figure out what we have
    import csv
    for row in csv.reader(data):
        keys = [x.strip() for x in row]
        break

    for row in csv.DictReader(data[1:], keys):
        yield row
    

        
class RongoRongo(magic.Ball):

    async def start(self):
        
        print('Rapa Nui')
        self.dem = netCDF4.Dataset(self.dem)

        # this should just be: self.moai = magic.Spell(open(self.moai))
        # just need an init method for spell
        records = list(data_to_rows(open(self.moai).readlines()))
        spell = magic.Spell()
        spell.find_casts(records)
        self.moai = list(spell.spell(records))

        self.extent = (
            self.dem.geospatial_lon_min, self.dem.geospatial_lon_max,
            self.dem.geospatial_lat_min, self.dem.geospatial_lat_max)

        print(self.dem)
        print(self.extent)
                       

    def zoomit(self, data):

        if self.zoom <= 1.:
            return data, self.extent

        width, height = data.shape
        ww = int(width // self.zoom)
        hh = int(height // self.zoom)

        xoff, yoff = self.xoff, self.yoff
        
        wstart = int((xoff + width - ww) // 2)
        hstart = int((yoff + height - hh) // 2)
        lats, lons = self.dem['lat'], self.dem['lon']

        extent = (lons[hstart], lons[hstart + hh-1],
                  lats[wstart], lats[wstart + ww-1])
        extent = [float(x) for x in extent]

        return data[wstart:wstart+ww, hstart:hstart+hh], extent
                            
    async def run(self):

        data = self.dem['Band1']

        zdata, extent = self.zoomit(data)
        zdata = zdata[::-1]

        plt.imshow(
            zdata, extent=extent, vmin=self.vmin, vmax=self.vmax,
            interpolation=self.interpolation[0],
            cmap=magic.random_colour())

        #plt.imshow(data, extent=extent)
        plt.colorbar()

        moai = select_moai(self.moai, extent)
        lats = [x['lat'] for x in moai]
        lons = [x['lon'] for x in moai]
        plt.scatter(lons, lats, s=.1, c='r')

        #plt.scatter([ahu.x for ahu in self.ahu.values()],
        #            [ahu.y for ahu in self.ahu.values()],
        #            s=1, c='r')
        
        await self.put()

def select_moai(moai, extent):

    minlon, maxlon, minlat, maxlat = extent

    result = []
    for mo in moai:
        lat, lon = mo['lat'], mo['lon']
        
        if minlon <= lon and lon <= maxlon and minlat <= lat and lat <= maxlat:
            result.append(mo)
    return result


if __name__ == '__main__':

    import argparse
    from pathlib import Path

    parser = argparse.ArgumentParser()

    AHU = dict(
        orongo = stop(y=-27.1874, x=-109.4431),
        ranoraraku = stop(y=-27.1220, x=-109.2889),
        rrq =        stop(y=-27.1263, x=-109.2885),
        tongariki =  stop(y=-27.1258, x=-109.2769),
        akivii =     stop(y=-27.1150, x=-109.3950),
        hanavarevare = stop(y=-27.1167, x=-109.4167),
        tepeu =      stop(y=-27.1024, x=-109.4163),

        xx1 =        stop(y=-27.0950, x=-109.4108),
        xx2 =        stop(y=-27.1236, x=-109.4215),
        xx3 =        stop(y=-27.0933, x=-109.4098),
        xx4 =        stop(y=-27.0887, x=-109.4074),
        xx5 =        stop(y=-27.0703, x=-109.3987),
    )

    ORIGIN=AHU['orongo']

    parser.add_argument('-moai', default='moai.csv')
    parser.add_argument('-vmin', type=float, default=-4000)
    parser.add_argument('-vmax', type=float, default=500)
    parser.add_argument('-xoff', type=float, default=0.0)
    parser.add_argument('-yoff', type=float, default=0.0)
    parser.add_argument('-zoom', type=float, default=2.0)
    parser.add_argument('-dem', default='easter_island_3_isl_2016.nc')

    args = parser.parse_args()

    magic.modes.rotate()
    animal = farm.Farm()

    rongo = RongoRongo()
    rongo.update(args)
    rongo.ahu = AHU
    rongo.interpolation = deque([
        None, 'none', 'nearest', 'bilinear', 'bicubic', 'spline16',
        'spline36', 'hanning', 'hamming', 'hermite', 'kaiser', 'quadric',
        'catrom', 'gaussian', 'bessel', 'mitchell', 'sinc', 'lanczos'])
    
    animal.add(rongo)
    animal.shep.path.append(rongo)

    farm.run(animal)

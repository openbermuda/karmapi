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
    

        
class RapaNui(magic.Ball):

    async def start(self):
        
        print('Starting Rapa Nui')
        self.dem = netCDF4.Dataset(self.dem)

        records = list(data_to_rows(open(self.moai).readlines()))
        spell = magic.Spell()
        spell.find_casts(records)
        self.moai = list(spell.spell(records))
        
                            
    async def run(self):

        data = self.dem['Band1'][::-1]
        extent = (
            self.dem.geospatial_lon_min, self.dem.geospatial_lon_max,
            self.dem.geospatial_lat_min, self.dem.geospatial_lat_max)
                  
        plt.imshow(
            data, extent=extent, vmin=self.vmin, vmax=self.vmax,
            cmap=magic.random_colour())

        #plt.imshow(data, extent=extent)
        plt.colorbar()

        lats = [x['lat'] for x in self.moai]
        lons = [x['lon'] for x in self.moai]
        plt.scatter(lons, lats)

        # add ahu?
        
        await self.put()

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
    parser.add_argument('-vmin', default=-4000)
    parser.add_argument('-vmax', default=500)
    parser.add_argument('-dem', default='easter_island_3_isl_2016.nc')

    args = parser.parse_args()

    animal = farm.Farm()

    rapanui = RapaNui()
    rapanui.update(args)
    rapanui.ahu = AHU
    animal.add(rapanui)
    animal.shep.path.append(rapanui)

    farm.run(animal)

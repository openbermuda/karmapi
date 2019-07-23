"""
View netcdf files of global data

Fit models

Simulate future

n c d f

natural circular data field?

OK time for an update.

I discovered *pyshtools* in my explorations.

Spherical harmonic analysis.   Fourier transforms for spheres.

Explore global harmonics.

But first I need to unravel what is here.
"""
import datetime
import math
import argparse
from pathlib import Path

from random import randint

from karmapi import base, tpot, cpr, pigfarm

import netCDF4
import numpy as np

import curio

import pyshtools

from matplotlib import pyplot
from matplotlib.pyplot import show, imshow, title, colorbar


def load(path):

    return netCDF4.Dataset(path)


def current_epoch():

    return datetime.datetime(1900, 1, 1)

def stamp_filter(stamps, start, epoch=None):

    for date in stamps_to_datetime(stamps, epoch):

        if date >= datetime.datetime(start.year, start.month, start.day):
            yield stamp

def stamps_to_datetime(stamps, epoch=None):

    epoch = epoch or current_epoch()

    for stamp in stamps:
        yield epoch + datetime.timedelta(hours=int(stamp))


def stamp_sort(stamps):
    """ FIXME: use this to go through images in order """
    ss = sorted(zip(stamps,
                    stamps_to_datetime(stamps),
                    range(len(stamps))))

    return ss

class WorldView(cpr.Sphere):

    def __init__(self, stamps, values, **kwargs):

        self.stamps = stamps
        self.values = values
        self.save = False
        self.size = self.values[0].shape
        #self.size = self.size[1], self.size[0]
        print('SIZE', self.size)
        self.min = self.values[0].min()
        self.max = self.values[0].max()
        self.ix = 0
        self.n = len(self.stamps)
        self.spin = 5

        self.sample_points()

        super().__init__(self.size, **kwargs)

        # data is some sort of ncdf thing
        # set it up so run can just cycle through the
        # frames in order.

        # take 3 at a time for r g b

    def sample_points(self):

        h, w = self.size

        self.points = []
        for pt in range(100):
            x, y = randint(0, h-1), randint(0, w-1)

            self.points.append((x, y))


    def __getstate__(self):
        """ Don't try and save stamps or values """
        state = self.__dict__.copy()
        state.update(dict(stamps=None, values=None))
        return state

    def show_date(self):
        
        print(self.current_date())

    def tick(self):

        self.t += 1

        if self.save:
            im = self.project()
            im.save(f'{self.save}/{now}.png')
            
        return self


    def post_tick(self):
        """ stuff that has to happen on this processor """
        self.next_frame()


    def current(self):

        s, d, ix = self.stamps[self.ix]

        data = self.values[ix]

        return data

    def current_date(self):
        """ Get date for current stamp """
        s, d, ix = self.stamps[self.ix]

        return d

    def next_frame(self):

        red = self.current()
        print(f'RED SHAPE {red.shape}')
        red = to_sha(red[1:])
        print(f'RED SHAPE {red.shape}')
        red = red.flatten()
        print(f'RED SHAPE {red.shape}')

        red = np.concatenate((red[self.spin:], red[0:self.spin]))

        self.forward()
        green = self.current()
        green = to_sha(green[1:])
        green = green.flatten()
        green = np.concatenate((green[self.spin:], green[0:self.spin]))

        self.forward()
        blue = self.current()
        blue = to_sha(blue[1:])
        blue = blue.flatten()
        blue = np.concatenate((blue[self.spin:], blue[0:self.spin]))

        self.rgb = np.array(list(zip(red,
                                     green,
                                     blue)))

        self.spin += 5
        self.spin %= self.size[0]

        #print(red[0][50])
        #print(red[1][50])

        height, width = self.size
        self.rgb.resize((height-1, width, 3))

        #self.sample_current()
        
        self.forward()

        # fix me
        #for skip in range((9 * 11) + 18):
        #    self.forward()

        
    def sample_current(self):
        """ Take a sample of current data 

        Add it to history.
        """
        if self.ix in self.history:
            print('size of history', len(history))
            1/0
            return

        rgb = []
        for xx, yy in self.points:
            value = self.rgb[xx, yy]
            rgb.append(value)
        
        self.history[self.ix] = rgb


    def forward(self):
        """ Step to next frame """
        self.ix += 1

        self.ix = self.ix % self.n
        
    def backward(self):

        self.ix -= 1

        if self.ix == -1:
            self.ix += self.n

    def scale(self, data):

        #return [randunit() for x in data]

        delta = self.max - self.min
        data = [(x - self.min) / delta for x in data.flatten()]

        # map to [-1, 1] interval
        data = [max(min((2 * x) - 1.0, 1.0), 0.0) for x in data]

        return data


def to_sha(data):

    from pyshtools.expand import SHExpandDH

    #print(data.shape)
    return SHExpandDH(data, sampling=2)


class World(cpr.NestedWaves):

    def __init__(self, parent, stamps=None, values=None,
                 balls=None,
                 save=None, **kwargs):

        self.stamps = list(stamps)
        self.values = values
        self.save = save
        self.spin = 1

        
        sphere = WorldView(self.stamps, self.values)
        sphere.M = 1
        sphere.r = 0
        balls[0] = sphere
        
        sphere = WorldView(self.stamps, self.values)
        sphere.M = balls[-1].M
        sphere.r = balls[-1].r
        balls[-1] = sphere

        #self.add_event_map('w', self.more_spin)
        #self.add_event_map('w', self.less_spin)

        super().__init__(parent, balls=balls, **kwargs)


class CircularField:

    def __init__(self, args):
        """ Load the file """

        path = Path.home() / Path(args.path)

        self.df = load(path / args.raw)

        stamps = self.df.variables['time']
        self.values = self.df.variables[args.value]

        print(self.df.variables.keys())
        
        self.stamps = stamp_sort(stamps)

        print("number of observations:", len(stamps))

        # totals across years
        self.totals = {}


    def filter_stamps(self, hour=None, day=None):

        good = []
        for stamp in self.stamps:
            s, d, ix = stamp
            if hour is not None:
                if d.hour != hour:
                    continue
            if day is not None:
                if d.day != day:
                    continue
            good.append(stamp)

        self.stamps = good

    def generate_data(self, epoch=None):
        """ spin through frames in stamp order """
        epoch = epoch or current_epoch()

        for ix, stamp in enumerate(self.stamps):
            ss, date, nix = stamp
            yield date, self.values[nix]


    def sum_years(self):
        """ Build totals across years """
        counts = {}
        for date, value in self.generate_data():
            key = (date.month, date.day, date.hour)

            if key in self.totals:
                self.totals[key] += value
                counts[key] += 1
            else:
                self.totals[key] = value
                counts[key] = 1
                
        for key in self.totals.keys():
            self.totals[key] /= counts[key]

    def deviation(self, date, value):
        """ Return defiation from monthly mean """
        key = (date.month, date.day, date.hour)
        return value - self.totals[key]


def argument_parser(parser=None):        
            
    parser = cpr.argument_parser(parser)
    parser.add_argument('--path', default='karmapi/ecmwf')
    parser.add_argument('--value', default='t2m')
    parser.add_argument('--raw', default='temperature.nc')
    parser.add_argument(
        '--pc', action='store_true',
        help='do principal components')

    parser.add_argument('--delta', action='store_true')
    parser.add_argument('--model', action='store_true')
    parser.add_argument('--offset', type=int, default=0)
    parser.add_argument('--save')

    return parser

if __name__ == '__main__':


    parser = argument_parser()

    args = parser.parse_args()


    if args.pc:
        pca = pcs(stamps, values, 48*35)

        pca.show_fracs(0.1)

        for x in dir(pca):
            print(x)

    elif args.delta:
        delta(stamps, values)

    elif args.model:

        model(stamps, values)
        
    else:
        #path = path / args.value
        #images(path, stamps, values)
        pass

    cf = CircularField(args)

    print('min max:')
    print(cf.values[0].min(), cf.values[0].max())
    
    spheres = cpr.args_to_spheres(args)

    print(f'Number of spheres {len(spheres)}')
    parms = dict(stamps=cf.stamps, values=cf.values, save=args.save,
                 balls=spheres)
    
    farm = pigfarm.sty(World, parms)

    curio.run(farm.run(), with_monitor=True)
    

   

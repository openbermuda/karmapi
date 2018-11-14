"""
View netcdf files of global data

Fit models

Simulate future

n c d f

natural circular data field?
"""
import datetime
import math
import argparse
from pathlib import Path

from random import randint

import netCDF4
import numpy as np

import curio

from matplotlib import pyplot
from matplotlib.pyplot import show, imshow, title, colorbar

from karmapi import base, sonogram, tpot, cpr, pigfarm

def load(path):

    return netCDF4.Dataset(path)


def images(path, folder):

    df = load(path)

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

    

def generate_data(stamps, values, epoch=None):

    epoch = epoch or current_epoch()
    
    for ix, stamp in enumerate(stamps):

        date = epoch + datetime.timedelta(hours=int(stamp))

        yield values[ix], date
    

        
def images(path, stamps, values):

    lastdate = None
    for data, date in generate_data(stamps, values):

        print(date)
        pyplot.imshow(data)

        item  = Path(f'{path}/{date.year}/1/1/').expanduser()

        item.mkdir(exist_ok=True, parents=True)

        filename = f'{date.month:02}{date.day:02}_'
        filename += f'{date.hour:02}{date.minute:02}{date.second:02}.jpg'

        print(filename)
        item = item / filename

        pyplot.savefig(str(item), bbox_inches='tight', pad_inches=0)


def totals(stamps, values):

    totals = []
    for data, date in generate_data(stamps, values):
        total = sum(sum(data))
        totals.append(total)

    return totals

def pcs(stamps, values, n=None):
    """ Get principal components for each longitude 

    See how picture changes if we just use first 2 components.
    """

    if n:
        stamps = stamps[:n]

    records = []
    for lon in range(1):
        for data, date in generate_data(stamps, values):
            print(date)
            records.append(data[lon])

    records = np.array(records)

    print(records.shape)

    pca = sonogram.Principals(records, standardize=True)

    print(pca.Wt)
    
    return pca


def downsample(stamps, values, k=15):

    
    for data, date in generate_data(stamps, values):
    
        xx = values[0]
        width, height = xx.shape

    nn = len(stamps)
    


def delta(stamps, values):

    nn = 37
    totals = values[0]
    for x in range(1, nn * 48):
        totals += values[x]

    totals /= (nn * 48)
    print(totals.shape)

    dt = list(stamps_to_datetime(stamps))
    
    rolling = None
    alpha = .3

    results = []
    for x in range(nn):

        data = values[x * 48]
        for offset in range(1, 48):
            ix = (x * 48) + offset
            data += values[ix]
        data /= 48
        data -= totals

        results.append(data)


    print(len(results))
    window = 5
    data = results[0].copy()
    for w in range(1, window):
        data += results[w]
        print(data.mean())

    print('start')
    for ix, (inn, out) in enumerate(zip(results[window:], results)):

        data += inn

        data -= out
        #xx = pyplot.subplot(8, 4, 1 + x - window)
        #xx.set_axis_off()ga
        
        print(f'{dt[48*ix]} {data.mean()}, {data.max()}, {data.min()}')
        xx = imshow(data / window, vmin=-3, vmax=3, cmap='rainbow')
        #for x in dir(xx):
        #    print(x)

        #colorbar()
        title(str(dt[48*(ix + window)]))
        saveimage('karmapi/ecmwf/anomaly', dt[48 * ix])



def saveimage(path, date):

    item  = Path(f'{path}/1979/1/1').expanduser()
    
    item.mkdir(exist_ok=True, parents=True)

    filename = f'{date.year:02}{date.month:02}.jpg'

    print(filename)
    item = item / filename

    pyplot.savefig(str(item), bbox_inches='tight', pad_inches=0)


def model(stamps, values):
    """ Build a model """
    stamps = list(stamps)
    xx = values[stamps[0]]

    print(xx.shape)


def model(stamps, values):
    """ fit a model """

    dt = list(stamps_to_datetime(stamps))

    data = pcs(stamps, values)

def xxx(stamps, ix, n=10):

    for x in stamps[ix: ix + n]:
        print(x)

    print([x % 24 for x in stamps[ix: ix + n]])


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
        """ """
        state = self.__dict__.copy()
        state.update(dict(stamps=None, values=None))
        return state

    def update(self, ball):

        super().update(ball)

        print(self.current_date())
        self.next_frame()

    def tick(self):

        self.t += 1

        if self.save:
            im = self.project()
            im.save(f'{self.save}/{now}.png')
            
        return self

    def current(self):

        s, d, ix = self.stamps[self.ix]

        data = self.values[ix]

        return data

    def current_date(self):
        """ Get date for current stamp """
        s, d, ix = self.stamps[self.ix]

        return d

    def next_frame(self):


        red = self.scale(self.current())
        red = red[self.spin:] + red[0:self.spin]

        self.forward()
        green = self.scale(self.current())
        green = green[self.spin:] + green[0:self.spin]

        self.forward()
        blue = self.scale(self.current())
        blue = blue[self.spin:] + blue[0:self.spin]

        self.spin += 5
        self.spin %= self.size[0]
        
        self.rgb = np.array(list(zip(red, green, blue)))

        height, width = self.size
        self.rgb.resize((height, width, 3))

        self.sample_current()
        
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

class CircularField:

    def __init__(self, args):
        """ Load the file """

        path = Path.home() / Path(args.path)

        self.df = load(path / args.raw)

        stamps = self.df.variables['time']
        self.values = self.df.variables[args.value]

        print(self.df.variables)
        
        self.stamps = stamp_sort(stamps)

        print("number of observations:", len(stamps))
        

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

    parms = dict(stamps=cf.stamps, values=cf.values, save=args.save,
                 balls=spheres)
    
    farm = pigfarm.sty(World, parms)

    curio.run(farm.run(), with_monitor=True)
    

   

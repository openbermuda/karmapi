"""
Interface to netcdf files
"""
import datetime
import math
import argparse
from pathlib import Path

import netCDF4
import numpy

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

    records = numpy.array(records)

    print(records.shape)

    pca = sonogram.Principals(records, standardize=True)

    print(pca.Wt)
    
    return pca


def downsample(stamps, values, k=15):

    
    for data, date in generate_data(stamps, values):
    
        xx = values[0]
        width, height = xx.shape

    nn = len(stamps)
    


def model(stamps, values):
    """ Build a model """
    stamps = list(stamps)
    xx = values[stamps[0]]

    print(xx.shape)

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
        self.size = self.size[1], self.size[0]
        self.min = self.values[0].min()
        self.max = self.values[0].max()
        self.ix = 0
        self.n = len(self.stamps)

        super().__init__(self.size, **kwargs)

        # data is some sort of ncdf thing
        # set it up so run can just cycle through the
        # frames in order.

        # take 3 at a time for r g b

    async def run(self):

        self.t += 1

        self.next_frame()
        now = self.current_date()
        print(now)
        if self.save:
            im = self.project()
            im.save(f'{self.save}/{now}.png')

    def current(self):

        s, d, ix = self.stamps[self.ix]

        return self.values[ix]

    def current_date(self):

        s, d, ix = self.stamps[self.ix]

        return d

    def next_frame(self):

        self.red = self.scale(self.current())

        self.forward()
        self.green = self.scale(self.current())
        #self.green = [0. for x in self.red]

        self.forward()
        self.blue = self.scale(self.current())
        #self.blue = [0. for x in self.red]
        
        self.forward()

        for skip in range((9 * 11) + 18):
            self.forward()

    def forward(self):

        self.ix += 1

        self.ix = self.ix % self.n
        
    def backward(self):

        self.ix == 1

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
                 save=None, **kwargs):

        self.stamps = list(stamps)
        self.values = values
        self.save = save

        super().__init__(parent, **kwargs)


    def build(self):
        """ Create the balls """
        # add a bunch of spheres to the queue
        self.balls = []
        last_ball = None
        for ball in range(self.n):
            size = self.base + (ball * self.inc)

            head = True
            
            if ball:
                head = False

            tail = False
            if ball == self.n - 1:
                tail = True


            if tail or head:
                sphere = WorldView(self.stamps, self.values, head=head, tail=tail)
                sphere.save = self.save or False
            else:
                sphere = cpr.Sphere((size, size), head=head, tail=tail)

            if not sphere.head:
                sphere.last_ball = last_ball
                last_ball.next_ball = sphere
            
            self.uq.put(sphere)
            self.balls.append(sphere)

            last_ball = sphere
            

if __name__ == '__main__':


    parser = cpr.argument_parser()

    parser.add_argument('--path', default='karmapi/ecmwf')
    parser.add_argument('--value', default='t2m')
    parser.add_argument('--raw', default='temperature.nc')
    parser.add_argument('--date')
    parser.add_argument(
        '--pc', action='store_true',
        help='do principal components')

    parser.add_argument('--delta', action='store_true')
    parser.add_argument('--model', action='store_true')
    parser.add_argument('--offset', type=int, default=0)
    parser.add_argument('--save')

    args = parser.parse_args()

    path = Path.home() / Path(args.path)

    df = load(path / args.raw)

    stamps = df.variables['time']
    values = df.variables[args.value]

    print(df.variables)
    
    stamps = stamp_sort(stamps)

    path = path / args.value

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
        #images(path, stamps, values)
        pass

    print('min max:')
    print(values[0].min(), values[0].max())

    parms = dict(stamps=stamps, values=values, save=args.save,
                 n=args.n, inc=args.inc, base=args.base)
    
    farm = pigfarm.sty(World, parms)

    curio.run(farm.run(), with_monitor=True)
    

    

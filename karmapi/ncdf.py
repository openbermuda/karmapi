"""
Interface to netcdf files
"""
import datetime
import math
import argparse
from pathlib import Path

import netCDF4
import numpy

from matplotlib import pyplot
from matplotlib.pyplot import show, imshow, title, colorbar

from karmapi import base, sonogram, tpot

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
    

if __name__ == '__main__':


    parser = argparse.ArgumentParser()

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

    args = parser.parse_args()

    path = Path(args.path)

    df = load(path / args.raw)

    stamps = df.variables['time']

    args.date = base.parse_date(args.date)

    if args.date:
        stamps = stamp_filter(stamps, args.date)

    values = df.variables[args.value]

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
        images(path, stamps, values)
    

    

    

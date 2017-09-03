"""
Interface to netcdf files
"""
import datetime
import math
import argparse
from pathlib import Path

import netCDF4

from matplotlib import pyplot

def load(path):

    return netCDF4.Dataset(path)


def images(path, folder):

    df = load(path)

def current_epoch():

    return datetime.datetime(1900, 1, 1)

def stamp_filter(stamps, start, epoch=None):

    epoch = epoch or current_epoch()

    for stamp in stamps:
        date = epoch + datetime.timedelta(hours=int(stamp))

        if date >= start:
            yield stamp
    

def generate_data(stamps, values, epoch=None):

    epoch = epoch or current_epoch()
    
    for ix, stamp in enumerate(stamps):

        date = epoch + datetime.timedelta(hours=int(stamp))

        yield values[ix], date
    

        
def images(path, stamps, values):

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



if __name__ == '__main__':


    parser = argparse.ArgumentParser()

    parser.add_argument('--path', default='karmapi/ecmwf')
    parser.add_argument('--value', default='t2m')
    parser.add_argument('--raw', default='temperature.nc')
    parser.add_argument('--date')

    args = parser.parse_args()

    path = Path(args.path)

    df = load(path / args.raw)

    epoch = current_epoch(args.date)

    stamps = df.variables['time']


    args.date = parse_date(args.date)

    if args.date:
        stamps = stamp_filter(stamps, args.date, epoch)

    values = df.variables[args.value]

    path = path / args.value

    images(path, stamps, values)
    

    

    

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

def generate_data(stamps, values):

    epoch = datetime.datetime(1900, 1, 1)
    
    for ix, stamp in enumerate(stamps):

        date = epoch + datetime.timedelta(hours=int(stamp))

        yield values[ix], date
    

        
def images(path, stamps, values):

    for data, date in generate_data(stamps, values):

        pyplot.imshow(data)

        path = Path(f'{path}/{date.year}/1/1/').expanduser()

        path.mkdir(exist_ok=True, parents=True)

        path = path / f'{date.hour:02}{date.minute:02}{date.second:02}.jpg'
        
        pyplot.savefig(path, bbox_inches='tight', pad_inches=0)



if __name__ == '__main__':


    parser = argparse.ArgumentParser()

    parser.add_argument('--path', default='karmapi/ecmwf')
    parser.add_argument('--value', default='t2m')
    parser.add_argument('--raw', default='temperature.nc')

    args = parser.parse_args()

    path = Path(args.path)

    df = load(path / args.raw)

    stamps = df.variables['time']

    values = df.variables[args.value]

    path = path / args.value

    images(path, stamps, values[:10])
    

    

    

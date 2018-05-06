"""
Quick and dirty move some pictures around.

Usual stuff guess year/month/day from file name, move accordingly

Cross fingers
"""
import datetime
import argparse
import shutil

from pathlib import Path

def warp(dest, when):

    folder = dest / str(when.year) /  str(when.month) / str(when.day)

    return folder / f'{when.hour:02}{when.minute:02}{when.second:02}'

def parse(item):
    """ Oh no.. date parsing time """
    print(item)
    pitem = Path(item)
    #for x in dir(pitem):
    #    print(x)
    when = pparse(pitem)
    
    return when, pitem

def pparse(pitem):
    """ Convert path into date time """
    fields = pitem.stem.split('_')
    print(fields)

    name, day, second = fields[:3]

    year = int(day[:4])
    month = int(day[4:6])
    day = int(day[6:])
    print(year, month, day)

    hour = int(second[:2])
    minute = int(second[2:4])
    second = int(second[4:])

    when = datetime.datetime(year, month, day, hour, minute, second)
    print(when)
    return when

if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('dest')

    parser.add_argument('-folder', default='.')

    args = parser.parse_args()

    items = Path(args.folder)

    dest = Path(args.dest)

    for item in items.glob('*'):

        # skip sub-folders for now. Pixel pics come with .inflight
        if item.is_dir():
            continue

        when, what = parse(item)

        if when and what:

            where = warp(dest, when).with_suffix(what.suffix)

            if where:
                where.parent.mkdir(exist_ok=True, parents=True)
                print(what, where)
                shutil.copyfile(what, where)

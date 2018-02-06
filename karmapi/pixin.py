"""
Quick and dirty move some pictures around.

Usual stuff guess year/month/day from file name, move accordingly

Cross fingers
"""

import argparse

from pathlib import Path

def warp(when, what, dest):

    return dest / f'{when.year}/{when.month}/when.day}' / what

def parse(item):
    """ Oh no.. date parsing time """

    return None, None


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('-folder', default='.')

    args = parser.parse_args()

    items = Path(args.folder)

    for item in items.glob('*'):

        when, what = parse(item)

        if when and what:

            where = warp(when, what, dest)

            if where:
                shutil.copyfile(what, where)

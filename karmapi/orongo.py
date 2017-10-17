"""  Convert to rongo rongo

Sort of.

Four suits.  

Still Rock Wobble Dance s r w d SH DC ?

0-9 a b
"""

from collections import Counter

from pathlib import Path

import argparse

from math import pi, e

import random

YEAR = 1

MONTH = 4

WEEK = 52

DAY = 7

EMONTH = (DAY * MONTH) / (pi * e)

EYEAR = 0.25 / (DAY * WEEK)

def orongo(data):
    """ Spin it around """
    print(data.__hash__())

    return reversed(data)

def alpha(image):
    """ Pick symbols from an image """

    for season in range(MONTH):
        for week in range(MONTH):
            for day in range(DAY):
                # pick up a pick up a pixel or many from image
                yield None
            


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('path', nargs='+')

    parser.add_argument('--glob', default='**/*.rst')

    args = parser.parse_args()


    totals = Counter()
    ototals = Counter()

    for path in args.path:
        print(path)
        for name in Path(path).glob(args.glob):

            print(name)

            counts = Counter()

            data = name.open().read()
            counts.update(data.split())
            totals.update(counts)


            rongo = orongo(data)
            counts = Counter(rongo)

            print('rongo')
            print(counts.most_common(5))
            print(sum(counts.values()))
            print()


    print('Totals:')

    print(totals.most_common(20))

    print(sum(totals.values()))
        

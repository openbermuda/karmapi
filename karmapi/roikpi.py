"""
Round objects in karma pi
"""

import math

import argparse

from collections import deque, defaultdict, Counter, namedtuple

import curio

import numpy

from PIL import Image, ImageTk

from karmapi import base, tpot, prime, pigfarm

from karmapi.wc import wc
from karmapi import cpr
from karmapi import ncdf
from karmapi import tankrain

from random import random, randint, gauss

def main():

    parser = cpr.argument_parser()

    parser.add_argument('--pig', action='store_false', default=True)
    parser.add_argument('--minutes', type=int, default=30)
    parser.add_argument('path', nargs='?', default='.')
    parser.add_argument('--background')
    parser.add_argument('--version', default='')
    parser.add_argument('--date')
    parser.add_argument('--events')
                            
    args = parser.parse_args()

    args.date = base.parse_date(args.date)

    if args.events:
        args.events = open(args.events)

    farm = pigfarm.sty()

    
    farm.add(
        tankrain.TankRain,
        dict(path=args.path, version=args.version, date=args.date))

    # JeusSansFrontieres
    jsf = wc.jsf
    
    farm.add(
        wc.MexicanWaves,
        dict(jsf=jsf,
             venues=wc.places,
             back_image=args.background,
             events=args.events))

    balls = list(cpr.prime_balls(args.base, args.n))

    farm.add(
        cpr.NestedWaves,
        dict(balls=balls))

    curio.run(farm.run(), with_monitor=True)
            

if __name__ == '__main__':

    main()

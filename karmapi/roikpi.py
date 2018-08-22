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

    parser = ncdf.argument_parser()
    
    parser.add_argument('--pig', action='store_false', default=True)
    parser.add_argument('--minutes', type=int, default=30)
    parser.add_argument('slides', nargs='?', default='.')
    parser.add_argument('--background')
    parser.add_argument('--version', default='')
    parser.add_argument('--date')
    parser.add_argument('--events')
                            
    args = parser.parse_args()
    print(args)
    
    args.date = base.parse_date(args.date)

    if args.events:
        args.events = open(args.events)

    farm = pigfarm.sty()

    
    farm.add(
        tankrain.TankRain,
        dict(path=args.slides, version=args.version, date=args.date))

    # JeusSansFrontieres
    jsf = wc.jsf
    
    farm.add(
        wc.MexicanWaves,
        dict(jsf=jsf,
             venues=wc.places,
             back_image=args.background,
             events=args.events))

    spheres = cpr.args_to_spheres(args)

    farm.add(
        cpr.NestedWaves,
        dict(balls=spheres))

    cf = ncdf.CircularField(args)
    print('min max:')
    print(cf.values[0].min(), cf.values[0].max())
    
    spheres = cpr.args_to_spheres(args)

    parms = dict(stamps=cf.stamps, values=cf.values, save=args.save,
                 balls=spheres)
    
    farm.add(ncdf.World, parms)

    curio.run(farm.run(), with_monitor=True)
            

if __name__ == '__main__':

    main()

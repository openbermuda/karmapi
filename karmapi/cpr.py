"""
Not, CPR, but Colin P Rourke.

Simulate nested spherical waves.
"""
import argparse

import curio

from karmapi import base, tpot, pigfarm

from random import random, randint

class Sphere:

    def __init__(self, size=None):

        size = size or 4

        grid = []
        for lat in range(size):
            grid.append([random() for x in range(size)])

        print(grid)

    async def run(self):
        pass

class NestedWaves(pigfarm.Yard):
    pass

    async def run(self):
        pass

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('--gallery', nargs='*', default=['.', '../gallery'])
    parser.add_argument(
        '--snowy', action='store_true',
        help='random cat pictures')
    parser.add_argument(
        '--name', default='tree',
        help='what to show')
                            

    args = parser.parse_args()

    farm = pigfarm.PigFarm()
    
    from karmapi.mclock2 import GuidoClock
    
    farm.add(GuidoClock)

    name = args.name
    if args.snowy:
        name = 'cat'
        
    farm.add(NestedWaves, dict(gallery=args.gallery, name=name))

    curio.run(farm.run(), with_monitor=True)
    

        
            

if __name__ == '__main__':

    main()




        

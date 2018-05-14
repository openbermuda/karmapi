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

    def __init__(self, parent, start=4, end=4*1024, skip=4):
        """ Initialise the thing """

        super().__init__(parent)

        self.start = start
        self.end = end
        self.skip = skip

        # expect we'll find something to do with a queue
        self.uq = curio.UniversalQueue()

    async def start(self):
        """ Start the thing running """
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
        
    farm.add(NestedWaves)

    curio.run(farm.run(), with_monitor=True)
    

        
            

if __name__ == '__main__':

    main()




        

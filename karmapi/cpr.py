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

        self.grid = grid

    def run(self):

        print(len(self.grid))

class NestedWaves(pigfarm.Yard):

    def __init__(self, parent, n=10, base=4, inc=4):
        """ Initialise the thing """

        super().__init__(parent)

        self.base = base
        self.n = n
        self.inc = inc

        # expect we'll find something to do with a queue
        self.uq = curio.UniversalQueue()

        self.build()

    def build(self):
        """ Create the balls """
        # add a bunch of spheres to the queue
        for ball in range(self.n):
            size = self.base + (ball * self.inc)
            self.uq.put(Sphere(size))


    def step_balls(self):

        uq = curio.UniversalQueue()
        while self.uq.qsize():
            ball = self.uq.get()
            ball.run()
            uq.put(ball)

        self.uq = uq

    def draw(self):
        pass
            
    async def run(self):
        """ Run the waves """

        self.sleep = 0.05

        self.set_background()
        
        while True:
            self.canvas.delete('all')

            self.draw()

            self.step_balls()
            
            await curio.sleep(self.sleep)            


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('--gallery', nargs='*', default=['.', '../gallery'])
    parser.add_argument(
        '--snowy', action='store_true',
        help='random cat pictures')
    parser.add_argument(
        '--name', default='tree',
        help='what to show')
    parser.add_argument('-n', type=int, default=10)
                            

    args = parser.parse_args()

    farm = pigfarm.PigFarm()
    
    from karmapi.mclock2 import GuidoClock
    
    farm.add(GuidoClock)

    farm.add(NestedWaves, dict(n=args.n))

    curio.run(farm.run(), with_monitor=True)
    

        
            

if __name__ == '__main__':

    main()




        

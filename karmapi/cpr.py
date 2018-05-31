"""
Not, CPR, but Colin P Rourke.

Simulate nested spherical waves.

Things have moved on a little.

So each ball of nested waves will have a driver at the inside and at the outside too.

Different clocks at each layer.

And then outer layers made up of other randomly placed nested spheres.

But using a universal queue, so let each sphere run in its own co-routine.
"""
import argparse

import curio

from PIL import Image, ImageTk

from karmapi import base, tpot, pigfarm

from random import random, randint

class Sphere:

    def __init__(self, size=None, head=False, tail=False, t=0):

        size = size or 4

        grid = []
        for pt in range(size * size):
            grid.append(tuple(int(256 * random()) for c in 'rgb'))

        self.grid = grid
        self.size = size

        self.head = head
        self.tail = tail
        self.t = t

        # time moves slower in the inner spheres?
        self.sleep = 1 / self.size

    def project(self):
        """ Turn into a PIL? """
        image = Image.new('RGB', (self.size, self.size))
        image.putdata(self.grid)

        return image

    async def run(self):

        print(self.head, self.tail, self.size, self.t)

        self.t += 1

        if self.head:
            return await self.head_run()
        
        # now what to do?
        pass

    async def head_run(self):
        """ inner wave

        red, green, blue
        """
        pass
        


class NestedWaves(pigfarm.Yard):
    """ Inner and outer spheres 

    simulated annealing inspired in between?

    but put it in the tea pot too.

    Lots of tea pots of all kinds.

    and draw slices on the canvas from the yard.
    """

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

            head = True
            
            if ball:
                head = False

            tail = False
            if ball == self.n - 1:
                tail = True
            
            sphere = Sphere(size, head=head, tail=tail)
            
            self.uq.put(sphere)


    async def step_balls(self):
        """ step all the balls once """

        # FIXME -- think we just step the outer ball
        # really need a RandomQueue()
        uq = curio.UniversalQueue()
        while self.uq.qsize():
            ball = await self.uq.get()
            
            await ball.run()

            await uq.put(ball)

        self.uq = uq

    async def draw(self):

        ball = await self.uq.get()

        await self.draw_ball(ball)
            
    async def draw_ball(self, ball):
        """ wc has everything???? 

        feels like I have written this bit 20 times
        """
        width, height = self.width, self.height

        image = ball.project()
        
        image = image.resize((int(width), int(height)))

        self.phim = ImageTk.PhotoImage(image)

        print('creating image')
        self.canvas.create_image(0, 0, image=self.phim)


    async def run(self):
        """ Run the waves """

        self.sleep = 0.05

        self.set_background()
        
        while True:
            self.canvas.delete('all')

            await self.draw()
            await self.step_balls()
            
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
    parser.add_argument('--inc', type=int, default=4)


    args = parser.parse_args()

    farm = pigfarm.PigFarm()
    
    from karmapi.mclock2 import GuidoClock
    
    farm.add(GuidoClock)

    farm.add(NestedWaves, dict(n=args.n))

    curio.run(farm.run(), with_monitor=True)
    

        
            

if __name__ == '__main__':

    main()




        

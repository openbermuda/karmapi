"""
Not, CPR, but Colin P Rourke.

Simulate nested spherical waves.

Things have moved on a little.

So each ball of nested waves will have a driver at the inside and at the outside too.

Different clocks at each layer.

And then outer layers made up of other randomly placed nested spheres.

But using a universal queue, so let each sphere run in its own co-routine.
"""
import math

import argparse

import curio

import numpy

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
        self.last_ball = None
        self.next_ball = None
        self.fade = 1 / math.e
        self.t = t

        # time moves slower in the inner spheres?
        self.sleep = 1 / self.size

        if self.head or self.tail:
            self.setup_end()

    def project(self):
        """ Turn into a PIL? """
        image = Image.new('RGB', (self.size, self.size))
        image.putdata(self.grid)

        return image

    async def run(self):

        self.t += 1

        if self.head or self.tail:
            return await self.end_run()
        
        # Here if we are between two spheres
        # so have last_ball and next_ball

        # for each point in grid select corresponding
        # points in inner/outer spheres

        lb = self.last_ball
        nb = self.next_ball
        
        lsize = self.last_ball.size
        nsize = self.next_ball.size
        n = self.size
        
        grid = []
        ix = 0
        delta = (1 / (2 * n)) * 2 * math.pi
            
        for x in range(self.size):
            x1 = (x / n) * 2 * math.pi
            x2 = x1 + delta
                
            for y in range(self.size):
                y1 = (y / n) * 2 * math.pi
                y2 = y1 + delta

                lbc = lb.sample(x1, y1, x2, y2)
                nbc = nb.sample(x1, y1, x2, y2)

                current = self.grid[len(grid)]

                value = [(aa + bb + cc) * self.fade
                             for aa, bb, cc in zip(lbc, nbc, current)]
                
                grid.append(tuple(self.quantise(x) for x in value))

        self.grid = grid
        self.normalise()

    def quantise(self, value):

        value = int(value * 256)
        value = max(0, min(value, 255))

        return value

    def normalise(self):
        """ Normalise the grid 
        
        want mean for each colour to be 127

        let's just scale so range is 0-255
        """

        off = []
        scale = []
        for ix in range(len(self.grid[0])):
            amin = min(x[ix] for x in self.grid)
            amax = min(x[ix] for x in self.grid)

            if amax != amin:
                sc = 255 / (amax - amin)
            else:
                sc = 1.0

            scale.append(sc)
            off.append(amin)


        grid = []
        for values in self.grid:
            value = tuple(int((x-ff) * sc)
                          for x, sc, ff in zip(values, scale, off))
            
            grid.append(value)

        self.grid = grid
            

    def setup_end(self):
        """ Do some set up work for a head sphere """

        self.waves = {}
        self.inc = math.pi/20
        
        for c in 'rgb':
            phase = random()
            scale = random()
            
            self.waves[c] = [c, phase, scale]


    def sample(self, x1, y1, x2, y2):
        """ Return a pixel given a rectangle """
        
        delta = 1 / self.size
        delta *= 2 * math.pi

        xdelta = x2 - x1
        ydelta = y2 - y1

        k = int(xdelta / delta) + 1

        xx = int(x1 / delta)

        xx = randint(xx, xx + k - 1)

        yy = int(y1 / delta)

        yy = randint(yy, yy + k - 1)

        #print('sample:', xx, yy, self.size, len(self.grid))
        print(xx, yy, k, self.size)
        return self.grid[(yy * self.size) + xx]
            
    async def end_run(self):
        """ inner or outer wave

        red, green, blue
 
        let's do:
           red up down
           blue left right
           green in and out all over

        How to fill in self.grid?
        """
        n = self.size
        width = 2 * math.pi
        height = math.pi
        

        grid = []
        
        for x in range(n):
            xx = ((x / n) + (1 / (2 * n))) * 2 * math.pi

            xx += self.inc * self.t
                
            for y in range(n):

                yy = (y / n) + (1 / (2 * n))
                yy += self.inc * self.t

                rc, rphase, rscale = self.waves['r']
                gc, gphase, gscale = self.waves['g']
                bc, bphase, bscale = self.waves['b']
                
                value = (
                    int(256 * sample_wave(rphase, xx) * rscale),
                    int(256 * sample_wave(bphase, yy) * bscale),
                    int(256 * sample_wave(gphase, xx+yy) * gscale))

                grid.append(value)

        self.grid = grid
            
            
def sample_wave(phase, x):

    xx = x + (2 * math.pi * phase)

    return math.sin(xx)

        


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
        self.add_event_map(' ', self.pause)
        self.paused = False
        self.add_event_map('r', self.reset)
        
        self.dball = 0
        self.add_event_map('j', self.backward)
        self.add_event_map('k', self.forward)

    async def pause(self):
        """ Pause """
        self.paused = not self.paused

    async def reset(self):
        """ Reset waves """
        self.balls[0].setup_end()
        self.balls[-1].setup_end()

    async def forward(self):
        """ Move to next sphere """
        self.dball += 1
        self.dball %= self.n

    async def backward(self):
        """ Move to previous sphere """
        self.dball -= 1
        if self.dball < 0:
            self.dball = self.n - 1

    def build(self):
        """ Create the balls """
        # add a bunch of spheres to the queue
        self.balls = []
        last_ball = None
        for ball in range(self.n):
            size = self.base + (ball * self.inc)

            head = True
            
            if ball:
                head = False

            tail = False
            if ball == self.n - 1:
                tail = True
                
            sphere = Sphere(size, head=head, tail=tail)

            if not sphere.head:
                sphere.last_ball = last_ball
                last_ball.next_ball = sphere
            
            self.uq.put(sphere)
            self.balls.append(sphere)

            last_ball = sphere

    async def step_all(self):
        """ Step all balls once """
        balls = self.balls[:]
        while balls:
            ix = randint(0, len(balls)-1)

            await balls[ix].run()

            del balls[ix]


    async def step_balls(self):
        """ step all the balls once 

        or maybe a random ball?
        """
        ball = self.pick()

        await ball.run()

    def pick(self):
        """ Choose a ball """
        return self.balls[randint(0, self.n-1)]

    async def draw(self):

        # xx = randint(0, self.n - 1)
        xx = self.dball

        print('And the lucky number is:', xx)
        ball = self.balls[xx]

        await self.draw_ball(ball)

            
    async def draw_ball(self, ball):
        """ wc has everything???? 

        feels like I have written this bit 20 times
        """
        width, height = self.width, self.height

        image = ball.project()
        
        image = image.resize((int(width), int(height)))

        self.phim = phim = ImageTk.PhotoImage(image)

        xx = int(self.width / 2)
        yy = int(self.height / 2)
        self.canvas.create_image(xx, yy, image=phim)


    async def run(self):
        """ Run the waves """

        self.sleep = 0.05

        
        self.set_background()

        await self.step_all()
        
        while True:
            if self.paused:
                await curio.sleep(self.sleep)
                continue
            
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




        

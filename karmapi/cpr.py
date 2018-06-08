"""
Not, CPR, but Colin P Rourke.

Or CPU central processsor unit?

CP R s t U

CPR: show time universe

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

    def __init__(self, size=None, head=False, tail=False,
                 t=0, m=1., r=1.):

        size = size or (4, 4)

        self.red = []
        self.green = []
        self.blue = []

        self.size = size

        self.head = head
        self.tail = tail
        self.last_ball = None
        self.next_ball = None
        self.fade = 1 / math.e
        self.t = t

        # time moves slower in the inner spheres?
        self.sleep = 1 / self.size[0]

        self.reset(init=True)

        
    def reset(self, init=False):
        """ Reset the sphere """

        if self.head or self.tail:
            self.setup_end()
            if self.red:
                return

        self.red.clear()
        self.green.clear()
        self.blue.clear()

        self.random_grid()

        return


    def random_grid(self):

        size = self.size
        for pt in range(size[0] * size[1]):
            self.red.append(randunit())
            self.green.append(randunit())
            self.blue.append(randunit())


    def project(self):
        """ Turn into a PIL? """
        image = Image.new('RGB', (self.size[0], self.size[1]))

        # FIXME do the 256 magic int stuff here

        #print('rgb', len(self.red), len(self.green), len(self.blue))

        image.putdata(self.rgb2grid())

        return image

    def rgb2grid(self):
        grid = []
        for rgb in zip(self.red, self.green, self.blue):
            pixel = tuple(self.quantise(x) for x in rgb)
            grid.append(pixel)

        return grid
        

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
        n1, n2 = self.size
        
        grid = []
        ix = 0
        deltax = (1 / (2 * n1)) * 2 * math.pi
        deltay = (1 / (2 * n2)) * 2 * math.pi
            
        for x in range(self.size[0]):
            x1 = (x / n1) * 2 * math.pi
            x2 = x1 + deltax
                
            for y in range(self.size[1]):
                y1 = (y / n2) * 2 * math.pi
                y2 = y1 + deltay

                lbc = lb.sample(x1, y1, x2, y2)

                if nb:
                    nbc = nb.sample(x1, y1, x2, y2)
                else:
                    nbc = tuple(randunit() for c in 'rgb')

                cix = (y * self.size[0]) + x
                current = (self.red[cix], self.green[cix], self.blue[cix])

                value = [(aa + bb + cc) * self.fade
                             for aa, bb, cc in zip(lbc, nbc, current)]
                
                grid.append(value)

        self.grid2rgb(grid)
        #self.normalise()

    def grid2rgb(self, value):

        for ix, (r, g, b) in enumerate(value):
            self.red[ix] = r
            self.green[ix] = g
            self.blue[ix] = r

    def quantise(self, value):

        value = int(127 + (value * 128))
        value = max(0, min(value, 255))

        return value

    def normalise(self):
        """ Normalise the grid 
        
        want mean for each colour to be 127

        let's just scale so range is 0-255
        """

        off = []
        scale = []
        grid = self.rgb2grid()
        for ix in range(len(grid[0])):
            amin = min(x[ix] for x in grid)
            amax = min(x[ix] for x in grid)

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

        # back to rgb
        self.grid2rgb(grid)
            

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
        
        deltax = 1 / self.size[0]
        deltax *= 2 * math.pi

        deltay = 1 / self.size[1]
        deltay *= 2 * math.pi

        xdelta = x2 - x1
        ydelta = y2 - y1

        k = int(xdelta / deltax) + 1

        xx = int(x1 / deltax)

        xx = randint(xx, xx + k - 1)

        yy = int(y1 / deltay)

        k = int(ydelta / deltay) + 1

        yy = randint(yy, yy + k - 1)

        ix = (yy * self.size[0]) + xx
        return self.red[ix], self.green[ix], self.blue[ix]
            
    async def end_run(self):
        """ inner or outer wave

        red, green, blue
 
        let's do:
           red up down
           blue left right
           green in and out all over

        How to fill in self.grid?
        """
        n1, n2 = self.size
        width = 2 * math.pi
        height = math.pi
        

        grid = []
        
        for x in range(n1):
            xx = ((x / n1) + (1 / (2 * n1))) * 2 * math.pi

            xx += self.inc * self.t
                
            for y in range(n2):

                yy = (y / n2) + (1 / (2 * n2))
                yy += self.inc * self.t

                rc, rphase, rscale = self.waves['r']
                gc, gphase, gscale = self.waves['g']
                bc, bphase, bscale = self.waves['b']
                
                value = (
                    sample_wave(rphase, xx) * rscale,
                    sample_wave(bphase, yy) * bscale,
                    sample_wave(gphase, xx+yy) * gscale)

                grid.append(value)

        self.grid2rgb(grid)
            

def randunit():

    x = random()
    if random() > 0.5:
        x *= -1

    return x
        
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
        for ball in self.balls:
            ball.reset()

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

            size = (size, size)

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

    async def random_step_some(self):
        """ Step all balls once """
        balls = self.balls[:]
        while balls:
            ix = randint(0, len(balls)-1)

            await balls[ix].run()

            del balls[ix]

    async def backward_step_all(self):
        """ Step all balls once """
        balls = self.balls[::-1]
        while balls:
            ix = randint(0, len(balls)-1)

            await balls[ix].run()

            del balls[ix]

    async def step_balls(self):
        """ step all the balls once 

        or maybe a random ball?
        """
        n = randint(0, len(self.balls) - 1)

        for ball in range(n):
            ball = self.pick()

            await ball.run()

    def pick(self):
        """ Choose a ball """
        return self.balls[randint(0, self.n-1)]

    async def draw(self):

        # xx = randint(0, self.n - 1)
        xx = self.dball

        print(xx, 'lucky for some')
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

        #await self.random_step_some()

        await self.backward_step_all()
        
        while True:
            if self.paused:
                await curio.sleep(self.sleep)
                continue
            
            self.canvas.delete('all')

            await self.draw()
            #await self.step_balls()
            await self.backward_step_all()
            
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
    parser.add_argument('--base', type=int, default=20)


    args = parser.parse_args()

    farm = pigfarm.sty(NestedWaves, dict(n=args.n, inc=args.inc, base=args.base))

    curio.run(farm.run(), with_monitor=True)
            

if __name__ == '__main__':

    main()




        

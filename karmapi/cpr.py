"""
Not, CPR, but Colin P Rourke.

Or CPU central processsor unit?

CP R s t U

CPR: show time universe

Simulate nested spherical waves.

Things have moved on a little.

So each ball of nested waves will have a driver at the inside and at the
outside too.

Different clocks at each layer.

And then outer layers made up of other randomly placed nested spheres.

But using a universal queue, so let each sphere run in its own co-routine.

Update: 2018/8/4
================

The Sphere and NestedWaves classes are moving along.

For now, a sphere is represented by a square grid.

We can decide later where the grid points lie.

I have been experimenting with grids multiples of primes and made a few code
changes moving it closer to *anpotu*.

Some interesting patterns emerging::

   python3.6 cpr --base 0 --inc 23 -n 7

"""
import math

import argparse

from collections import deque, defaultdict, Counter, namedtuple

import curio

import numpy

from PIL import Image, ImageTk

from karmapi import base, tpot, prime, pigfarm

from random import random, randint, gauss

class Sphere:
    """ If it hass mass (m) then pass through waves

    Regardless, show the view at radius r from centre of mass.

    omega: angular velocity, three orthogonal directions

    velocity: relative to what???
    """

    def __init__(self, size=None, 
                t=0, m=None, r=None, omega=None, velocity=None, mu=None):

        # resolution
        size = size or (4, 4)

        self.red = []
        self.green = []
        self.blue = []

        self.size = size
        self.history = None
        self.delta = False

        self.last_ball = None
        self.next_ball = None
        self.fade = 1 / math.e
        self.t = t

        # Default for mass??
        if mu and m:
            m = gauss(m, mu)
            
        self.M = m
        
        self.omega = omega or [random() for x in range(3)]
        self.velocity = velocity or [random() for x in range(3)]

        # radius corresponding to grid view???
        self.r = r
        
        # time moves slower in the inner spheres?
        # FIXME?
        self.sleep = 1 / self.size[0]

        self.reset(init=True)

        
    def reset(self, init=False):
        """ Reset the sphere """

        if self.M:
            self.setup_wave()

            # first time only, carry on?
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
        """ Change lists of red green blue to a quantised pixel grid"""
        grid = []
        for rgb in zip(self.red, self.green, self.blue):
            pixel = tuple(self.quantise(x) for x in rgb)
            grid.append(pixel)

        return grid
        

    async def run(self):
        """ Run a sphere 

        
        Does one tick for the sphere.

        so self.t is also a count of how often we've been here.

        at least in this thread.

        """

        self.t += 1

        if self.M:
            return await self.wave_run()
        
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
            self.blue[ix] = b

    def quantise(self, value):

        value = int(127 + (value * 128))
        value = int(value % 256)

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
            

    def setup_wave(self):
        """ Do some set up work for a sphere with mass """

        self.waves = {}
        self.inc = math.pi/20
        
        for c in 'rgb':
            phase = random()
            scale = 1 # was random() wondering if should just use 1?
            
            self.waves[c] = [c, phase, scale]


    def sample(self, x1, y1, x2, y2):
        """ Return a pixel given a rectangle 

        x1, y1, x2, y2 are real

        Want to select a point from a rectangle around this
        point.

        allowing the rectangle to wrap around, identifying the left right
        edges as well as the top and bottom.

        (perhaps make this optional?)
        """

        # radians per x-step
        deltax = 1 / self.size[0]
        deltax *= 2 * math.pi

        # radians per y-step
        deltay = 1 / self.size[1]
        deltay *= 2 * math.pi

        # width height of rectangle.
        xdelta = x2 - x1
        ydelta = y2 - y1

        # expansion or contraction modulus
        xk = int(xdelta / deltax)

        xk = xk or 1

        xx = int(x1 / deltax)

        xk2 = xk // 2
        xx = randint(xx-xk2, xx + xk - (1 + xk2))

        yk = int(ydelta / deltay)
        yk = yk or 1

        yy = int(y1 / deltay)

        yk2 = yk // 2
        yy = randint(yy - yk2, yy + yk - (1 + yk2))

        ix = (yy * self.size[0]) + xx

        return self.red[ix], self.green[ix], self.blue[ix]
    

    async def wave_run(self):
        """ wave

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

                yy = (y / n2) + (1 / (2 * n2)) * 2 * math.pi
                yy += self.inc * self.t

                rc, rphase, rscale = self.waves['r']
                gc, gphase, gscale = self.waves['g']
                bc, bphase, bscale = self.waves['b']
                
                value = (
                    sample_wave(rphase, xx) * rscale,
                    sample_wave(bphase, yy) * bscale,
                    # scratches head and wonders if xx is ok in next line
                    sample_wave(gphase, xx) * gscale)

                grid.append(value)

        self.grid2rgb(grid)

        
class NeutronStar:
    """

    An inner sphere 
    
    Just supply the mass.

    or... maybe a bit more complex.

    So, nest some waves and figure out project and sample.

    So what radii are interesting?

    Each star, or galaxy can have its own process, and a pi can run a
    good few stars.

    
    """
    def __init__(self):
        pass
        
            

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

    def __init__(self, parent, balls=None):
        """ Initialise the thing """

        super().__init__(parent)

        # expect we'll find something to do with a queue
        self.uq = curio.UniversalQueue()

        self.build(balls)
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
        self.dball %= len(self.balls)

    async def backward(self):
        """ Move to previous sphere """
        self.dball -= 1
        if self.dball < 0:
            self.dball = len(self.balls) - 1

    def build(self, balls):
        """ Create the balls """
        # add a bunch of spheres to the queue
        self.balls = []
        last_ball = None
        ball = 0
        
        for nn in balls:

            size = nn

            size = (size, size)

            M, mu = 1.0, 0.1

            #if ball and ball != self.n -1:
            if ball:
                M, mu = None, None

            sphere = Sphere(size, m=M, mu=mu)

            if last_ball:
                sphere.last_ball = last_ball
                last_ball.next_ball = sphere
                
            # may need to revisit this, spread some work
            self.uq.put(sphere)
            self.balls.append(sphere)

            last_ball = sphere

            # next ball
            ball += 1


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

        ball = self.balls[xx]
        print(xx, 'lucky for some', ball.size, ball.M)

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


def prime_balls(base, n):
    """ Generate next n primes starting at base"""

    for nn in range(base, 1000_0000):
        
        if not prime.isprime(nn):
            continue

        print('prime', nn)
        yield nn

        n -= 1
        if n == 0:
            return

def pi_balls(base, n):
    """ Generate next n pi-based balls starting at base 

    pi = 4 * sum((-1)^n * (1/(1 + (2*n))))
    """
    # for now, punt to prime balls
    return prime_balls(base, n)
            

            
class CelestialSphere(NestedWaves):
    """ An outer sphere of nested waves

    Embed random neutron stars in a de Sitter Space

    Present a window onto this sphere to inner layers.

    N = a / M for number of stars

    Give them mass, velocity to get ball rolling

    Each star does its own thing, schedules itself to run.

    Stars collide -- for now do pass through.

    Just model gravitational wave

    reflect what passes its way
    """
    def __init__(self, parent, a=1, n=None, m=None):
        """Initialise.

        *a* is the size of the universe

        *m* the mean mass of galaxies.

        *n* is the number of galaxies.

        However, we assume:

            n = a / m

        By setting a = 1 as a default, you can control the 
        expected number of galaxies by setting m to 1/n.


        So, for ~7 galaxies, set m to 1/7 or just supply n == 7


        Where to put the galaxies?

        Should really put them in de Sitter Space

        A 4-dimensional subspace of a 5 dimensional Minkowski space

        metric

        ds**2 = sum ((x[i] - y[i]) ** 2) - (t - u) ** 2)

        R = sum  ((x[i] - y[i]) ** 2) - (t - u) ** 2)) ** 0.5


        For now just place randomly in unit sphere with random velocity?

        Relative to the centre of the unit sphere?

        But try to set it to be in sync with the existing balls ***

        So don't need velocity after all.

        Just record each run what it is, balanced by the grid.

        For now everything is on a p * p grid, with p grids to make a cube.

        Each grid can be viewed as the surface of a sphere, latitude and
        longitude grids.

        Aim to be able to navigate the grid of galaxies.
        
        Some interesting possibilities arise as sizes of grids vary.

        Elliptic curves and modular forms???
        """

        super().__init__(parent)

        n = n or a / m
        a = a or n * m
        m = a / n

        self.n = n
        self.m = m
        self.a = a


    def build(self):
        """ Create the balls

        Really should place them in the five dimensions,

        but have a constraint that gets us down to four dimensions.

        For now, place them randomly in a unit cube.
        """
        self.balls = {}
        for wave in range(self.n):
            
            self.ball[wave] = Sphere(m=1, mu=0.1)

            # where is it?  what's the observer?

        

    async def run(self):
        """ ??? """
        

def argument_parser():

    parser = argparse.ArgumentParser()

    parser.add_argument('--gallery', nargs='*', default=['.', '../gallery'])
    parser.add_argument(
        '--snowy', action='store_true',
        help='random cat pictures')
    parser.add_argument(
        '--name', default='tree',
        help='what to show')
    parser.add_argument('-a', type=int, default=1)
    parser.add_argument('-n', type=int, default=10)
    parser.add_argument('-m', type=int, default=1)
    parser.add_argument('--inc', type=int, default=4)
    parser.add_argument('--base', type=int, default=20)

    return parser

def random_prime_balls(nmin, nmax):
    """ generate a random prime balls """
    while True:
        base = random.randint(nmin, nmax)
        ball = list(prime_balls(base, random.randint(3, 13)))
        yield ball
    
def main():

    parser = argument_parser()

    args = parser.parse_args()

    # pass list of balls into NestedWaves

    balls = list(prime_balls(args.base, args.n))
    
    #for ball in random_prime_balls(args.base, 127):
    #    balls.append(ball)

    farm = pigfarm.sty(NestedWaves, dict(balls=balls))

    curio.run(farm.run(), with_monitor=True)
            

if __name__ == '__main__':

    main()




        

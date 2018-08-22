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

Update: 2018/8/9

The motivation for using grids with prime dimensions was that it makes it makes
it challenging for the spheres to stay in sync with each other.

Their periods are co-prime.

As a result, spirals emerge.

In the initial runs there was a strong diagonal property developing.

A smooth, square, space in the top left corner.

A more random square bottom right, with the corners of these two squares meeting.

Much symmetry for the bands to the top and left of the view.

My interpretation is these bands show the layers largely being in sync.

Regardless, another view of these grids is to view them from the north or south
pole.  When you do that there are spirals everywhere.

"""
import math

import argparse

from collections import deque, defaultdict, Counter, namedtuple

import curio

import numpy

from PIL import Image, ImageTk

from karmapi import base, tpot, prime, pigfarm

from random import random, randint, gauss, shuffle

class Sphere:
    """ If it hass mass (m) then pass through waves

    Regardless, show the view at radius r from centre of mass.

    omega: angular velocity, three orthogonal directions

    velocity: relative to what???
    """

    def __init__(self, size=None, 
                t=0, m=None, r=None, omega=None, velocity=None, mu=None,
                twist=True):

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

        self.twist = True

        #self.fade = 1 / math.e
        self.fade = 1

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

        self.red.clear()
        self.green.clear()
        self.blue.clear()

        self.random_grid()

        return

    async def more_sleepy(self):
        """ Make the ball sleep more """
        self.sleep *= 2


    async def more_wakey(self):
        """ Make the ball sleep less """
        self.sleep /= 2


    def random_grid(self):

        size = self.size
        for pt in range(size[0] * size[1]):
            self.red.append(randunit())
            self.green.append(randunit())
            self.blue.append(randunit())


    def project(self, view=None):
        """ Turn into a PIL? """

        views = dict(
            grid=self.rgb2grid,
            northpole=self.northpole,
            southpole=self.southpole,
            uphemi=self.uphemi,
            lowhemi=self.lowhemi)
            
        image = Image.new('RGB', (self.size[0], self.size[1]))

        # FIXME do the 256 magic int stuff here

        #print('rgb', len(self.red), len(self.green), len(self.blue))

        project = views.get(view, self.rgb2grid)
        print(view)
        
        image.putdata(project())

        return image

    def rgb2grid(self):
        """ Change lists of red green blue to a pixel grid"""
        grid = []
        for rgb in zip(self.red, self.green, self.blue):
            pixel = tuple(self.quantise(x) for x in rgb)
            grid.append(pixel)

        return grid

    def poleview(self, pixels, scale=1, wind=1):
        """ View from a pole """
    
        # make black everywhere
        width, height = self.size

        
        grid = [(127, 127, 127)] * width * height

        xorig = int(width / 2)
        yorig = int(height/ 2)
        
        for ix, rgb in enumerate(pixels):

            pixel = tuple(self.quantise(x) for x in rgb)
            xx = ix % width
            yy = ix // height

            #if yy >= height / 2:
            #    break
                        
            # so radius yy from centre and xx how far round the circle
            angle = wind * xx * 2 * math.pi / width
             
            xoff = yy * math.cos(angle) / scale
            yoff = yy * math.sin(angle) / scale

            xpos = int(xorig + xoff)
            ypos = int(yorig + yoff)

            target = xpos + ypos * width

            ix = ix % (width * height)

            target %= width * height
            
            grid[target] = pixel
            
        return grid

    def northpole(self):
        """ Give a circular view from the north pole """
        pixels = zip(self.red, self.green, self.blue)

        return self.poleview(pixels, scale=2)

    def southpole(self):
        """ Give a circular view from the south pole """
        pixels = zip(self.red[::-1], self.green[::-1], self.blue[::-1])

        return self.poleview(pixels, scale=2, wind=-1)

    def uphemi(self):
        """ show upper hemisphere """
        nn = int(len(self.red) / 2)
        pixels = zip(self.red[:nn], self.green[:nn], self.blue[:nn])

        return self.poleview(pixels)

    def lowhemi(self):
        """ show lower hemisphere """
        nn = int(len(self.red) / 2)
        pixels = zip(self.red[nn::-1], self.green[nn::-1], self.blue[nn::-1])

        return self.poleview(pixels, wind=-1)

    async def run(self):
        """ Run the sphere """

        while True:
            await self.tick()
            await curio.sleep(self.sleep)
        

    async def tick(self):
        """ Do one tick for the sphere

        so self.t is also a count of how often we've been here ??

        at least in this thread.

        """

        self.t += 1

        # Here if we are between two spheres
        # so have last_ball and next_ball

        # for each point in grid select corresponding
        # points in inner/outer spheres

        lb = self.last_ball
        nb = self.next_ball
        
        n1, n2 = self.size
        
        grid = [0] * n1 * n2
        ix = 0
        deltax = (1 / (2 * n1)) * 2 * math.pi
        deltay = (1 / (2 * n2)) * 2 * math.pi

        cbweight = self.weight(self)
        lbweight = (lb or self).weight(self)
        nbweight = (nb or self).weight(self)

        #cbweight = lbweight = nbweight = 1

        #print(cbweight, lbweight, nbweight)

        xgrid = list(range(n2))
        ygrid = list(range(n1))

        cbweight = lbweight = nbweight = 1
        print('weights', cbweight, lbweight, nbweight)

        shuffle(ygrid)
        for y in ygrid:
            curio.sleep(0)
            y1 = (y / n2) * 2 * math.pi
            y2 = y1 + deltay

            shuffle(xgrid)
            for x in xgrid:
                #curio.sleep(0)

                x1 = (x / n1) * 2 * math.pi
                x2 = x1 + deltax

                if lb:
                    lbc = lb.sample(x1, y1, x2, y2)
                else:
                    lbc = tuple(randunit() for c in 'rgb')
                    #lbc = (127, 127, 127)
                    #lbweight = 0
                    
                if nb:
                    nbc = nb.sample(x1, y1, x2, y2)
                else:
                    nbc = tuple(randunit() for c in 'rgb')
                    #nbweight = 0
                    #nbc = (127, 127, 127)

                
                tix = cix = (y * n1) + x

                if n1 == n2 and self.twist:
                    tix = (x * n1) + y
                        
                cbc = (self.red[cix], self.green[cix], self.blue[cix])

                value = [((aa * lbweight) +
                          (bb * cbweight) +
                          (cc * nbweight)) * (1 / math.e)
                              for aa, bb, cc in zip(lbc, cbc, nbc)]

                    
                grid[tix] = value

            

        self.grid2rgb(grid)
        #self.normalise()


    def weight(self, ball):

        delta_r = abs(ball.r - self.r)

        
        if delta_r == 0:
            return self.M or 1

        weight = (self.M or 1) / (delta_r ** self.fade)
        #print(delta_r, self.M or 1, self.fade, weight)

        return weight

            
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
    


        
class NeutronStar(Sphere):
    """

    An sphere with a mass
    
    Just supply the mass.

    or... maybe a bit more complex.

    So, nest some waves and figure out project and sample.

    So what radii are interesting?

    Each star, or galaxy can have its own process, and a pi can run a
    good few stars.

    
    """
    def reset(self, init=False):
        """ Reset the sphere """

        super().reset(init)
        self.setup_wave()


    async def tick(self):
        """ wave

        red, green, blue
 
        let's do:
           red up down
           blue left right
           green in and out all over

        How to fill in self.grid?
        """
        await super().tick()

        self.red = [x/10 for x in self.red]
        self.blue = [x/10 for x in self.blue]
        self.green = [x/10 for x in self.green]

        n1, n2 = self.size
        width = 2 * math.pi
        height = math.pi

        ix = 0
        for x in range(n1):
            xx = ((x / n1) + (1 / (2 * n1))) * 2 * math.pi

            xx += self.inc * self.t
                
            for y in range(n2):

                yy = (y / n2) + (1 / (2 * n2)) * 2 * math.pi
                yy += self.inc * self.t

                rc, rphase, rscale = self.waves['r']
                gc, gphase, gscale = self.waves['g']
                bc, bphase, bscale = self.waves['b']

                self.red[ix] += sample_wave(rphase, xx) * rscale
                self.blue[ix] += sample_wave(bphase, yy) * bscale

                # not sure xx is the right thing here
                self.green[ix] += sample_wave(gphase, xx) * gscale

                ix += 1
                
            #await curio.sleep(0)


def randunit():

    x = random()
    if random() > 0.5:
        x *= -1

    return x / 10
        
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

    def __init__(self, parent, balls=None, fade=1, twist=True):
        """ Initialise the thing """

        super().__init__(parent)

        # expect we'll find something to do with a queue
        #self.uq = curio.UniversalQueue()

        self.views = ['grid', 'northpole', 'southpole', 'uphemi', 'lowhemi']
        self.view = 0
        self.fade = fade
        self.twist = twist

        self.build(balls)
        self.add_event_map(' ', self.pause)
        self.paused = False
        self.add_event_map('r', self.reset)
        
        self.dball = 0
        self.add_event_map('j', self.backward)
        self.add_event_map('k', self.forward)
        self.add_event_map('v', self.next_view)
        self.add_event_map('b', self.previous_view)
        self.add_event_map('d', self.lessfade)
        self.add_event_map('f', self.morefade)
        self.add_event_map('s', self.more_sleepy)
        self.add_event_map('w', self.more_wakey)
        self.add_event_map('t', self.toggle_twist)


    async def lessfade(self):
        """ Decrease r exponent """
        self.fade -= 1
        print(f"metric: 1 / (r ** {self.fade})")

    async def morefade(self):
        """ Increase r exponent """
        self.fade += 1
        print(f"metric: 1 / (r ** {self.fade})")

    async def more_sleepy(self):
        """ Sleep more

        Tell each ball and self to sleep more
        """
        await self.sleepy()

        for ball in self.balls:
            await ball.more_sleepy()


    async def more_wakey(self):
        """ Sleep less

        Tell each ball and self to sleep less
        """
        await self.wakey()

        for ball in self.balls:
            await ball.more_wakey()

    async def toggle_twist(self):
        """ Toggle 90 degree twist 

        Tell each ball to toggle twist
        """
        self.twist = not self.twist
        
        for ball in self.balls:
            ball.twist = self.twist

    
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

    async def next_view(self):
        """ next view """
        self.view += 1
        self.view %= len(self.views)

    async def previous_view(self):
        """ previous view """
        if self.view:
            self.view -= 1
        else:
            self.view = len(self.views) - 1

    def build(self, balls):
        """ Create the balls """
        # add a bunch of spheres to the queue
        self.balls = []
        last_ball = None
        
        for sphere in balls:
            
            if last_ball:
                sphere.last_ball = last_ball
                last_ball.next_ball = sphere
                
            # may need to revisit this, spread some work
            # self.uq.put(sphere)
            print('adding ball', sphere.size)
            sphere.fade = self.fade
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

        ball = self.balls[xx]
        print(xx, 'lucky for some', ball.size, ball.M)

        await self.draw_ball(ball)

            
    async def draw_ball(self, ball):
        """ wc has everything???? 

        feels like I have written this bit 20 times
        """
        width, height = self.width, self.height

        image = ball.project(self.views[self.view])
        
        image = image.resize((int(width), int(height)))

        self.phim = phim = ImageTk.PhotoImage(image)

        xx = int(self.width / 2)
        yy = int(self.height / 2)
        self.canvas.create_image(xx, yy, image=phim)

    async def start_balls_running(self):

        spheres = []
        for ball in self.balls:
            sphere = await curio.spawn(ball.run)
            spheres.append(sphere)
            
        return sphere


    async def run(self):
        """ Run the waves """

        self.sleep = 0.05

        
        self.set_background()

        #await self.random_step_some()

        #await self.backward_step_all()

        spheres = await self.start_balls_running()
        
        while True:
            if self.paused:
                await curio.sleep(self.sleep)
                continue
            
            self.canvas.delete('all')

            await self.draw()
            #await self.step_balls()
            #await self.backward_step_all()
            
            await curio.sleep(self.sleep)

        curio.join(spheres)


def generate_spheres(sizes, clazz=None):

    clazz = clazz or NeutronStar
    xclazz = clazz
    
    first = True
    sizes = list(sizes)

    K = 2
    for r, nn in enumerate(sizes[:-1]):

        size = nn

        size = (size, size)

        M = 1.0 * K

        mu = M / 10

        R = 2 * r

        #M = M / (R+1)
        mu = M / 10

        sphere = clazz(size, r=R, m=M, mu=mu)

        clazz = Sphere

        yield sphere

    # Add an outer sphere too
    size = sizes[-1]
    size = (size, size)

    #M = 10 * M
    #mu = M / 10
    print(xclazz)
    yield xclazz(size=size, r=r+1, m=M, mu=mu)
        

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
        

def argument_parser(parser=None):

    parser = parser or argparse.ArgumentParser()

    parser.add_argument('-a', type=int, default=1)
    parser.add_argument('-n', type=int, default=10)
    parser.add_argument('--twist', type=bool, default=True)
    parser.add_argument('--fade', type=int, default=1)
    parser.add_argument('--stride', type=int)
    parser.add_argument('-m', type=int, default=1)
    parser.add_argument('--base', type=int, default=20)

    return parser

def random_prime_balls(nmin, nmax):
    """ generate a random prime balls """
    while True:
        base = random.randint(nmin, nmax)
        ball = list(prime_balls(base, random.randint(3, 13)))
        yield ball


def args_to_spheres(args):
    
    if args.stride:
        stride = args.stride
        start = args.base
        end = start + (args.n * args.stride)
        
        balls = range(start, end, stride)
    else:
        balls = prime_balls(args.base, args.n)

    print('balls', balls)
    spheres = list(generate_spheres(balls))

    return spheres
    
        
def main():

    parser = argument_parser()

    args = parser.parse_args()

    # pass list of balls into NestedWaves
    spheres = args_to_spheres(args)
    
    farm = pigfarm.sty(NestedWaves, dict(balls=spheres, fade=args.fade,
                                         twist=args.twist))

    curio.run(farm.run(), with_monitor=True)
            

if __name__ == '__main__':

    main()




        

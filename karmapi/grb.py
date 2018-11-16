"""
Are gamma-ray bursts optical illusions?

Robert S MacKay, Colin Rourke

http://msp.warwick.ac.uk/~cpr/paradigm/GammaRayBursts.pdf

What is it like when a galaxy emerges into view at the edge of our visible
universe?

In what follows I am imagining a wider universe that has the similar uniform
structure.

It appears spirals are a natural thing to arise and perhaps we just see a
window on an expanding arm of a giant spiral of galaxies.

If we go with this, then from the perspective of the galaxy (the emitter of
light just coming into view from our world) nothing unusual is happening, it is
just cruising along, just like our galaxy.

What paths have the light waves have taken to get to us and how
long that journey was?

Note also the new addition to our inertial field, settling in.

Update
======

The emitter itself does not need to enter our visible universe.  All that is
required is a beam of light from that emitter that enters our visible universe,
and is heading in our direction.

Colin::

   Not quite right.  All we ever see of anything is light.  Sending light
   to us is the same as being in our universe

There was lots more from Colin. See docs/nodice/grb.rst for more on that
story.

Now if a gamma-ray burst indicates a new galaxy arriving in our visible
universe, with the burst representing the, finite, but unbounded history of the
universe, including the histlory of its inertial drag field.

This latter, is hypothesised to be driven by a super-massive object (~10^11
solar masses) at the centre of the galaxy.

Noting that this field decays linearly with distance, but extends well beyond
the visible part of the galaxy.

When a galaxy comes into view, not just a big slice of time, but also a large
expanse of space becomes visible in a short space of time.

I picture this as a wave, like a sunrise, sweeping across our solar system.

We see gamma ray bursts lasting several minutes, with the frequency rising
rapidly to a sharp peak before slowly tailing off over the next several
minutes.

It is hypothesised that the gravitational wave that is seen will broadly follow
the shape of the gamma-ray, but over a longer time span.

It is hypothesised that large masses in our solar system will act to amplify
the signal.

The result will be echo cancellation due to the different paths that the
gravitational wave can take.

Echoes will bounce around the solar system as bodies follow the incoming wave
together.

It also has to be noted that the earth too will act to echo the wave it sees.

Consider the moon, earth and sun.  It takes just 1.3 seconds for light to travel
from earth to moon or vice versa.

From moon or earth to the sun is around 500 seconds, or 8 minutes 20 seconds.

Place the earth at the origin and then picture the different path lenghts.

So,

    P = location of GRB emitter
    M = location of moon
    S = location of sun
    E = earth, location (origin)

Lengths of interest::

    deltaS = PSE - PE 

    deltaM = PSME - PSE = SME - SE

Now deltaM is independent of P.

Given the location in the sky that the GRB actually comes from, we can also get
a better estimate on deltaS.

We may also be able to work this backwards: given a signal that will place some
constraints on the geometry.

Jupiter?  other planets?

For now the goal is given a time and a place in the sky P, draw a picture?
""" 

import math
import numpy as np
import argparse

import datetime

from astropy import coordinates, constants
from astropy.time import Time

from matplotlib import pyplot as pp

import curio

from karmapi import base, cpr, pigfarm

def angle(d, m, s):

    a = s
    a = m + a / 60
    return d + (a / 60)

LIGO_HLAT = angle( 46, 27, 18.52)
LIGO_HLON = angle(119, 24, 27.56)

LIGO_LLAT = angle(30, 33, 46.42)
LIGO_LLON = angle(90, 46, 27.27)


class SolarSystem(cpr.NestedWaves):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)


    def draw(self):
        """ Draw the balls """
        ball = self.balls[self.dball]
        print('current ball', ball.name, ball)

        for body in self.balls:
            name = body.name
            where = body.body.transform_to(ball.body)
            #print(name, where)
            print(name, where.ra, where.dec)

            self.canvas.draw
            
        print()

def gamma_hack():

    T = 1000
    k = 10000

    xx = [x * math.pi / k for x in range(T)]
    shint = np.array([math.sinh(x) for x in xx])
    cosht = np.array([math.cosh(x) for x in xx])
    print(shint.size)
    #print(xx[-100:])
    #print(yy[-100:])

    pp.plot(list(shint), list(cosht))


    # emitter
    shinu = shint.copy()
    coshu = cosht.copy()

    alpha = 2
    beta  = 1
    gamma = -1
    delta = 1
    e0 = (alpha * shinu) + (beta * coshu)
    e1 = (gamma * shinu) + (delta * coshu)

    # 2.2

    geo_test = - (e0 * shint) + (e1 * cosht)

    pp.plot(geo_test)

    pp.show()


    # TODO plot t against u: receiver and emitter times respectively


def argument_parser(parser=None):

    parser = parser or argparse.ArgumentParser()

    parser.add_argument('--lat', type=float, default=LIGO_HLAT)

    parser.add_argument('--lon', type=float, default=LIGO_HLON)

    parser.add_argument('--date', default='2015/09/14/09/50/45')

    return parser


def get_body(body, t=None):

    t = t or datetime.datetime.now()

    return coordinates.get_body(body, Time(t))


def get_mass(body):

    # masses (10^24 Kg)
    em = 5.97
    
    to_earth = 1.0 / em

    masses = dict(
        moon =      0.073 * to_earth,
        mercury =   0.330 * to_earth,
        venus =     4.87  * to_earth,
        mars =      0.64  * to_earth,
        earth =     1.0,
        jupiter =  1898 * to_earth,
        saturn =  568.0 * to_earth, 
        uranus =   86.8 * to_earth,
        neptune = 102.0 * to_earth,
        pluto =     0.0146 * to_earth)

    sun = masses['jupiter'] * (constants.GM_sun / constants.GM_jup)
    masses['sun'] = sun

    return masses.get(body)


BODIES = [
    'sun', 'moon',
    'mercury', 'venus',
    'earth',
    'mars', 'jupiter', 'saturn',
    'neptune', 'uranus']

RADIUS_OF_EARTH = 6378.
RADIUS_OF_SUN =   1.391e6
    
def au2earth(value=1):
    """ Convert astronomical units to earth radii """

    # earth to sun
    e2s = float(constants.c.to('km/s').value) * 499.0
    print(e2s)
    return value * e2s / 6378
    

def display_body(name, t):
        
    print("Time of event:", t)
    print("Viewing from:", name)
    target = get_body(name, t)
    results = {}
    for body in BODIES:
        print(body)

        bd = body_data(body, t)

        mass = bd['m']
        bod = bd['body']
        
        if body == name:
            if name in ['earth', 'sun']:
                r = bd['r']
        else:
            r = target.separation_3d(bod)

        print(bod)
        print('mass:', mass)
        print(f'distance to {name}: {r}')
        print('m over r:', mass / r)
        print()
        print()

    return results

def get_distance():
    pass

def body_data(name, t):
    
    bod = get_body(name, t)
    mass = get_mass(name)
    radius = None
    if name == 'earth':
        radius = 6378 / 1.5e8
    elif name == 'sun':
        radius = 1.391e6 / au2earth(1)

    return dict(
        r=radius,
        m=mass,
        name=name,
        body=bod)


class Body(cpr.Sphere):


    def __init__(self, name, t, size=None):
        """ Initialise the body """
        self.name = name
        bd = body_data(name, t)
        self.body = bd['body']

        super().__init__(size=size, t=t.timestamp(), m=bd['m'], r=bd['r'])

    def tick(self):

        return self
    
    def separation(self, body):
        """ Return distance to body """
        return self.body.separation_3d(body)


def args_to_spheres(args, t):

    spheres = []
    for body in BODIES:
        spheres.append(Body(body, t=t))

    return spheres

def main():

    parser = argument_parser(cpr.argument_parser())
    
    args = parser.parse_args()

    print(args.date)
    args.date = base.parse_date(args.date)

    t = args.date

    earth = display_body('earth', t)
    sun = display_body('sun', t)


    for k,v in earth.items():
        print(f'{k}: {v["moverr"]}')


    # pass list of balls into NestedWaves
    spheres = args_to_spheres(args, t)
    
    farm = pigfarm.sty(SolarSystem, dict(balls=spheres, fade=args.fade,
                                         twist=args.twist))

    curio.run(farm.run, with_monitor=True)



if __name__ == '__main__':

    main()
        

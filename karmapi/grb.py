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
universe, including the history of its inertial drag field.

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
import requests
import json
from pathlib import Path

from datetime import datetime as dt
from datetime import timedelta

from astropy import coordinates, constants
from astropy.time import Time

import curio

from matplotlib import pyplot as plt

import blume
from blume import magic, farm

from karmapi import cpr


# Much thanks for all involved in this:
OBSERVATIONS = 'https://www.gw-openscience.org/catalog/GWTC-1-confident/json/'

GRB_20170818_0224 = """

J1243.9-1135	07012051001	12 43 51.26	-11 35 06.28	Aug 18, 2017 02:22:00	Aug 28, 2017	120.341	119.873	128	Aug 29, 2017
J1245.4-1154	07012052001	12 45 22.41	-11 54 01.4	    Aug 18, 2017 02:25:00	Aug 28, 2017	123.173	122.995	130	Aug 29, 2017
J1246.9-1213	07012053001	12 46 53.91	-12 12 34.99	Aug 18, 2017 02:27:00	Aug 28, 2017	122.849	120.104	128
"""

def angle(d, m, s):

    a = s
    a = m + a / 60
    return d + (a / 60)

LIGO_HLAT = angle( 46, 27, 18.52)
LIGO_HLON = angle(119, 24, 27.56)

LIGO_LLAT = angle(30, 33, 46.42)
LIGO_LLON = angle(90, 46, 27.27)


class SkyMap(magic.Ball):

    def __init__(self, balls, planets, *args, **kwargs):

        super().__init__()
        self.sleep = 1
        self.balls = balls
        self.planets = planets

        #self.add_event_map('r', self.reverse)

    async def reverse(self):
        """ Rongo Rongo change direction """
        self.paused = False
        for ball in self.balls:
            ball.inc *= -1

    async def run(self):
        """ Draw the balls """
        #ball = self.balls[self.dball]
        #print('current ball', ball.name, ball)

        fig = plt.figure()

        locs = [self.decra2rad(
            ball.body.dec.value,
            ball.body.ra.value) for ball in self.balls]

        print(locs[:10])

        fig.clear()
                
        #ax = fig.add_axes((0,0,1,1), projection='mollweide')
        ax = fig.add_subplot(1, 1, 1,
                             projection='mollweide')

        ax.set_title(str(self.planets[0].t), color='white')
        for planet in self.planets:
            planet.tick()
            print(planet.body)

        print([x.body.ra for x in self.planets])
        ax.scatter([xx[1] for xx in locs], [xx[0] for xx in locs],
                   c=[x.distance for x in self.balls])

        ax.scatter([x.body.ra.radian - math.pi for x in self.planets],
                   [x.body.dec.radian for x in self.planets], color='r')

        for pp in self.planets:
            ax.text(pp.body.ra.radian - math.pi, pp.body.dec.radian + math.pi/10,
                    pp.name, color='yellow')
        ax.axis('off')

        await self.outgoing.put(magic.fig2data(plt))

        fig.clear()

        ax = fig.add_subplot(111)
        rv = [xx.data.get('radial_velocity', 0.0) or 0. for xx in self.balls]
        distance = [xx.data.get('distance', 0.0) or 0. for xx in self.balls]

        rrv = []
        dd = []
        for vel, dist in zip(rv, distance):
            if dist > 12:
                continue
            
            if vel == 0.0:
                # use Hubble relationship
                vel = dist * 70.
            rrv.append(vel)
            dd.append(dist)

        ax.scatter(dd, rrv)

        #await curio.sleep(self.sleep)
        #await self.outgoing.put(magic.fig2data(fig))
        #await curio.sleep(self.sleep)

        #await self.outgoing.put(magic.fig2data(fig))
        fig.clear()
        ax = fig.add_subplot(111)
        ax.plot(distance)
        #await self.outgoing.put(magic.fig2data(fig))

        fig.clear()
        ax = fig.add_subplot(111)
        ax.plot([xx[1] for xx in locs])
        #await self.outgoing.put(magic.fig2data(fig))


    def decra2rad(self, dec, ra):

        return dec * math.pi / 180, (ra - 12) * math.pi / 12.
        

    def latlon2xy(self, lat, lon):
        """ Convert lat lon to yard coordinates """
        if lon < 0:
            lon += 360.
        lon += 180
        lon %= 360

        xscale = 360.0 / self.width
        yscale = 180.0 / self.height

        xx = int(lon / xscale)
        yy = int((90 + lat) / yscale)
 
        return xx, yy
        
        
def gamma_hack():

    from matplotlib import pyplot as pp

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

    #parser.add_argument('--date', default='2015/09/14/09/50/45')
    #parser.add_argument('--date', default='2017/08/14')
    parser.add_argument('--date', default='2017/08/17')

    parser.add_argument('--grb', default='170817A')
    parser.add_argument('--gw', help="file for latest ligo data")
    parser.add_argument('--galaxy', help="file of local galaxy data")

    return parser


def get_body(body, t=None):

    t = t or dt.now()

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

    return masses.get(body, 1.)


BODIES = [
    'sun', 'moon',
    'mercury', 'venus',
    'earth',
    'mars', 'jupiter', 'saturn',
    'neptune', 'uranus']
#BODIES = coordinates.solar_system_ephemeris.bodies

RADIUS_OF_EARTH = 6378.
RADIUS_OF_SUN =   1.391e6
    
def au2earth(value=1):
    """ Convert astronomical units to earth radii """

    # earth to sun
    e2s = float(constants.c.to('km/s').value) * 499.0
    #print(e2s)
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


class Body(magic.Ball):


    def __init__(self, name, t, size=None):
        """ Initialise the body """

        super().__init__()

        self.name = name
        self.t = t
        self.inc = 3600 * 6

        self.set_body()

    def set_body(self):

        bd = body_data(self.name, self.t)
        self.body = bd['body']
        self.data = bd

    def tick(self):

        self.t += timedelta(seconds=self.inc)
        return self.set_body()

    async def run(self):

        self.tick()
    
    def separation(self, body):
        """ Return distance to body """
        return self.body.separation_3d(body)


def args_to_spheres(args, t):

    spheres = []
    for body in BODIES:
        bod = Body(body, t=t)
        bod.distance = 0
        spheres.append(bod)

    grb = {}
    grb['170817A'] = (176.8, -39.8)  # RA DEC

    if args.grb in grb:
        ra, dec = grb.get(args.grb)

        gbod = Body('sun', t=t)
        gbod.body = coordinates.SkyCoord(ra, dec, unit='deg')
        gbod.distance = 0.0
        gbod.name = args.grb
        spheres.append(gbod)

    return spheres

def dump(spheres):

    for a in spheres:
        
        for b in spheres:
            if a is b: continue
            xx = b.body
            yy = xx.transform_to(a.body)
            print(f'{a.name} {b.name} {xx.ra.value - yy.ra.value} {xx.dec.value - yy.dec.value}')
            print(f'zzzzzzz {a.name} {b.name} {yy.ra.value} {yy.dec.value}')
        print

def sun(t=None):

    return get_body('sun', t)

def moon(t=None):

    return get_body('moon', t)

def earth(t=None):

    return get_body('earth', t)

def jupiter(t=None):

    return get_body('jupiter', t)


def get_waves(path=None):

    if path.exists():
        with path.open() as infile:
            return json.load(infile)

    resp = requests.get(OBSERVATIONS)

    data = json.loads(resp.content.decode('utf-8'))
    print(type(data))

    if path is not None:
        with path.open('w') as outfile:
            json.dump(data, outfile, indent=True)

    return data


def parse_date(date):
    """ Parse a date """
    if date is None:
        return date

    fields = [int(x.strip()) for x in date.split('/')]
                  

    while len(fields) < 3:
        fields.append(1)

    while len(fields) < 6:
        fields.append(0)
    
    year, month, day, hour, minute, second = fields

    return dt(year, month, day, hour, minute, second)


class Bod(object):

    def __init__(self, ra, dec):
        self.body = coordinates.SkyCoord(ra, dec, unit='deg')

async def run(args):


    print(args.date)
    args.date = parse_date(args.date)

    t = args.date

    earth = display_body('earth', t)
    sun = display_body('sun', t)


    for k,v in earth.items():
        print(f'{k}: {v["moverr"]}')



    # pass list of balls into NestedWaves
    planets = args_to_spheres(args, t)

    print("GOT solar system", len(planets))

    spheres = []
    if args.galaxy:
        gals = list(near_galaxies(open(args.galaxy)))

        gals = [cleanse(gal) for gal in gals]

        print('clean galaxy data')
        print(gals[0])

        for gal in gals:
            #gbod = Body('sun', t=t)
            ra = gal['ra']
            dec = gal['dec']
            gbod = Bod(ra, dec)
            gbod.distance = gal['distance']
            gbod.data = gal
            #gbod.body = coordinates.SkyCoord(ra, dec, unit='deg')

            gbod.name = gal['name']

            spheres.append(gbod)

    print("GOT spheres", len(spheres))

    the_farm = farm.Farm()

    ss = SkyMap(balls=spheres, planets=planets, fade=args.fade,
                twist=args.twist)

    the_farm.add_edge(ss, the_farm.carpet)
    the_farm.add_edge(farm.GuidoClock(), the_farm.carpet)
    #spheres = cpr.args_to_spheres(args)
    #farm.add(cpr.NestedWaves, dict(
    #    balls=spheres, fade=args.fade,
    #    twist=args.twist))

    the_farm.setup()
    starter = await curio.spawn(the_farm.start())

    print('farm runnnnnnnnnning')
    runner = await the_farm.run()
    

def gravity_waves(path):
    """ Read or download gravity wave observations """
    waves = get_waves(path)

    data = waves['data']

    print(json.dumps(waves['parameters'], indent=True))

    rows = []
    for name, fields in data.items():
        print()
        print(name)
        row = dict(name=name)
        
        #fields['name'] = name
        
        for k, v in fields.items():
            print(k, v['best'])
              

        for k, v in fields.items():
            row[k] = v.setdefault('best')
            print(f"{v['best']}", end=', ')
        print()

        rows.append(row)

    return rows

def tokens(line, sep=','):
    """ Split line into tokens """
    return [x.strip() for x in line.split(sep)]

def near_galaxies(infile):
    """ parse galaxy.txt from 

    https://heasarc.gsfc.nasa.gov/w3browse/all/neargalcat.html

    """
    header = tokens(infile.readline())
    print(header)
    for row in infile:
        fields = tokens(row)
        yield dict(zip(header, fields))


def parse_radec(value):

    d, m, s = [float(s) for s in value.split()]

    scale = 1
    if d < 0:
        d *= -1
        scale = -1

    d += m / 60.
    d += s / 3600.

    return d * scale
    
def cleanse(data):

    clean = {}

    for key, value in data.items():

        try:
            value = float(value)
        except:
            pass

        if key in ('ra', 'dec'):
            value = parse_radec(value)
            
        clean[key] = value

    return clean

if __name__ == '__main__':


    parser = argument_parser(cpr.argument_parser())
    
    args = parser.parse_args()



    if args.gw:
        rows = gravity_waves(Path(args.gw))

        import pandas

        df = pandas.DataFrame(rows)
        print(df.describe())
    else:

        curio.run(run(args))
        

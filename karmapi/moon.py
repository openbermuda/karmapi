"""
Moon or moai

Electromagnetic balls of wonder dancing together.

Ahu bus stops

and the number 7 bus.

May Day Parade

Winter Solstice

Spring Tide Mays

And October blaze.


So far now, simulate moai.  

And orongo.


"""

import datetime

NEW = datetime.datetime(1900, 1, 1, 5, 50)

NEXTNEW = datetime.datetime(1900, 1, 30, 5, 22)


delta = (NEXTNEW - NEW)

deltas = delta.days * 24 * 3600

print(delta.days)

deltas += delta.seconds

print(deltas)


latest = datetime.datetime(2017, 11, 18, 3, 43)

ldelta = latest - NEW


seconds = ldelta.days * 24 * 3600
seconds += ldelta.seconds

print(seconds, seconds / deltas)

current = NEW
for x in range(100):
    print(current)

    current += delta

from collections import deque
from math import pi

class queue(deque):

    def __init__(self):

        super().__init__(self)

        self.value = 0.0
    
    def value(self):

        return self.value

    def tick(self):

        self.value /= pi
    
class stop:
    """ Or Ahu, a bus depot """

    def __init__(self, x=None, y=None):

        self.queue = queue()

        self.x = x
        self.y = y

    async def echo(self, depot=None):

        value = 0.0
        for item in depot:
            value += depot.value()

        self.value += value / 2
        return self.value

    def add(self, moai):

        # fixme push according to direction of travel
        self.queue.push(moai)

class moai:

    def __init__(self, m=1, x=0, y=0, z=0, t=0):

        self.x = x
        self.y = y
        self.z = z
        self.t = t

    async def tick(self):

        self.t += 1

        # loop to t udating position
        for d in range(self.t):
            # magnus magnus son needed
            pass    
            

if __name__ == '__main__':

    import argparse
    from pathlib import Path

    parser = argparse.ArgumentParser()

    AHU = dict(
        orongo = stop(y=-27.1874, x=-109.4431),
        ranoraraku = stop(y=-27.1220, x=-109.2889),
        rrq =        stop(y=-27.1263, x=-109.2885),
        tongariki =  stop(y=-27.1258, x=-109.2769),
        akivii =     stop(y=-27.1150, x=-109.3950),
        hanavarevare = stop(y=-27.1167, x=-109.4167),
        tepeu =      stop(y=-27.1024, x=-109.4163),

        xx1 =        stop(y=-27.0950, x=-109.4108),
        xx2 =        stop(y=-27.1236, x=-109.4215),
        xx3 =        stop(y=-27.0933, x=-109.4098),
        xx4 =        stop(y=-27.0887, x=-109.4074),
        xx5 =        stop(y=-27.0703, x=-109.3987),
    )

    ORIGIN=AHU['orongo']

    parser.add_argument('--path', default='karmapi/ecmwf')
    parser.add_argument('--value', default='t2m')
    parser.add_argument('--raw', default='temperature.nc')
    parser.add_argument('--date')
    parser.add_argument(
        '--pc', action='store_true',
        help='do principal components')

    parser.add_argument('--delta', action='store_true')
    parser.add_argument('--model', action='store_true')
    parser.add_argument('--offset', type=int, default=0)

    args = parser.parse_args()

    path = Path(args.path)

    for name, ahu in AHU.items():
        print(name, ahu)

    overandout

    df = load(path / args.raw)

    stamps = df.variables['time']

    args.date = base.parse_date(args.date)

    if args.date:
        stamps = stamp_filter(stamps, args.date)

    values = df.variables[args.value]

    path = path / args.value

    if args.pc:
        pca = pcs(stamps, values, 48*35)

        pca.show_fracs(0.1)

        for x in dir(pca):
            print(x)

    elif args.delta:
        delta(stamps, values)

    elif args.model:

        model(stamps, values)
        
    else:
        images(path, stamps, values)
    
        

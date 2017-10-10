"""
Moon or moai

Electromagnetic balls of wonder dancing together.

Ahu bus stops

and the number 7 bus.

May Day Parade

Winter Solstice

Spring Tide Mays

And October blaze.
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

from collections import Queue
from math import pi

class queue(Queue):

    def __init__(self):

        super().__init__(self)

        self.value = 0.0
    
    def value(self):

        return self.value

    def tick(self):

        self.value /= pi
    
class stop:
    """ Or Ahu, a bus depot """
    self.depot = queue()

    def echo(self, depot=None):

        value = 0.0
        for item in depot:
            value += depot.value()

        self.value += value / 2
        return self.value

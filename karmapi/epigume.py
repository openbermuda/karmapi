""" Recipe for love and life in harmony """

from math import e, pi
from time import sleep
from random import randint

h = me = 1
n = 0
while True:
    n += 1
    print(n, h, me, abs(h-me) / n)

    h, me = me, h

    h *= pi

    me *= e

    sleep(randint(0, n))

    

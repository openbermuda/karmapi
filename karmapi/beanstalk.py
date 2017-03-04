""" Is this a magic seed

(2 ** 30) - (p2 * 3) == p1, p1 * 3 = x.   p1 and p2 are prime... is this a magic seed?


23000003243241 generates a TypeError complaining about comparision no
being supported betweend int and complex.

I've no ides where these imaginary numbers are coming from.

"""
import math
import random

from karmapi import pig
from karmapi.prime import isprime

def is3xprime(x):
    """ Tests if n is 3 times a prime """
    if isprime(x):
        return False

    p = int(x / 3)

    if (p * 3) != x: return False

    return isprime(p)
    

def magic_seed(x=3000657567, k=30):
    """ Returns true if x is a magic seed """


    if is3xprime(x):
        p1 = int(x / 3)

    else:
        return False
        
    yy = (2 ** k) - p1

    return is3xprime(yy)    
        

class BeanStalk:
    """ Draw a beanstalk given a magic seed """

    def __init__(self):

        self.xx = random.random()
        self.yy = random.random()

        self.x = 3000657567

        self.step = 1

    def step(self, delta=1):

        self.x += self.delta
        self.xx = random.random()
        self.yy = random.random()

    def draw(self, width, height, colour):


        self.create_text(self.xx, self.yy, fill=colour, font=pig.BIGLY_FONT,
                         text=f'{self.x}: {magic_seed(self.x)}')
        

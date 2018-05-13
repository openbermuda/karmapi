"""
Not, CPR, but Colin P Rourke.

Simulate nested spherical waves.
"""
import argparse

from karmapi import base, tpot

from random import random, randint

class Sphere:

    def __init__(self, size=None):

        size = size or 4

        grid = []
        for lat in range(size):
            grid.append([random() for x in range(size)])

        print(grid)

if __name__ == '__main__':

    ball = Sphere()
            




        

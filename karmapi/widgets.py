"""
Widgets for pig
"""

from karmapi import pig

import numpy as np
from numpy import random

import math

PI = math.pi

class Circle(pig.PlotImage):


    def compute_data(self):

        r = 50

        self.x = range(-50, 51)

        self.y = [(((r * r) - (x * x)) ** 0.5) for x in self.x]


    def plot(self):

        self.axes.hold(True)
        self.axes.plot(self.x, self.y)

        
        self.axes.plot(self.x, [-1 * y for y in self.y])


class Friday(pig.Video):


    def compute_data(self):

        #self.data = random.randint(0, 100, size=100)
        self.data = list(range(100))

    def plot(self):

        self.axes.plot(self.data)

class MapPoints(pig.PlotImage):

    def compute_data(self):

        self.df = base.load(self.path)

    def plot(self):
        """ See Maps.plot_points_on_map """

        self.df.plot(axes=self.axes)
        
        self.axes.plot(self.data)

        
class InfinitySlalom(pig.Video):

    def compute_data(self):

        #self.data = random.randint(0, 100, size=100)
        waves_start = random.randint(5, 10)
        waves_end = random.randint(32, 1024)
        self.x = np.linspace(
            0,
            random.randint(waves_start, waves_end),
            1000) * PI
        
        self.y = np.sin(self.x)

    def plot(self):

        
        self.axes.hold(random.randint(0, 1))
        self.axes.plot(self.x, self.y * -1 * random.random())
        self.axes.plot(self.x, self.y * -1 * random.random())

    

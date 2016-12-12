"""
Widgets for pig
"""

from karmapi import pig

import curio

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

    def __init__(self, parent=None):

        super().__init__(parent, facecolor='grey')

    def compute_data(self):

        #self.data = random.randint(0, 100, size=100)
        waves_start = random.randint(5, 10)
        waves_end = random.randint(32, 128)
        self.x = np.linspace(
            0,
            random.randint(waves_start, waves_end),
            512) * PI
        
        self.y = np.sin(self.x / PI) * (64 * PI)

    def plot(self):

        selector = pig.win_curio_fix()
        curio.run(self.updater(), selector=selector)

    async def updater(self):

        self.axes.hold(True)

        if random.random() < 0.02:
            self.axes.clear()

        colour = random.random()
        n = 100
        background = np.ones((n, n))

        background *= colour

        background[0, 0] = 0.0
        background[n-1, n-1] = 1.0
        
        for curve in range(random.randint(3, 12)):

            await curio.sleep(1)

            self.axes.fill(self.x, self.y * 1 * random.random(), alpha=0.3)
            self.axes.fill(self.x, self.y * -1 * random.random(), alpha=0.3)

            #self.compute_data()
            break

        
        self.axes.imshow(background, alpha=0.1, extent=(
            0, 128 * PI, -128, 128))
        

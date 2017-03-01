""" Dice Ware

Generate dice ware passwords.

Don't do it this way, use real dice, its more fun.

But use this to learn how.

"""

from karmapi import pig
from karmapi.bats import Theme, Swarm
import curio
import random
import math


class StingingBats(pig.Canvas):

    def __init__(self, parent):

        super().__init__(parent)

        self.width = self.height = 200
        self.minswarms = 20
        self.maxswarms = 50
        self.themes = []
        self.themes.append(Theme())
        self.themes.append(Theme(
            background='#0d0d0d',
            colours=['#b35900', '#804000', '#663300', '#662200', '#b36b00']))
        self.themes.append(Theme(colours=['green', 'yellow', 'red']))
        self.theme = self.themes[0]

        self.canvas.configure(bg=self.theme.background,
            width=self.width, height=self.height)

        self.create_event_map()
        self.create_swarms()

    def create_event_map(self):

        self.add_event_map('j', self.fewer)
        self.add_event_map('k', self.more)
        self.add_event_map('f', self.fast)
        self.add_event_map('s', self.slow)
        self.add_event_map('t', self.next_theme)


    async def next_theme(self):
        '''Toggles color scheme'''

        self.theme = self.themes[random.randint(0, len(self.themes) - 1)]
        self.canvas.configure(bg=self.theme.background)

    async def fewer(self):
        '''Fewer bats displayed'''

        self.minswarms = max(1, self.minswarms - 5)
        self.maxswarms = max(1, self.maxswarms - 5)
        self.create_swarms()

    async def more(self):
        '''More bats displayed'''

        self.minswarms = max(1, self.minswarms + 5)
        self.maxswarms = max(1, self.maxswarms + 5)
        self.create_swarms()

    async def fast(self):
        '''Faster bats'''

        self.sleep -= 0.05

    async def slow(self):
        '''Slower bats'''

        self.sleep += 0.05

    def create_swarms(self):

        print('new swarms')
        self.swarms = [Swarm()
                           for x in range(random.randint(self.minswarms, self.maxswarms))]

        self.rays = [SwoopingMantaRay()
                         for x in range(random.randint(self.minswarms, self.maxswarms))]


    def recalc(self, width, height):

        self.width = width
        self.height = height

        self.canvas.configure(scrollregion=(0, 0, width, height))


    async def run(self):
        self.sleep = 0.1

        while True:
            if random.random() < 0.01:
                self.create_swarms()

            self.canvas.delete('all')

            for swarm in self.swarms:
                swarm.draw(self.canvas, self.width, self.height,
                            self.theme.colours)

            for ray in self.rays:
                ray.draw(self.canvas, self.width, self.height,
                            self.theme.colours)

            await curio.sleep(self.sleep)


class SwoopingMantaRay:
    """ Throw dice, pick words """


    def __init__(self):

        self.xx = random.random()
        self.yy = random.random()

        self.clockwise = -1
        self.angle = random.random() * 360.

        self.speed = random.random() / 2
        
        self.step = 0
        self.this_step = random.randint(40, 100)


    def draw(self, canvas, width, height, colours):


        delta = random.random() * self.speed

        rangle = 2 * math.pi * self.angle / 360.
        dx = math.cos(rangle) * delta
        dy = math.sin(rangle) * delta

        self.xx += dx
        self.yy += dy

        # FIXME set angle based on direction of movement
        dangle = random.random() * 20.0
        self.angle += dangle * self.clockwise

        self.xx = min(max(self.xx, -0.1), 1.1)
        self.yy = min(max(self.yy, -0.1), 1.1)

        size = random.randint(10, 50)

        head_colour = colours[random.randint(0, len(colours) - 1)]
        tail_colour = colours[random.randint(0, len(colours) - 1)]
        

        extent = random.randint(20, 40)

        xx = self.xx * width
        yy = self.yy * height
        canvas.create_arc(xx-size, yy-size, xx+size, yy+size,
                          start=self.angle, extent=extent/2, fill=head_colour)
        canvas.create_arc(xx-size, yy-size, xx+size, yy+size,
                          start=self.angle + extent/2, extent=extent/2, fill=tail_colour)
        

        self.step += 1

        if 0 == self.step % self.this_step:
            self.clockwise *= -1

            self.this_step = random.randint(40, 100)

        # FIXME: draw tail -- sine wave angle of dangle based on dx, dy

from karmapi import pig

import curio
import random
import math

class StingingBats(pig.Canvas):

    def __init__(self, parent):

        super().__init__(parent)

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
        self.set_background(self.theme.background)

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

class Theme:

    def __init__(self, background=None, colours=None):

        if background is None:
            background = 'black'
        if colours is None:
            colours = ['red', 'magenta', 'skyblue', 'orange', 'yellow']

        self.background = background
        self.palettes =[]
        self.palettes.append(colours)
        self.colours = colours

    def add_colours(self, colours):

        self.palettes.append(colours)

    def choose_colours(self):

        return self.palettes[random.randint(0, len(self.palettes))]

class Swarm:

    def __init__(self):

        self.xx = random.random()
        self.yy = random.random()

        self.bats = [(random.random(), random.random()) for x in range(random.randint(1, 40))]

        self.scale = random.random() / 10.0

        self.xmove = random.random() / 10.0

        self.ymove = random.random() / 10.0


    def draw(self, canvas, width, height, colours):

        for x, y in self.bats:

            xx = int(width * x * self.scale) + int(width * self.xx)
            yy = int(height * y * self.scale) + int(height * self.yy)

            self.xx += (random.random() - 0.5) * self.xmove
            self.yy += (random.random() - 0.5) * self.ymove

            self.xx = min(max(self.xx, -0.1), 1.1)
            self.yy = min(max(self.yy, -0.1), 1.1)

            size = random.randint(1, 3)

            colour = colours[random.randint(0, len(colours) - 1)]

            canvas.create_oval(xx-size, yy-size, xx+size, yy+size, fill=colour)
            

class SwoopingMantaRay:


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
        
        

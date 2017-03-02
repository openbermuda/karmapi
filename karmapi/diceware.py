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

BIGLY = 'helvetica 20 bold'

class StingingBats(pig.Canvas):

    def __init__(self, parent):

        super().__init__(parent)

        self.width = self.height = 200

        self.size = 5
        self.sides = 6
        self.canvas_text = None
        
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
        self.add_event_map('r', self.roll)
        self.add_event_map('t', self.next_theme)
        self.add_event_map('u', self.up)
        self.add_event_map('d', self.down)

    async def up(self):
        """ Increase the number of dice """

        self.size += 1


    async def down(self):
        """ Decrease the number of dice """

        self.size -= 1


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

    async def roll(self):
        ''' roll the dice '''

        self.data = [random.randint(1, self.sides) for die in range(self.size)]

        total = 0
        for die in self.data:
            total += (total * self.size) + die

        self.total = total

        print(f'{self.data} {total}')

        self.canvas_text = f'{self.data}    {total}   {self.sides ** self.size}'
        

    def create_swarms(self):

        self.swarms = [Swarm()
                           for x in range(random.randint(self.minswarms, self.maxswarms))]

        self.rays = [SwoopingMantaRay()
                         for x in range(random.randint(self.minswarms, self.maxswarms))]


    def recalc(self, width, height):

        self.width = width
        self.height = height

        self.canvas.configure(scrollregion=(0, 0, width, height))


    def draw_digit(self, x, y, size, die):
        """ Draw a digit like a die """
        digits = {
            1: ((0,0,0), (0,1,0), (0,0,0)),
            2: ((1,0,0), (0,0,0), (0,0,1)),
            3: ((1,0,0), (0,1,0), (0,0,1)),
            4: ((1,0,1), (0,0,0), (1,0,1)),
            5: ((1,0,1), (0,1,0), (1,0,1)),
            6: ((1,0,1), (1,0,1), (1,0,1))}

        
        self.draw_pixel(digits[die], x, y, size, size, 10)

    def draw_pixel(self, data, x, y, width, height, size, colour=None):

        #colour = 'red'
        colour = colour or self.random_colour()
        
        for ix, row in enumerate(data):
            for jx, col in enumerate(row):

                xx = (ix * width) + x
                
                yy = (jx * height) + x

                #print(f'zzzz {xx} {yy} {size}, {colour}')
                
                if col:
                    self.canvas.create_arc(xx-size, yy-size, xx+size, yy+size,
                        start=0, extent=180, fill=colour)

    def random_colour(self):

        colours = self.theme.colours

        return colours[random.randint(0, len(colours) - 1)]


    def dice_ware_text(self):
        """ Return password for current data """

        # FIXME get a diceware list of words
        # Also, remind me to write a bit about why real dice are better
        
        return "no dice"

    def draw_dice(self):
        """ Draw the dice """

        #FIXME make the tkinter part async
        totsize = min(self.width, self.height)

        gap = totsize / (1 + self.size)

        xx = gap / 2
        yy = gap / 2

        print(self.height, self.width)
        ygap = (self.height / 3) / (self.size - 1)

        text = self.dice_ware_text()
        self.canvas.create_text(totsize - (2 * gap), yy, fill=self.random_colour(),
                                text=text, font=BIGLY)
        
        for die in self.data:
            #print(f'drawing {xx} {yy} {gap} {die}')
            self.draw_digit(xx, yy, gap * 0.4, die)

            #print(xx, yy)
            xx += gap
            yy += gap

            

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

            if self.canvas_text:
                self.canvas.create_text((self.width * 0.3, self.height * 0.9),
                                        text=self.canvas_text, fill='yellow',
                                        font=BIGLY)
                self.draw_dice()


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

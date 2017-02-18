from karmapi import pig

import curio
import random

class StingingBats(pig.Canvas):

    def __init__(self, parent):

        super().__init__(parent)

        self.width = self.height = 200
        self.canvas.configure(bg='black', width=self.width, height=self.height)

        self.create_swarms()
        
    def create_swarms(self):
        
        print('new swarms')
        self.swarms = [Swarm() for x in range(random.randint(20, 50))]


    def recalc(self, width, height):

        self.width = width
        self.height = height
        #self.canvas.configure(scrollregion=(-width//2, -height//2,
        #                                    width//2, height//2))
        self.canvas.configure(scrollregion=(0, 0, width, height))


    async def run(self):

        while True:
            if random.random() < 0.01:
                self.create_swarms()
            
            self.canvas.delete('all')

            for swarm in self.swarms:
                swarm.draw(self.canvas, self.width, self.height)
                
            await curio.sleep(0.1)


class Swarm:

    def __init__(self):

        self.xx = random.random()
        self.yy = random.random()

        self.bats = [(random.random(), random.random()) for x in range(random.randint(1, 40))]

        self.scale = random.random() / 10.0

        self.xmove = random.random() / 10.0

        self.ymove = random.random() / 10.0


    def draw(self, canvas, width, height):

        colours = ['red', 'magenta', 'skyblue', 'orange', 'yellow']

        for x, y in self.bats:

            xx = int(width * x * self.scale) + int(width * self.xx)
            yy = int(height * y * self.scale) + int(width * self.yy) 

            self.xx += (random.random() - 0.5) * self.xmove
            self.yy += (random.random() - 0.5) * self.ymove

            self.xx = min(max(self.xx, -0.1), 1.1)
            self.yy = min(max(self.yy, -0.1), 1.1)

            size = random.randint(1, 3)

            colour = colours[random.randint(0, len(colours) - 1)]

            canvas.create_oval(xx-size, yy-size, xx+size, yy+size, fill=colour)

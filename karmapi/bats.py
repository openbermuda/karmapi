from karmapi import pig

import curio
import random

class StingingBats(pig.Canvas):

    def __init__(self, parent):

        super().__init__(parent)

        self.width = self.height = 200
        self.canvas.configure(bg='black', width=self.width, height=self.height)


    def recalc(self, width, height):

        self.width = width
        self.height = height
        #self.canvas.configure(scrollregion=(-width//2, -height//2,
        #                                    width//2, height//2))
        self.canvas.configure(scrollregion=(0, 0, width, height))


    async def run(self):

        while True:

            if random.random() < 0.01:
                # random bat removal
                print('deleting bats')
                self.canvas.delete('all')
                
            self.redraw()
            await curio.sleep(0.1)

            
    def redraw(self):

        bats = [(random.random(), random.random()) for x in range(random.randint(1, 10))]

        colours = ['red', 'magenta', 'skyblue', 'orange', 'yellow']

        for x, y in bats:

            xx = int(self.width * x)
            yy = int(self.height * y)

            size = random.randint(1, 3)

            colour = colours[random.randint(0, len(colours) - 1)]

            self.canvas.create_oval(xx-size, yy-size, xx+size, yy+size, fill=colour)

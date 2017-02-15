from karmapi import pig

import curio
import random

class StingingBats(pig.Canvas):

    def __init__(self, parent):

        super().__init__(parent)

        radius = 200
        self.radius = 200
        self.canvas.configure(bg='black', width=2*radius, height=2*radius)

        self.canvas.bind("<Configure>", self.on_configure)

    def on_configure(self, event):
        self.recalc(event.width, event.height)

    def recalc(self, width, height):
        radius = min(width, height) // 2
        self.width = width
        self.height = height
        self.radius = radius
        self.canvas.configure(scrollregion=(-width//2, -height//2,
                                            width//2, height//2))



    async def run(self):

        while True:
            self.redraw()
            await curio.sleep(0.1)

            
    def redraw(self):

        bats = [(random.random(), random.random()) for x in range(random.randint(1, 10))]

        for x, y in bats:

            xx = int(self.radius * x)
            yy = int(self.radius * y)

            self.canvas.create_oval(xx-3, yy-3, xx+3, yy+3, fill='red')

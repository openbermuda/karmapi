""" Dice Ware

Generate dice ware passwords.

Don't do it this way, use real dice, its more fun.

But use this to learn how.

"""

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

""" Is this a magic seed

(2 ** 30) - (p2 * 3) == p1, p1 * 3 = x.   p1 and p2 are prime... is this a magic seed?


23000003243241 generates a TypeError complaining about comparision no
being supported betweend int and complex.

I've no ides where these imaginary numbers are coming from.

"""
import math
import random
from pathlib import Path
import time

from tkinter import PhotoImage
from PIL import Image, ImageTk

from karmapi import pig, piglet
from karmapi.prime import isprime

def is3xprime(x):
    """ Tests if n is 3 times a prime """
    if isprime(x):
        return False

    p = int(x / 3)

    if (p * 3) != x: return False

    return isprime(p)
    

def magic_seed(x=3000657567, k=30):
    """ Returns true if x is a magic seed """


    if is3xprime(x):
        p1 = int(x / 3)

    else:
        return False
        
    yy = (2 ** k) - p1

    return is3xprime(yy)    

class BeanField(pig.Canvas):

    def __init__(self, parent):

        super().__init__(parent)

        self.beanstalk = BeanStalk(1)
        self.beanstalks = []

    def draw_beanstalks(self):

        for beanstalk in self.beanstalks:
            beanstalk.draw(self.canvas, self.width, self.height, 'red')


    def prune(self):

        beans = []
        tt = time.time()
        for bean in self.beanstalks:
            if (tt - bean.create_time) < 20:
                beans.append(bean)
                
        self.beanstalks = beans
        

    async def run(self):
        self.sleep = 0.1

        while True:
            self.canvas.delete('all')

            self.beanstalk.step()
            
            if self.beanstalk.is_magic():
                self.beanstalks.append(
                    BeanStalk(self.beanstalk.x))
 
            if self.beanstalks:
                self.draw_beanstalks()

            self.prune()
            await curio.sleep(self.sleep)
    

class BeanStalk:
    """ Draw a beanstalk given a magic seed """

    def __init__(self, x=None, name=None):

        self.name = name
        image_name = Path(__file__).parent / 'tree_of_hearts.jpg'

        self.images = []
        self.image_pick = None

        self.xx = random.random()
        self.yy = random.random()

        self.x = x or 3000657567

        self.create_time = time.time()

        self.delta = 1

    def add_image(self, inage_name, scale=100):
        
        image = Image.open(image_name)

        width, height = image.size

        wscale = width / scale

        height *= wscale
        widht *= wscale
        
        image = image.resize((int(width), int(height))).convert('RGBA')

        self.images.append(image)


    def step(self, delta=1):

        self.x += self.delta

        if len(self.images) < 10:
            if self.name:
                self.add_image(name)

        if  self.images:
            self.image_pick = random.randint(1, len(self.images))

        if random.random() < 0.01:
            self.xx = random.random()
            self.yy = random.random()


    def is_magic(self):

        return magic_seed(self.x)

    def draw(self, canvas, width, height, colour):

        xx = self.xx * width
        yy = self.yy * width

        
        if self.image:

            tt = time.time()
            alpha = 255 - (10 * (tt - self.create_time))
            self.image.putalpha(int(alpha))

            self.phim = ImageTk.PhotoImage(self.image)
            canvas.create_image(xx, yy, image=self.phim)

        
        canvas.create_text(
            xx, yy + 50, fill=colour, font=pig.BIGLY_FONT,
            text=f'{self.x}')

def main():

    parser = argparse,ArgumentParser()

    parser.add_argument('--gallery', nargs='*', default=['.', '../gallery'])

    args = parser.parse_args()

    from karmapi import currie
    import curio
    
    farm = currie.PigFarm()
    
    from karmapi.mclock2 import GuidoClock
    
    farm.add(GuidoClock)
    farm.add(BeanField(galleries=args.galleries))

    curio.run(farm.run(), with_monitor=False)
    

if __name__ == '__main__':

    main()
        

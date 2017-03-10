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
import argparse

from tkinter import PhotoImage
from PIL import Image, ImageTk


import curio

from karmapi import pig, piglet
from karmapi.prime import isprime
from karmapi import currie
    

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

    def __init__(self, parent, gallery=None, name='tree'):

        super().__init__(parent)

        self.name = name
        
        if gallery:
            self.gallery = gallery

        self.beanstalk = BeanStalk(1)
        self.beanstalks = []
        self.scale = 400
        self.fade = 30
        self.images = {}

        self.add_event_map('l', self.larger)
        self.add_event_map('k', self.smaller)
        self.add_event_map('s', self.slow_fade)
        self.add_event_map('f', self.fast_fade)

    async def larger(self):
        """ Larger pictures """
        self.scale += 50

    async def smaller(self):
        """ Smaller pictures """

        self.scale -= 50
        
    async def slow_fade(self):
        """ Fade slower """

        self.fade += 5

    async def fast_fade(self):
        """ Fade faster """

        if self.fade > 5:
            self.fade -= 5

    def load_image(self, name):

        ximage = self.images.get(name)

        if ximage:
            image, scale = ximage
            if scale == self.scale:
                return image

        image = Image.open(name)

        width, height = image.size

        wscale = width / self.scale

        height /= wscale
        width /= wscale

        print(f'load {width} {height}')
        
        image = image.resize((int(width), int(height))).convert('RGBA')

        # cache image
        self.images[name] = image, self.scale

        return image


    def draw_beanstalks(self):
        """ Draw the beanstalks """
        for beanstalk in self.beanstalks:

            try:
                beanstalk.draw(self.canvas, self.width, self.height, 'red')
            except RuntimeError as error:
                print('Whoops -- run time error drawing', error)


    def prune(self):

        beans = []
        tt = time.time()
        for bean in self.beanstalks:
            if (tt - bean.create_time) < self.fade:
                beans.append(bean)
                
        self.beanstalks = beans
        

    async def run(self):
        self.sleep = 0.05
        self.set_background()
        
        while True:
            self.canvas.delete('all')

            self.beanstalk.step()
            
            if self.beanstalk.is_magic():

                name = self.find_image(self.name)
                
                image = self.load_image(name)
                
                self.beanstalks.append(
                    BeanStalk(
                        self.beanstalk.x,
                        image=image,
                        fade=self.fade))
 
            if self.beanstalks:
                self.draw_beanstalks()

            self.prune()
            await curio.sleep(self.sleep)
    

class BeanStalk:
    """ Draw a beanstalk given a magic seed """

    def __init__(self, x=None, image=None, fade=10):

        self.image = image
        self.fade = fade

        self.xx = random.random()
        self.yy = random.random()

        self.x = x or 3000657567

        self.create_time = time.time()

        self.delta = 1

    def step(self, delta=1):

        self.x += self.delta

        if random.random() < 0.01:
            self.xx = random.random()
            self.yy = random.random()


    def is_magic(self):

        return magic_seed(self.x)

    def draw(self, canvas, width, height, colour):

        xx = self.xx * width
        yy = self.yy * width

        
        canvas.create_text(
            xx, yy + 50, fill=colour, font=pig.BIGLY_FONT,
            text=f'{self.x}')

        if self.image:

            tt = time.time()
            fade = int(255 / self.fade)
            alpha = 255 - (fade * (tt - self.create_time))
            self.image.putalpha(int(alpha))

            self.phim = ImageTk.PhotoImage(self.image)
            canvas.create_image(xx, yy, image=self.phim)

        

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('--gallery', nargs='*', default=['.', '../gallery'])
    parser.add_argument(
        '--snowy', action='store_true',
        help='random cat pictures')
                            

    args = parser.parse_args()

    farm = currie.PigFarm()
    
    from karmapi.mclock2 import GuidoClock
    
    farm.add(GuidoClock)

    name = 'tree'
    if args.snowy:
        name = 'cat'
        
    farm.add(BeanField, dict(gallery=args.gallery, name=name))

    curio.run(farm.run(), with_monitor=False)
    

if __name__ == '__main__':

    main()
        

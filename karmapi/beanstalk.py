""" Is this a magic seed

(2 ** 30) - (p2 * 3) == p1, p1 * 3 = x.   p1 and p2 are prime... is this a magic seed?


23000003243241 generates a TypeError complaining about comparision no
being supported betweend int and complex.

I've no ides where these imaginary numbers are coming from.

"""
import math
import random
from pathlib import Path
from tkinter import PhotoImage
from PIL import Image
import numpy as np

from matplotlib.backends.tkagg import blit
from matplotlib import pyplot

from karmapi import pig
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
        

class BeanStalk:
    """ Draw a beanstalk given a magic seed """

    def __init__(self, x=None):

        image_name = Path(__file__).parent / 'tree_of_hearts.jpg'
        print('loading beanstalk image data')
        import time
        t = time.time()
        self.image = Image.open(image_name)
        self.image = self.image.resize((250, 190))
        print('image open')
        data = np.array(self.image.getdata())
        print('got array')
        #data = data.reshape(self.image.size + (3,))
        self.image_data = data
        self.image_data = pyplot.imread(image_name)

        t2 = time.time()
        print('image load time', t2 - t)
        
        self.xx = random.random()
        self.yy = random.random()

        self.x = x or 3000657567

        self.delta = 1
        self.phim = None

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

        
        if self.image:

            if self.phim is None:
                width, height = self.image.size
                width = height = 100
                phim = PhotoImage(master=canvas, width=width, height=height)

                bbox = np.array((
                    xx - 100, yy - 100,
                    xx + 100, yy + 100))

                data = np.array([[[int(random.random() * 255) for x in range(3)]
                                    for x in range(width)]
                                    for z in range(height)], dtype=np.uint8)

                self.image_data = data
                self.phim = phim

            canvas.create_image(xx, yy, image=self.phim)
            blit(self.phim, self.image_data)

            
            #canvas.update()

        
        canvas.create_text(
            xx, yy, fill=colour, font=pig.BIGLY_FONT,
            text=f'{self.x}')




        
def xblit(photoimage, aggimage, bbox=None, colormode=1):
    """ From matplotlib tkagg backend 

    Pick this apart to get fast images on a tkcanvas.
    """
    tk = photoimage.tk

    if bbox is not None:
        bbox_array = bbox.__array__()
    else:
        bbox_array = None
    data = np.asarray(aggimage)
    try:
        tk.call(
            "PyAggImagePhoto", photoimage,
            id(data), colormode, id(bbox_array))
    except Tk.TclError:
        try:
            try:
                _tkagg.tkinit(tk.interpaddr(), 1)
            except AttributeError:
                _tkagg.tkinit(id(tk), 0)
            tk.call("PyAggImagePhoto", photoimage,
                    id(data), colormode, id(bbox_array))
        except (ImportError, AttributeError, Tk.TclError):
            raise


if __name__ == '__main__':

    #main()
    from karmapi import currie
    import curio
    
    farm = currie.PigFarm()
    
    #farm.add(BattleShips)

    from karmapi.mclock2 import GuidoClock
    from karmapi.diceware import StingingBats
    
    farm.add(GuidoClock)
    farm.add(StingingBats)
    farm.add(BeanStalk)

    curio.run(farm.run(), with_monitor=False)
        

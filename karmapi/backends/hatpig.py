"""
Pi Gui on a Sense Hat
"""
import random

import curio

import sense_hat

import numpy as np

from . import tkpig, core

from .tkpig import Pig, AppEventLoop, Docs, cpu_count

from . import tkpig

class Help:

    def __init__(self, msg):

        msg = msg or "Help Me!"

        print(msg)
        #messagebox.showinfo(message=msg)

class Canvas(tkpig.Canvas):

    def __init__(self, parent, **kwargs):

        super().__init__(parent, **kwargs)

        self.hat = sense_hat.SenseHat()

    
    def draw(self):

        super().draw()

        # FIXME: set self.image to image data

        self.blit()

    def blit(self):
        """ Update the image on the sense hat

        Need to downsample from width x height to 8 x 8

        """
        pixels = pick_pixels(self.image)

        self.hat.set_pixels(pixels)
        
    
class PlotImage(tkpig.PlotImage):

    def __init__(self, parent, **kwargs):

        super().__init__(parent, **kwargs)

        self.hat = sense_hat.SenseHat()

    
    def draw(self):

        self.image.draw()

        self.blit()

    def blit(self):
        """ Update the image on the sense hat

        Need to downsample from width x height to 8 x 8

        """
        # FIXME - something here is slow
        dpi = self.fig.get_dpi()
        width = self.fig.get_figwidth()
        height = self.fig.get_figheight()

        print('getting string for image')
        image = self.image.tostring_rgb()

        print(width, height, len(image))

        iwidth = int(dpi * width)
        iheight = int(dpi * height)

        print('converting to lists FIXME use np')
        image = rgb_string_to_image(image, iwidth, iheight)
        print('got image')


        # normalise image
        from matplotlib.colors import Normalize
        norm = Normalize()

        image = norm(image) * 255

        pixels = pick_pixels(image)

        pixels = np.array(pixels).astype(int)
        
        for f in max, min:
            print(f(x[0] for x in pixels))
            print(f(x[1] for x in pixels))
            print(f(x[2] for x in pixels))

        for row in range(8):
            for col in range(8):
                print(pixels[(8*row) +col], end=' ')
            print()

        self.hat.set_pixels(pixels.astype(int))
        
    
def pick_pixels(image, size=8):
    """ Pick a random pixel for each on the hat """

    width, height = len(image), len(image[0])

    pwidth = int(width / size)
    pheight = int(height / size)

    pickx = random.randint(0, pwidth-1)
    picky = random.randint(0, pheight-1)

    pixels = []
    for x in range(size):
        for y in range(size):
                
                xpos = pwidth * x
                ypos = pheight * y
                
                pix = image[int(xpos + pickx)][int(ypos + picky)]
                pixels.append(pix)

    return pixels
    

def rgb_string_to_image(rgb, width, height):

    image = []
    pos = 0
    for y in range(height):
        row = []
        image.append(row)
        for x in range(width):
            
            pixel = [int(pix) for pix in rgb[pos:pos+3]]
            
            row.append(pixel)
            pos += 3

    return image
    

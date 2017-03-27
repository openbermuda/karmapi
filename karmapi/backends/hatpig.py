"""
Pi Gui on a Sense Hat
"""

import curio

import sense_hat

from . import tkpig, core

from .tkpig import Pig, AppEventLoop, Docs, cpu_count

from . import tkpig

class Help:

    def __init__(self, msg):

        msg = msg or "Help Me!"

        print(msg)
        #messagebox.showinfo(message=msg)

class Canvas(tkpig.Pig):

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
        pixels = self.pick_pixels()

        self.hat.set_pixels(pixels)
        
    
    def pick_pixels(self):
        """ Pick a random pixel for each on the hat """
        width = self.width / 8
        height = self.height / 8
        
        pickx = random.randint(0, width-1)
        picky = random.randint(0, height-1)

        pixels = []
        for x in range(8):
            for y in range(8):
                
                xpos = self.width * x
                ypos = self.height * y
                

                pix = self.image.getpixel((xpos + pickx, ypos + picky))
                pixels.append(pix)

        return pixels


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
        pixels = self.pick_pixels()

        self.hat.set_pixels(pixels)
        
    
    def pick_pixels(self):
        """ Pick a random pixel for each on the hat """
        width = self.width / 8
        height = self.height / 8
        
        pickx = random.randint(0, width-1)
        picky = random.randint(0, height-1)

        image = self.image.print_to_buffer()

        pixels = []
        for x in range(8):
            for y in range(8):
                
                xpos = self.width * x
                ypos = self.height * y
                

                pix = image[xpos + pickx, ypos + picky]
                pixels.append(pix)

        return pixels
    

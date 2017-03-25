"""
Pi Gui on a Sense Hat
"""

import curio

from . import tkpig

from tkpig import Pig, AppEventLoop



class Help:

    def __init__(self, msg):

        msg = msg or "Help Me!"

        print(msg)
        #messagebox.showinfo(message=msg)

class Canvas(tkpig.Canvas):

    
    def __init__(self, parent):

        super().__init__(parent, **kwargs)

        self.width = 400
        self.height = 400

    
    def draw(self):

        super().draw()

        self.blit()

    def blit(self):
        """ Update the image on the sense hat

        Need to downsample from width x height to 8 x 8

        """
        size = self.radius // 4

        pixels = self.pick_pixels()

        self.hat.set_pixels(pixels)
        
    
    def pick_pixels(self):
        """ Pick a random pixel for each on the hat """
        pickx = random.randint(0, xx-1)
        picky = random.randint(0, xx-1)

        pixels = []
        for x in range(8):
            for y in range(8):
                
                xpos = self.width * x
                ypos = self.height * y
                

                pix = self.image.getpixel((xpos + pickx, ypos + picky))
                pixels.append(pix)

        return pixels

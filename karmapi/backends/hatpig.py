"""
Pi Gui on a Sense Hat
"""
import random

import curio

import sense_hat

import numpy as np

from . import tkpig, core

from .tkpig import Pig, Docs, cpu_count

from . import tkpig

class Help(tkpig.Help):

    def __init__(self, msg):

        msg = msg or "Help Me!"

        super().__init__(msg)

        print(msg)
        

class Canvas(tkpig.Canvas):

    def __init__(self, parent, **kwargs):

        super().__init__(parent, **kwargs)

        self.hat = sense_hat.SenseHat()

    
    def draw(self):

        super().draw()


class PillBox(tkpig.PillBox):

    def get_pixels(self, size=8):

        width = self.width
        height = self.height

        selection = pixel_selector(width, height, size=size)

        image = self.image.getdata()
        
        pixels = []
        for choice in selection:
            
            pixel = image[choice]

            pixels.append(pixel[:3])
        
        pixels = np.array(pixels).astype(int)

        return pixels
    
class PlotImage(tkpig.PlotImage):

    def __init__(self, parent, **kwargs):

        super().__init__(parent, **kwargs)

    
    def draw(self):

        self.image.draw()

    def get_pixels(self, size=8):
        """ Update the image on the sense hat

        Need to downsample from width x height to 8 x 8

        FIXME - separate the grabbing of the image from
                the bliting to the hat.

                Move the pixel selecting and write to the
                hat to the event loop.

                Have that monitor current for an image to
                show.

                Control blit speed with HatStick.
        """
        # FIXME - something here is slow
        dpi = self.fig.get_dpi()
        width = self.fig.get_figwidth()
        height = self.fig.get_figheight()

        image = self.image.tostring_rgb()

        iwidth = int(dpi * width)
        iheight = int(dpi * height)

        selection = pixel_selector(iwidth, iheight, size=8)

        pixels = []
        for choice in selection:
            
            pixel = string_to_rgb(image[3*choice:3*(choice+1)])

            pixels.append(pixel)
        
        pixels = np.array(pixels).astype(int)

        return pixels
        
 
    
def pixel_selector(width, height, size=8):
    """ Generate list of pixel positions to select """

    pwidth = int(width / size)
    pheight = int(height / size)

    pickx = random.randint(0, pwidth-1)
    picky = random.randint(0, pheight-1)

    pixels = []
    for x in range(size):
        for y in range(size):
                
                xpos = pwidth * x
                ypos = pheight * y

                # FIXME 50-50 chance this is transposing the image
                # in some way
                pixels.append(((xpos + pickx) * width) + (ypos + picky))
                

    return pixels

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
    
def string_to_rgb(pixel):

    return [int(pix) for pix in pixel[:3]]


class AppEventLoop(tkpig.AppEventLoop):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.hat = sense_hat.SenseHat()

        # stick technically not a display.. peripheral?
        self.displays = [self.hatblit(), self.stick()]
    
 
    async def hatblit(self):
        """ blit current widget to hat if possible """
        while True:
            current = self.farm.current

            if current:
                get_pixels = getattr(current, 'get_pixels', None)

                if get_pixels:

                    try:
                        pixels = get_pixels()

                        self.hat.set_pixels(pixels)
                    except:
                        pass

            await curio.sleep(0.01)
                
        
    async def stick(self):
        """ Turn SenseStick events into keyboard events """

        stick = sense_hat.stick.SenseStick()

        while True:
            for event in stick.get_events():
                await self.process_stick(event)

            # FIXME make stick.wait_for_events a co-routine?
            await curio.sleep(0.05)

    async def process_stick(self, event):
        """ Process a stick event """
        print(event)
        events = dict(
            left='p',
            right='n',
            middle='R',
            down='b',
            up='v')
        
        action = event.action
        direction = event.direction
        print(action, direction)
        if action == 'released':
            await self.farm.process_event(events.get(direction))
        

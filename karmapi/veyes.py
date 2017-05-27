"""
Eyes for pies.
"""

from picamera import PiCamera
import time
import curio

from fractions import Fraction


async def long_exposure(path,
                  length=6,
                  framerate=6,
                  resolution=(1280, 720),
                  iso=800,
                  sleep=60):
    """ Take a long exposure shot


    path: where to save the image
    length: exposure length in seconds
    framerate: number of frames per second
    resolution: resolution for image
    """
    # Set a framerate of 1/6fps, then set shutter
    # speed to 6s and ISO to 800
    camera = PiCamera(resolution=resolution, framerate=Fraction(1, framerate))
    camera.shutter_speed = length * 1000000
    camera.iso = 800
    # Give the camera a good long time to set gains and
    # measure AWB (you may wish to use fixed AWB instead)
    curio.sleep(sleep)

    camera.exposure_mode = 'off'
    # Finally, capture an image with a 6s exposure. Due
    # to mode switching on the still port, this will take
    # longer than 6 seconds
    camera.capture(path)

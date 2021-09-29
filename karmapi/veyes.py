"""
Eyes for pies.
"""
import argparse
import datetime
from pathlib import Path
import random

from io import BytesIO

from picamera import PiCamera
import time
import curio

from PIL import Image


from fractions import Fraction


def long_exposure(length=6,
                  framerate=6,
                  resolution=(1280, 720),
                  iso=800):
    """ Return camera configured for a long exposure shot

    length: exposure length in seconds
    framerate: number of frames per second
    resolution: resolution for image
    iso: iso setting for camera
    """
    # Set a framerate of 1/6fps, then set shutter
    # speed to 6s and ISO to 800
    camera = PiCamera(resolution=resolution, framerate=Fraction(1, framerate))
    camera.shutter_speed = length * 1000000
    camera.iso = 800

    camera.exposure_mode = 'off'

    # return a camera object
    return camera

def random_picture(cam):

    length = random.random() * 6

    cam.framerate = 1.0 / length
    cam.shutter_speed = int(length * 1000000)
    cam.iso - random.random() * 800

    cam.exposure_mode = 'off'

    return cam
    

def as_pil(camera):
    """ Capture an image and return as PIL.Image """
    # Create the in-memory stream
    stream = BytesIO()
    camera.capture(stream, format='rgb')

    # "Rewind" the stream to the beginning so we can read its content
    stream.seek(0)
    image = Image.open(stream)

    return image


async def capture(args):

    if args.long:
        camera = long_exposure()
    else:
        camera = PiCamera()

    camera.start_preview()
    await curio.sleep(2)

    last = None
    while True:

        now = datetime.datetime.now()
        path = Path(f'{args.path}/{now.year}/{now.month}/{now.day}')
        path.mkdir(exist_ok=True, parents=True)
        path = path / f'{now.hour:02}{now.minute:02}{now.second:02}.jpg'

        print(path)
        camera.capture(str(path))
        #image = as_pil(camera)
        await curio.sleep(args.sleep)

        if args.dedupe:
            # Compare image to last and save if it is different enough
            pass

        # save the image
        #image.save(path)

        if args.random:
            camera = random_picture(camera)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--sleep', type=float, default=60)
    parser.add_argument('path', nargs='?', default='.')
    parser.add_argument('--long', action='store_true')
    parser.add_argument('--random', action='store_true')
    parser.add_argument('--dedupe', action='store_true')

    args = parser.parse_args()

    curio.run(capture(args))


if __name__ == '__main__':

    main()

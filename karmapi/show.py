"""
Show images.
"""
from IPython import display

import pandas
from PIL import Image

from matplotlib import pyplot

from karmapi import base, heart


def show(path):
    """ Show image for path """
    path = str(path)
    #if path.endswith('.gif'):
    #    return hshow(path)
    
    return Image.open(path)

def hshow(path):
    """ Show image for path using HTML 
    
    For some reason, IPython.display.Image does not do GIFs.

    So we embed it in html instead.
    """
    return display.HTML('<img src="{}">'.format(path))


def movie(images, path=None, **kwargs):
    """ Create a movie for images """
    import imageio
    if path is None:
        path = imageio.RETURN_BYTES
        
    return imageio.mimwrite(path, images, format='GIF', **kwargs)


def load(path):

    return Image.open(str(path))

def save(path, image):

    im = Image.fromarray(image)
    im.save(str(path))

def sono(so, offset=1, end=None, **kwargs):
    """ Show an sonogram image """
    
    so = pandas.np.array(so)

    n = so.shape[1]

    if end is None:
        end = n / 2
    
    pyplot.title('offset: {} end: {} n: {}'.format(offset, end, n))

    pyplot.imshow(so[:, offset:int(end)].T.real, aspect='auto',
                  **kwargs)


def sono2(so, offset=1, end=None, **kwargs):
    """ Show an sonogram image """
    
    so = pandas.np.array(so)

    n = so.shape[1]

    if end is None:
        end = n / 2

    pyplot.figure(figsize=(12, 4))
    pyplot.subplot(1, 2, 1)
    pyplot.title('offset: {} end: {} n: {}'.format(offset, end, n))

    pyplot.imshow(so[:, offset:int(end)].T.real, aspect='auto',
                  **kwargs)
    
    pyplot.subplot(1, 2, 2)

    pyplot.imshow(so[:, offset:int(end)].T.imag, aspect='auto',
                  **kwargs)

def wide():
    pyplot.figure(figsize=(12,4))
    

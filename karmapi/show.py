"""
Show images.
"""
from IPython.display import HTML, Image
import imageio

from karmapi import base, heart


def show(path):
    """ Show image for path """
    if path.endswith('.gif'):
        return hshow(path)
    
    return Image(data=load(path))

def hshow(path):
    """ Show image for path using HTML 
    
    For some reason, IPython.display.Image does not do GIFs.

    So we embed it in html instead.
    """
    return HTML('<img src="{}">'.format(path))


def movie(images, path=None, **kwargs):
    """ Create a movie for images """
    if path is None:
        path = imageio.RETURN_BYTES
        
    return imageio.mimwrite(path, images, format='GIF', **kwargs)


def load(path):

    return imageio.imread(path)


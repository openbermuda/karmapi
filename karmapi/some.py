"""
Something from nothing.

Extract pieces of things.

For now, filter data by time, aggregate and difference.
"""

from karmapi import base, sense


def zoom(path):

    df = base.load(path)

    meta = base.meta(path)

    # figure out how to shrink it and where to put it
    pass


def image_zoom(path):
    """ Create sub folders of path with 

    meta data giving lists of images to create.
    """

    
    
    df = base.load(path)

    meta = base.meta(path)


    print(meta)

    print(df.describe())
    

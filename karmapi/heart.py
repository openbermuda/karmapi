""" Karma Pi heart

Getting Stuff
-------------

get(key): get thing for key

meta(key):  get meta data for key

Building Stuff
--------------

build(key):  build data at key


Pears
-----

clones(key)  look for clones of key

"""
import json
import datetime
from pathlib import Path

import pandas

from karmapi import base, checksum, pear

def get(key):
    """ Get data for a path """

    return base.load(key)


def meta(key):

    return base.get_all_meta_data(key)


def build(key):
    """  build key

    or:
        pick a pear
           ask pear to help
    """
    return return base.build(key)

def save(key, data):
    """ Save dataframe df at path.

    For now, save as csv.

    FIXME: include meta data for format, or use file extension.
    """
    base.save(key, data)


    
def _save_meta(key, meta):
    """ Save meta data at path 

    don't need this save will take care of it
    """
    raise NotImplemented
    



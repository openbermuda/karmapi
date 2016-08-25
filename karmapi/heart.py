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

from karmapi import base, checksum

def get(key=None, meta=None):
    """ Get data for a key or meta """

    if key is None:
        key = checksum.check(str(meta))

    try:
        data = base.load(key)
    except Exception as e:
        # try a pear - for now just let it rise
        raise e
    
    return data


def meta(key=None, path=None):

    if key is None:
        key = get(key)

    return base.get_all_meta_data(key)


def build(key):
    """  build key

    or:
        pick a pear
           ask pear to help
    """
    return base.build(key)

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
    



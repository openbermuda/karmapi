"""
Flash
=====

Maybe Flash Gordon.

Make things faster.
"""
from karmapi import base

def save_hdf(path, df):
    """ Save a dataframe as hdf """

    df.to_hdf(path, 'data', mode='w')


def meta(path, data):
    """ Update meta data at path with new data """
    m = base.meta(path)

    m.update(data)

    base.save_meta(path, m)

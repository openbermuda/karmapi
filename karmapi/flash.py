"""
Flash
=====

Maybe Flash Gordon.

Make things faster.
"""

def save_hdf(path, df):
    """ Save a dataframe as hdf """

    df.to_hdf(str(path), 'data', mode='w')


def meta():
    """ Return meta data describing formats 

    The idea here is to set meta data for folders and
    then magically have the data stored in hdf format
    instead of the default csv.

    New writes will work fine, but old files will need converting.

    
    """

    return dict(format='hdf')
    

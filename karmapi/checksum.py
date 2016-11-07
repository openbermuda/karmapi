"""Checksum files in the system.

This code creates checksums on files in the karmapi system.

For each file it calculates the checksum.

Optionally checks existing checksums and stores the result
in meta data.

Reports on files whose checksum has changed since last time.

Creates dataframe with: checksum, path

Also creates meta.json with a timestamp and the path that was
proecessed.

"""
import argparse
import datetime
from pathlib import Path

import hashlib

import pandas

from karmapi import base

BLOCKSIZE = 1024 * 1024 * 10

CHECKS = None

CACHE = {}

BASE = 'checksums'

def blocks(infile):

    buffer = infile.read(BLOCKSIZE)
    while (len(buffer)):
        yield buffer

        buffer = infile.read(BLOCKSIZE)

def checksum(path):
    """ Create checksum for path """
    with path.open('rb') as infile:

        hash = hashlib.md5()
        for buffer in blocks(infile):
            hash.update(buffer)

    return hash

def checksums(paths):

    results = []

    for path in paths:
        if path.is_dir():
            continue
        check = checksum(path)

        results.append([path.as_posix(), check.hexdigest()])

    df = pandas.DataFrame(results, columns=['path', 'checksum'])
                          
    return df


def changes(checka, checkb):
    """ Given two sets of dataframes report changes """

    # get stuff in both frames
    both = pandas.merge(checka, checkb, on='path')

    changes = both[both.checksum_x != both.checksum_y]

    return changes

def dupes(checks):
    """ Look for duplicate checksums """
    counts = checks.groupby('checksum').size()

    dupes = set(counts[counts > 1].index.values)

    return checks[checks.checksum.isin(dupes)]

def load_checksums(path=None):

    global CHECKS
    if path is None:
        path = Path(BASE)

    path = Path(path)
    if path.is_dir():

        path = path / 'checksums'

    # cache checksums to save repeated loading
    if path in CACHE:
        CHECKS = CACHE[path]

    CHECKS = base.load(path)
    
    CACHE[path] = CHECKS

def checksum_to_path(check):
    """ Return first path matching checksum """

    rows = checksum_to_paths(check)

    if len(rows) >= 1:
        return rows.iloc[0].path
        
def checksum_to_paths(check):
    """ Return all paths matching check """
    
    if CHECKS is None:
        load_checksums()

    rows = CHECKS[CHECKS.checksum == check]

    return rows

def path_to_checksum(path):
    """ Return checksum for path

    This does not calculate the checksum, rather
    it looks up path in CHECKS.

    To calculate a checksum, see checksum(path)
    """

    if CHECKS is None:
        load_checksums()

    rows = CHECKS[CHECKS.path == path]

    if len(rows) >= 1:
        return rows.iloc[0].checksum

def path_to_checksums(path):
    """ Return checksums for path

    It looks for any paths in checksums that match path.
    """

    if CHECKS is None:
        load_checksums()

    rows = CHECKS[CHECKS.path.str.contains(str(path))]

    return rows


def load(checksum):
    """ Loads the thing with checksum """
    # load the checksums
    if CHECKS is None:
        load_checksums()

    path = checksum_to_path(checksum)

    return base.load(path)

def mirror(paths, pear):
    """ Use pear to mirror paths

    :paths:  the paths to mirror

    :pear:  a peer, see the pear module
    """

    # read the checksums for folder
    for path in paths:
        pear.mirror(path)


def get_parser():

    
    parser = argparse.ArgumentParser()

    parser.add_argument('path', nargs='+', default=['.'])
    parser.add_argument('--checksums', default='checksums')
    parser.add_argument('--glob', default='**/*')

    return parser


def main(args=None):

    args = get_parser().parse_args(args)

    glob = args.glob
    if glob == True:
        glob = '**/*'
    
    for apath in args.path:
        df = checksums(Path(apath).glob(glob))

        cpath = Path(args.checksums) / apath / 'checksums'
        cpath.parent.mkdir(exist_ok=True, parents=True)
        base.save(cpath, df)

        # save meta data
        timestamp = datetime.datetime.now()
        meta = dict(path=apath, timestamp=timestamp.isoformat())
        base.save_meta(cpath.parent, meta)


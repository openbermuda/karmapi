""" Checksum files in the system.

This code creates checksums on files in the karmapi system.

For each file it calculates the checksum.

Optionally checks existing checksums and stores the result
in meta data.

Reports on files whose checksum has changed since last time.

Creates dataframe with: checksum, path and date.

"""
import argparse
import datetime
from pathlib import Path

import hashlib

import pandas

from karmapi import base

BLOCKSIZE = 1024 * 1024 * 10

CHECKS = None

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
        path = Path(BASE) / 'checksums'

    CHECKS = base.load(path)

def checksum_to_path(check):

    if CHECKS is None:
        load_checksums()

    rows = CHECKS[CHECKS.checksum == check]

    if len(rows) >= 1:
        return rows.iloc[0].path
        
    
def load(checksum):
    """ Loads the thing with checksum """
    # load the checksums
    if CHECKS is None:
        load_checksums()

    path = CHECKS.get(checksum)

    return base.load(path)


def get_parser():

    
    parser = argparse.ArgumentParser()

    parser.add_argument('path', nargs='+', default=['.'])
    parser.add_argument('--checksums', default='checksums')
    parser.add_argument('--glob', default='**/*')

    return parser


def main(args):

    glob = args.glob
    if glob == True:
        glob = '**/*'
    
    for apath in args.path:
        foo = Path(apath).glob(glob)
        df = checksums(Path(apath).glob(glob))

        cpath = Path(args.checksums) / apath / 'checksums'
        cpath.parent.mkdir(exist_ok=True, parents=True)
        base.save(cpath, df)

        # save meta data
        timestamp = datetime.datetime.now()
        meta = dict(path=apath, timestamp=timestamp)
        base.save_meta(cpath.parent, meta)

if __name__ == '__main__':

    parser = get_parser()
    args = parser.parse_args()

    main(args)

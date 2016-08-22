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
    timestamp = datetime.datetime.now()

    print('checksums', paths)

    for path in paths:
        if path.is_dir():
            continue
        check = checksum(path)

        results.append([path.as_posix(), check.hexdigest(), timestamp])

    df = pandas.DataFrame(results, columns=['path', 'checksum', 'time'])
                          
    return df


def get_parser():

    
    parser = argparse.ArgumentParser()

    parser.add_argument('path', nargs='+', default=['.'])
    parser.add_argument('--checksums', default='checksums')
    parser.add_argument('--glob', default='**/*')

    return parser


def main(args=None):

    parser = get_parser()
    args = parser.parse_args(args)

    print(args.path)

    for apath in args.path:
        foo = Path(apath).glob(args.glob)
        df = checksums(Path(apath).glob(args.glob))

        cpath = Path(args.checksums) / apath / 'checksums'
        cpath.parent.mkdir(exist_ok=True, parents=True)
        base.save(cpath, df)

if __name__ == '__main__':

    main()

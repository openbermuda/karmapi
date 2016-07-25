"""Fix up readings 

Each time the monitor starts it write out the fields, but these come
from a dictionary, so the order varies.

For now, split into separate files
"""
import sys
import argparse
from pathlib import Path

def get_parser():

    parser = argparse.ArgumentParser()

    parser.add_argument('--infile')
    parser.add_argument('--folder', default='.')

    return parser

def main(args=None):

    args = get_parser().parse_args(args)

    count = 0

    if args.infile:
        infile = open(args.infile)
    else:
        infile = sys.stdin

    base = Path(args.folder)

    outfile = None
    for row in infile:
        if 'a' in row:
            if outfile: outfile.close()
            count += 1
            
            outfile = (base / 'readings{}.csv'.format(count)).open('w')

        outfile.write(row)


            
            
        

if __name__ == '__main__':

    main()

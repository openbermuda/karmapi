
"""
Noddy
=====

Something playful.

A place to try something, see what happens.

Keep it short, go back in time.

"""

import sys

import argparse

def play(infile):

    print('infile:', infile)

if __name__ == '__main__':

    print(sys.argv)

    parser = argparse.ArgumentParser()
    parser.add_argument('--file')
    parser.add_argument('--thresh', type=float, default=10.0)

    
    args = parser.parse_args()

    print(args)


    if args.thresh > 10:

        print('bigly')

    elif args.thresh < 5:

        print('fake')

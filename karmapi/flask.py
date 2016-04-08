"""
Run a klein built flask app
"""
# configuration
import conf

import sys
import argparse

from karmapi import base

import json

from flask import Flask, request
from flask.ext.restplus import Resource, Api

app = Flask(__name__)
api = Api(app)


def get_parser():

    parser = argparse.ArgumentParser()

    parser.add_argument('--run', action='store_true')
    parser.add_argument('--meta',
                        type=argparse.FileType('r'),
                        nargs='?', default=sys.stdin)

    return parser

def main(args):

    if args.run:
        app.run(debug=False)

if __name__ == '__main__':

    parser = get_parser()
    args = parser.parse_args()

    main(args)


    

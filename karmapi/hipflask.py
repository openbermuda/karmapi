"""
Run a klein built flask app
"""
# configuration
#import conf
import argparse

from flask import Flask

from karmapi.apis import api
from karmapi.base import config

app = Flask(__name__)
api.init_app(app)

def get_parser():

    parser = argparse.ArgumentParser()

    parser.add_argument('--no-debug', action='store_true',
                        default=False)
    parser.add_argument('--config')
    parser.add_argument('--host')

    return parser

def main(args):

    if args.config:
        config(args.config)
        
    app.run(debug=not args.no_debug, host=args.host)

if __name__ == '__main__':

    parser = get_parser()
    args = parser.parse_args()

    main(args)


    

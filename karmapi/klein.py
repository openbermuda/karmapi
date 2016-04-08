""" 
Try and build flask api from a karma pi module

The Klein Bottle got its name from a mathematician who knew a bit
about topology.

It is a strange flask, or bottle, that is twisted in such a way that
it actually has no inside.

The idea here is to create a Flask interface to karma pi data.

There are not many calls:

get(path)::

   Get whatever is at path

     - returns whatever is at path

     - 404 if there is nothing there

     - ??? and meta data for item, if it can be created
     
     
post(path)::

   Create what should be at path

If you want meta data, then just ask for <path>/meta.json

Problem
=======

So this is super easy to do with Flask-restplus.  And you get the api
documented with swagger.

The problem is that what gets returned from different paths is
different.  And what those paths actually mean is anybody's guess.

In Karma Pi land we have a python module that deals with the building
for any path.  

So for any path we just have something like::

   { path = "foo/<lon:float>/<lat:float>/tmax",
     karma = karma.weather,
     model = karma.models.lat_long_grid,
     start = date(1979, 1, 1),
     end   = date(2015, 1, 1),
     lats = [latitudes()],
     lons = [longitudes()],
   }
     
Here we want to add routes for all of these to a Flask app.

This bit is simple, since we can just add lots of routes to the Flask
app all pointing to the same get and post.

There are many ways to get the docs for all these routes. 

The model associated with each path is intended to be some sort of
model for the data returned.  

The flask_restful models work well with swagger.

So the thought is to just generate some code to build all these
endpoints.

Turning the flask inside out.

"""
import sys
import argparse

from karmapi import base

import json

from flask import Flask, request
from flask.ext.restplus import Resource, Api

GET_RESOURCE_TEMPLATE =  '''

@api.route('{path}')
class {name}(Resource):
    """ {doc} """

    @api.doc("{doc}")
    @api.marshal_with({model})
    def get(self, **kwargs):
        """{doc}"""
        parms = base.Parms(kwargs)
        function = base.get_item('{karma}')

        return function(parms)
'''

PUT_RESOURCE_TEMPLATE =  '''
    @api.doc("{post_doc}")
    @api.marshal_with({model})
    def post(self, {post_args}):
        """{post_doc}"""
        return {post_function({post_args})}
'''

def get_parser():

    parser = argparse.ArgumentParser()

    parser.add_argument('--meta',
                        type=argparse.FileType('r'),
                        nargs='?', default=sys.stdin)

    return parser


def build(parms, template):

    result = ""

    #print(parms.karma)
    function = base.get_item(parms.karma)
    parms.doc = function.__doc__
    #print(function.__doc__)

    return template.format(**parms.__dict__)
        

def main():

    parser = get_parser()
    args = parser.parse_args()

    # read meta data
    meta = json.loads(args.meta.read())

    for template, items in [
        [GET_RESOURCE_TEMPLATE,
         list(meta.get('gets', {}).items())],
        [GET_RESOURCE_TEMPLATE,
         list(meta.get('builds', {}).items())]]:
        
    
        for key, value in items:

            parms = base.Parms(value)

            parms.name = key
            # build the resource, then evaluate it
            code = build(parms, GET_RESOURCE_TEMPLATE)

            print(code)


if __name__ == '__main__':


    main()


    

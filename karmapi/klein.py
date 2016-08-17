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

HEADER = """
from karmapi import base

from flask import request
from flask_restplus import Namespace, Resource, fields

api = Namespace("{name}", description="{minidoc}")
"""

MODEL_TEMPLATE = '''
from {model_module} import {model}
{model} = api.model("{model}", {model})
'''

RESOURCE_TEMPLATE =  '''
@api.route('/{path}')
class {name}(Resource):
    """ {doc} """

'''

GET_RESOURCE_TEMPLATE =  '''

    @api.doc("{name}")
    @api.marshal_with({model}, as_list={as_list})
    def get(self, **kwargs):
        """ {doc} """
        path = request.url[len(request.url_root):]
        return base.get(path)
'''

PUT_RESOURCE_TEMPLATE =  '''

    @api.doc("{name}")
    @api.marshal_with({model}, as_list={as_list})
    def post(self, **kwargs):
        """{doc}"""
        path = request.url[len(request.url_root):]
        return base.build(parms)
'''

METHOD_TEMPLATES = dict(
    get=GET_RESOURCE_TEMPLATE,
    put=PUT_RESOURCE_TEMPLATE)

def get_parser():

    parser = argparse.ArgumentParser()

    parser.add_argument('--meta',
                        type=argparse.FileType('r'),
                        nargs='?', default=sys.stdin)
    parser.add_argument('--outfile',
                        type=argparse.FileType('w'),
                        nargs='?', default=sys.stdout)
    parser.add_argument('--nobuild', action='store_true',
                        help="do not include builds in api")

    parser.add_argument('--name')
                        

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
    outfile = args.outfile
    
    # do the header
    minidoc = "api for {}".format(args.name)
    print(HEADER.format(name=args.name,
                        minidoc=minidoc), file=outfile)

    # Join the gets and builds
    resources = dict()
    gets = list(meta.get('gets', {}).items())
    for name, value in gets:
        key = value['path']
        value['name'] = name
        resources[key] = dict(get=value)

    puts = list(meta.get('builds', {}).items())

    # Don't include builds if --nobuild flag was passed
    if args.nobuild:
        puts = []
        
    for name, value in puts:
        key = value['path']
        value['name'] = name
        if key in resources:
            resources[key]['put'] = value
        else:
            resources[key] = dict(put=value)

    for path, resource in sorted(resources.items()):
        print(path)
        print(resource.keys())
        # do models
        method_code = []
        for method in ['get', 'put']:
            item = resource.get(method)
            
            if not item: continue
                
            # output model
            parms = base.Parms(item)
            print(item.keys())

            if 'as_list' not in item:
                parms.as_list = False

            model_path = parms.model.split('.')
            parms.model = model_path[-1]
            parms.model_module = '.'.join(model_path[:-1])

            print(MODEL_TEMPLATE.format(**parms.__dict__),
                  file=outfile)

            method_code.append(build(parms, METHOD_TEMPLATES[method]))


        print(RESOURCE_TEMPLATE.format(
            **parms.__dict__), file=outfile)
            
        # print out the code for the methods
        for code in method_code:
            print(code, file=args.outfile)
            


if __name__ == '__main__':


    main()


    

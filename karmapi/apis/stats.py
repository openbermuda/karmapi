""" Karmapi base web api
"""
from pathlib import Path

from karmapi import base

from flask import request, make_response
from flask_restplus import Namespace, Resource, fields

api = Namespace("stats", description="karmapi stats api")


formats = dict(
    csv=dict(
        method='to_csv',
        content_type='text/csv',),

    default=dict(
        method='to_string',
        content_type='text/plain',),

    html=dict(
        method='to_html',
        content_type='text/html',),
    )
        

@api.route('/', defaults={'path': ''})
@api.route('/<path:path>')
class Stats(Resource):

    @api.doc('load data at path')
    def get(self, path):
        """ Get stats for object at path """
        ppath = Path(path)

        # see if path has a suffix
        suffix = ppath.suffix
        
        df = base.load(ppath.parent / ppath.stem)

        # turn into stats -- just call describe
        df = df.describe()

        form = formats.get(suffix[1:], formats['default'])

        result = getattr(df, form['method'])()
        ctype = form['content_type']
        
        response = make_response(result)

        response.headers["content-type"] = ctype

        return response

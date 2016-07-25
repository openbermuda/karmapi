""" Karmapi base web api
"""
from pathlib import Path

from karmapi import base

from flask import request, make_response
from flask_restplus import Namespace, Resource, fields

api = Namespace("base", description="Base karmapi api")

txt = """
hello world

hello universe
"""

@api.route('/', defaults={'path': ''})
@api.route('/<path:path>')
class Load(Resource):

    @api.doc('load data at path')
    def get(self, path):
        """ Get object at path as text """
        ppath = Path(path)

        # see if path has a suffix
        suffix = ppath.suffix
        
        df = base.load(ppath.parent / ppath.stem)

        if suffix == '.csv':
            result = df.to_csv()
            ctype = "text/csv"
        else:
            result = df.to_string()
            ctype = "text/plain"
        
        response = make_response(result)

        response.headers["content-type"] = ctype

        return response

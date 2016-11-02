""" Karmapi base web api
"""
from pathlib import Path
from io import BytesIO

import pandas

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

        if ppath.exists():
            df = base.load(ppath)
        else:
            df = base.load(ppath.parent / ppath.stem)

        if suffix == '.csv':
            result = df.to_csv()
            ctype = "text/csv"
        elif suffix == '.json':
            result = df.to_json(orient='records')
            ctype = "application/json"
        elif suffix == '.gif':
            result = df
            ctype = "image/gif"
        elif suffix == '.png':
            result = df
            ctype = "image/png"
        elif suffix == '.xlsx':
            out = BytesIO()
            ew = pandas.ExcelWriter(out)
            df.to_excel(ew)
            ew.save()
            result = out.getvalue()
            ctype = 'application/vnd.ms-excel; charset=utf-16'
        else:
            result = df.to_string()
            ctype = "text/plain"
        
        response = make_response(result)

        response.headers["content-type"] = ctype

        return response

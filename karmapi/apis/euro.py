
from karmapi import base

from flask import request
from flask_restplus import Namespace, Resource, fields

api = Namespace("euro", description="api for euro")


from karmapi.models.lists import Array
Array = api.model("Array", Array)


@api.route('/space/<field>')
class space(Resource):
    """  Extract all the data for all latitudes.

    This then allows us to get the data for any lat/lat
    quickly
     """




    @api.doc("space")
    @api.marshal_with(Array)
    def post(self, **kwargs):
        """ Extract all the data for all latitudes.

    This then allows us to get the data for any lat/lat
    quickly
    """
        path = request.url.strip(request.url_root)
        return base.build(parms)


from karmapi.models.lists import Array
Array = api.model("Array", Array)


@api.route('/space/<float:lat>/<field>')
class lon(Resource):
    """  Extract all the data for a given latitude.

    This then allows us to get the data for any lat/lon
    quickly.

    Alternatively, use build_space and do everythng in one.
     """




    @api.doc("lon")
    @api.marshal_with(Array)
    def post(self, **kwargs):
        """ Extract all the data for a given latitude.

    This then allows us to get the data for any lat/lon
    quickly.

    Alternatively, use build_space and do everythng in one.
    """
        path = request.url.strip(request.url_root)
        return base.build(parms)


from karmapi.meta.weather import AllFields
AllFields = api.model("AllFields", AllFields)


@api.route('/space/<float:lat>/<float:lon>')
class all_latlon(Resource):
    """  Get all fields for a specific lat/lon  """




    @api.doc("all_latlon")
    @api.marshal_with(AllFields)
    def get(self, **kwargs):
        """  Get all fields for a specific lat/lon  """
        path = request.url.strip(request.url_root)
        return base.get(path)


from karmapi.models.lists import Array
Array = api.model("Array", Array)


@api.route('/time/<field>')
class time(Resource):
    """  Copy data over from raw files into day folders 

    Assume path is relative to current working directory.
     """




    @api.doc("time")
    @api.marshal_with(Array)
    def post(self, **kwargs):
        """ Copy data over from raw files into day folders 

    Assume path is relative to current working directory.
    """
        path = request.url.strip(request.url_root)
        return base.build(parms)


from karmapi.models.lists import Array
Array = api.model("Array", Array)


from karmapi.models.lists import Array
Array = api.model("Array", Array)


@api.route('/time/<int:year>/<int:month>/<int:day>/<field>')
class day(Resource):
    """  Copy data over from raw files into day folders 

    Assume path is relative to current working directory.
     """




    @api.doc("day")
    @api.marshal_with(Array)
    def get(self, **kwargs):
        """ None """
        path = request.url.strip(request.url_root)
        return base.get(path)



    @api.doc("day")
    @api.marshal_with(Array)
    def post(self, **kwargs):
        """ Copy data over from raw files into day folders 

    Assume path is relative to current working directory.
    """
        path = request.url.strip(request.url_root)
        return base.build(parms)


from karmapi.models.lat_lon_grid import LatLonGrid
LatLonGrid = api.model("LatLonGrid", LatLonGrid)


@api.route('/space/<float:lat>/<float:lon>/<field>')
class latlon(Resource):
    """   Get all the data for a given lat/lon and field  """




    @api.doc("latlon")
    @api.marshal_with(LatLonGrid)
    def get(self, **kwargs):
        """   Get all the data for a given lat/lon and field  """
        path = request.url.strip(request.url_root)
        return base.get(path)


from karmapi.models.lat_lon_grid import LatLonGrid
LatLonGrid = api.model("LatLonGrid", LatLonGrid)


@api.route('/time/<int:year>/<int:month>/<int:day>/')
class all_day(Resource):
    """  Get all fields for a specific date  """




    @api.doc("all_day")
    @api.marshal_with(LatLonGrid)
    def get(self, **kwargs):
        """  Get all fields for a specific date  """
        path = request.url.strip(request.url_root)
        return base.get(path)


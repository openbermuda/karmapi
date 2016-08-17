
from karmapi import base

from flask import request
from flask_restplus import Namespace, Resource, fields

api = Namespace("euro", description="api for euro")


from karmapi.meta.weather import Image
Image = api.model("Image", Image)


@api.route('/locations/<location>/<item>')
class location(Resource):
    """ Rough notes on how to plot centred on a location using basemap

    What I really want to do is implement a Karma Pi path something like
    this:

    locations/{location}/{item}

    That will show you {item} from location's point of view.

    Now {item} works best if it does not have any /'s, so for
    the item parameter we'll convert /'s to ,'s and see how that looks.

    The idea is {item} will be a path to something in Karma Pi.

    So here is how it might go:

    >>> parms = base.Parms()
    >>> parms.path = "locations/bermuda"
    >>> parms.item = "time,2015,11,01,precipitation,image"

    >>> data = location(parms)

    In the background, some magic will read lat/lon for 
    locations/bermuda, or rather read the meta data and hope the 
    info is there.

    It will find the data for the precipitation image and use it to 
    create an image of the data using the "ortho" projection in basemap.

    This shows a hemisphere of the world, centered on the location.

    It would be good to offer other views.

    This can be supported by adding different end points for each view

    Eg:

    >>> parms = base.Parms()
    >>> parms.path = "locations/bermuda"
    >>> parms.item = "time,2015,11,01,precipitation,mercator"
    
    Might return a mercator projection.

    >>> parms = base.Parms()
    >>> parms.path = "locations/bermuda"
    >>> parms.item = "time,2015,11,01,precipitation,tendegree"

    Might return a 10 degree window around the location.
     """




    @api.doc("location")
    @api.marshal_with(Image, as_list=False)
    def get(self, **kwargs):
        """ Rough notes on how to plot centred on a location using basemap

    What I really want to do is implement a Karma Pi path something like
    this:

    locations/{location}/{item}

    That will show you {item} from location's point of view.

    Now {item} works best if it does not have any /'s, so for
    the item parameter we'll convert /'s to ,'s and see how that looks.

    The idea is {item} will be a path to something in Karma Pi.

    So here is how it might go:

    >>> parms = base.Parms()
    >>> parms.path = "locations/bermuda"
    >>> parms.item = "time,2015,11,01,precipitation,image"

    >>> data = location(parms)

    In the background, some magic will read lat/lon for 
    locations/bermuda, or rather read the meta data and hope the 
    info is there.

    It will find the data for the precipitation image and use it to 
    create an image of the data using the "ortho" projection in basemap.

    This shows a hemisphere of the world, centered on the location.

    It would be good to offer other views.

    This can be supported by adding different end points for each view

    Eg:

    >>> parms = base.Parms()
    >>> parms.path = "locations/bermuda"
    >>> parms.item = "time,2015,11,01,precipitation,mercator"
    
    Might return a mercator projection.

    >>> parms = base.Parms()
    >>> parms.path = "locations/bermuda"
    >>> parms.item = "time,2015,11,01,precipitation,tendegree"

    Might return a 10 degree window around the location.
     """
        path = request.url[len(request.url_root):]
        return base.get(path)


from karmapi.models.lists import Array
Array = api.model("Array", Array)


@api.route('/space/<field>')
class space(Resource):
    """  Extract all the data for all latitudes.

    This then allows us to get the data for any lat/lat
    quickly
     """




    @api.doc("space")
    @api.marshal_with(Array, as_list=False)
    def post(self, **kwargs):
        """ Extract all the data for all latitudes.

    This then allows us to get the data for any lat/lat
    quickly
    """
        path = request.url[len(request.url_root):]
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
    @api.marshal_with(Array, as_list=False)
    def post(self, **kwargs):
        """ Extract all the data for a given latitude.

    This then allows us to get the data for any lat/lon
    quickly.

    Alternatively, use build_space and do everythng in one.
    """
        path = request.url[len(request.url_root):]
        return base.build(parms)


from karmapi.meta.weather import AllFields
AllFields = api.model("AllFields", AllFields)


@api.route('/space/<float:lat>/<float:lon>')
class all_latlon(Resource):
    """  Get all fields for a specific lat/lon  """




    @api.doc("all_latlon")
    @api.marshal_with(AllFields, as_list=False)
    def get(self, **kwargs):
        """  Get all fields for a specific lat/lon  """
        path = request.url[len(request.url_root):]
        return base.get(path)


from karmapi.models.lists import Array
Array = api.model("Array", Array)


@api.route('/space/<float:lat>/<float:lon>/<field>')
class latlon(Resource):
    """   Get all the data for a given lat/lon and field  """




    @api.doc("latlon")
    @api.marshal_with(Array, as_list=False)
    def get(self, **kwargs):
        """   Get all the data for a given lat/lon and field  """
        path = request.url[len(request.url_root):]
        return base.get(path)


from karmapi.models.lat_lon_grid import LatLonTimeGrid
LatLonTimeGrid = api.model("LatLonTimeGrid", LatLonTimeGrid)


@api.route('/space/<float:min_lat>/<float:min_lon>/<float:max_lat>/<float:max_lon>/<field>')
class grid(Resource):
    """  Get all the data for a lat/lon grid  """




    @api.doc("grid")
    @api.marshal_with(LatLonTimeGrid, as_list=False)
    def get(self, **kwargs):
        """  Get all the data for a lat/lon grid  """
        path = request.url[len(request.url_root):]
        return base.get(path)


from karmapi.models.lists import Array
Array = api.model("Array", Array)


@api.route('/time/<field>')
class time(Resource):
    """  Copy data over from raw files into day folders 

    Assume path is relative to current working directory.
     """




    @api.doc("time")
    @api.marshal_with(Array, as_list=False)
    def post(self, **kwargs):
        """ Copy data over from raw files into day folders 

    Assume path is relative to current working directory.
    """
        path = request.url[len(request.url_root):]
        return base.build(parms)


from karmapi.models.lists import Array
Array = api.model("Array", Array)


@api.route('/time/<int:year>/<int:month>/<field>')
class month(Resource):
    """  Sum all the days in the month 

    Create some stats on the totals
     """




    @api.doc("month")
    @api.marshal_with(Array, as_list=False)
    def post(self, **kwargs):
        """ Sum all the days in the month 

    Create some stats on the totals
    """
        path = request.url[len(request.url_root):]
        return base.build(parms)


from karmapi.meta.weather import AllFields
AllFields = api.model("AllFields", AllFields)


@api.route('/time/<int:year>/<int:month>/<int:day>')
class all_day(Resource):
    """  Get all fields for a specific date  """




    @api.doc("all_day")
    @api.marshal_with(AllFields, as_list=False)
    def get(self, **kwargs):
        """  Get all fields for a specific date  """
        path = request.url[len(request.url_root):]
        return base.get(path)


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
    @api.marshal_with(Array, as_list=False)
    def get(self, **kwargs):
        """  Returns data for a path 

    Assumes the data is just an array of floats.
     """
        path = request.url[len(request.url_root):]
        return base.get(path)



    @api.doc("day")
    @api.marshal_with(Array, as_list=False)
    def post(self, **kwargs):
        """ Copy data over from raw files into day folders 

    Assume path is relative to current working directory.
    """
        path = request.url[len(request.url_root):]
        return base.build(parms)


from karmapi.models.lists import Array
Array = api.model("Array", Array)


@api.route('/time/months/<field>')
class months(Resource):
    """  Create monthly totals for each month of data
     """




    @api.doc("months")
    @api.marshal_with(Array, as_list=False)
    def post(self, **kwargs):
        """ Create monthly totals for each month of data
    """
        path = request.url[len(request.url_root):]
        return base.build(parms)


"""
Utility to help generate meta data for a weather dataset.
"""



from datetime import date
import karmapi.weather
from karmapi.weather import RawWeather

from flask_restplus import fields

# defaults are good
raw = RawWeather()

meta = dict(
    base = "euro",
    fields = ['tmax', 'tmin', 'precipitation', 'evaporation', 'photo'],
    start_year = raw.start_day.year,
    start_month = raw.start_day.month,
    start_day = raw.start_day.day,

    end_year = raw.end_day.year,
    end_month = raw.end_day.month,
    end_day = raw.end_day.day,

    lats = raw.latitudes(),
    lons = raw.longitudes(),
)

AllFields = {
    (field, fields.List(fields.Float)) for field in meta['fields']}

Image = dict(image=fields.String)

Observation = dict(
    date=fields.Date,
    lat=fields.Float,
    lon=fields.Float,
    value=fields.Float,)

Observations = dict(
    field = fields.String,
    data = fields.List(fields.Nested(Observation)))
    

# Stuff we can build
meta['builds'] = dict(
    day = dict(
        doc="extract data for a day from the raw data",
        path="time/<int:year>/<int:month>/<int:day>/<field>",
        karma="karmapi.weather.build_day",
        model = "karmapi.models.lists.Array",
        source = "raw/{field}",
    ),
    month = dict(
        doc="get means for a month",
        path="month/<int:year>/<int:month>/<field>",
        karma="karmapi.weather.build_month",
        model = "karmapi.models.lists.Array",
    ),
    months = dict(
        doc="get means for a month",
        path="months/<field>",
        karma="karmapi.weather.build_months",
        model = "karmapi.models.lists.Array",
    ),
    time = dict(
        doc="extract data for a day from the raw data",
        path="time/<field>",
        karma="karmapi.weather.build_time",
        model = "karmapi.models.lists.Array",
        source = "raw/{field}",
    ),
    lon = dict(
        doc="extract data from the day files for a specific latitude",
        path="space/<float:lat>/<field>",
        karma="karmapi.weather.build_latitude",
        model = "karmapi.models.lists.Array",
    ),
    space = dict(
        doc="extract data from the day files for all lat/lons",
        path="space/<field>",
        karma="karmapi.weather.build_space",
        model = "karmapi.models.lists.Array",
    ),
)


# Stuff we can get
meta['gets'] = dict(
    day = dict(
        doc="Data for a specific year/month/day and field",
        path="time/<int:year>/<int:month>/<int:day>/<field>",
        karma="karmapi.weather.get_array_as_dict",
        model = "karmapi.models.lists.Array",
        ),
    month = dict(
        doc="Data for a specific year/month/ and field",
        path="month/<int:year>/<int:month>/<field>",
        karma="karmapi.weather.get_array_as_dict",
        model = "karmapi.models.lists.Array",
        ),
    all_day = dict(
        doc="All data for a specific year/month/day",
        path="time/<int:year>/<int:month>/<int:day>",
        karma="karmapi.weather.get_all_for_day",
        model = "karmapi.meta.weather.AllFields",
        ),
    latlon = dict(
        doc="Data for a specific lat/lon",
        path="space/<float:lat>/<float:lon>/<field>",
        karma="karmapi.weather.get_lat_lon_field",
        model = "karmapi.models.lists.Array",
        ),
    all_latlon = dict(
        doc="Return all data for a given lat/lon",
        path="space/<float:lat>/<float:lon>",
        karma="karmapi.weather.get_all_for_lat_lon",
        model = "karmapi.meta.weather.AllFields",
        ),

    grid = dict(
        doc="Return all data for a grid of lat/lons and a field",
        path="space/<float:min_lat>/<float:min_lon>/<float:max_lat>/<float:max_lon>/<field>",
        karma="karmapi.weather.get_grid",
        model = "karmapi.models.lat_lon_grid.LatLonTimeGrid",
        ),

    location = dict(
        doc="Return an image from location's perspective",
        path="locations/<location>/<item>",
        karma="karmapi.weather.location",
        model = "karmapi.meta.weather.Image",
        ),


)


if __name__ == '__main__':

    # write out meta data for dataset
    import json
    
    with open('meta.json', 'w') as out:
        out.write(json.dumps(meta, indent=True, sort_keys=True))

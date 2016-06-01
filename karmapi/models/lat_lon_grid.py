"""
Model for a lat lon grid
"""
from flask_restplus import fields, Model

LatLonGrid = Model(
    "LatLonGrid",
    lats = fields.List(fields.Float),               
    lons = fields.List(fields.Float),
    grid = fields.List(fields.Float))

LatLonTimeGrid = Model(
    "LatLonGrid",
    lats = fields.List(fields.Float),               
    lons = fields.List(fields.Float),
    start_day = fields.Date,
    end_day = fields.Date,
    grid = fields.List(fields.Float))

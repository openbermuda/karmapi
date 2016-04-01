"""
Model for a lat lon grid
"""
from flask_restplus import fields, Model

LatLonGrid = Model(
    "LatLonGrid",
    lats = fields.List(fields.Float),               
    lons = fields.List(fields.Float),
    grid = fields.List(fields.Float))


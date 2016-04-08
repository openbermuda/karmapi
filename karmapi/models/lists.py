"""
Model for a lat lon grid
"""
from flask_restplus import fields, Model

Array = dict(
    data = fields.List(fields.Float),               
)

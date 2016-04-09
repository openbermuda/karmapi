from flask_restplus import Api

from .euro import api as ns_euro

api = Api(
    Title="Karma Pi",
    version='0.0.1',
    description="Data with added karma and pi",
    )

api.add_namespace(ns_euro)

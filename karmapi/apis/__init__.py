from flask_restplus import Api

from .base import api as ns_base
from .stats import api as ns_stats
from .euro import api as ns_euro

api = Api(
    Title="Karma Pi",
    version='0.0.1',
    description="Data with added karma and pi",
    )

api.add_namespace(ns_base)
api.add_namespace(ns_stats)
api.add_namespace(ns_euro)

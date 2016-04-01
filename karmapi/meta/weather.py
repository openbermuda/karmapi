from datetime import date
import karmapi.weather
from karmapi.weather import RawWeather
from karmapi.models.lat_lon_grid import LatLonGrid

# defaults are good
raw = RawWeather()

META = dict(
    karma = karmapi.weather,
    model = LatLonGrid,
    start = raw.start_day,
    end   = raw.end_day,
    lats = raw.latitudes(),
    lons = raw.longitudes(),
)

# Stuff we can build
BUILD = dict(
    path="time/{year}/{month}/{day}/{field}",
    karma=karmapi.weather,
)

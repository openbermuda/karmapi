"""
Utility to help generate meta data for a weather dataset.
"""



from datetime import date
import karmapi.weather
from karmapi.weather import RawWeather

# defaults are good
raw = RawWeather()

meta = dict(
    start_year = raw.start_day.year,
    start_month = raw.start_day.month,
    start_day = raw.start_day.day,

    end_year = raw.end_day.year,
    end_month = raw.end_day.month,
    end_day = raw.end_day.day,

    lats = raw.latitudes(),
    lons = raw.longitudes(),
)

# Stuff we can build
meta['builds'] = dict(
    day = dict(
        path="time/{year}/{month}/{day}/{field}",
        karma="karmapi.weather.build_day",
        model = "karmapi.models.lat_lon_grid.LatLonGrid",
    )
)


# Stuff we can get
meta['gets'] = dict(
    day = dict(
        path="time/{year}/{month}/{day}/{field}",
        karma="karmapi.weather.get_day",
        model = "karmapi.models.lat_lon_grid.LatLonGrid",
     )
)


if __name__ == '__main__':

    # write out meta data for dataset
    import json
    
    with open('meta.json', 'w') as out:
        out.write(json.dumps(meta, indent=True))

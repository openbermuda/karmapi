""" Testing airport with hypothesis """

from sys import float_info
from math import isinf, isnan

import pandas
from collections import Counter

from hypothesis.strategies import (lists, tuples,
                                   floats, integers,
                                   fixed_dictionaries)
from hypothesis import given, note, assume, example

from karmapi import locations

@given(floats(min_value=-180.0, max_value=180.0))
def test_translate(value):
    """translate is self inverse 

    So translate(tranaslate(value)) == value

    Except for when it doesn't.  There is a discontinuity in the
    function areound value = +/- 180.
    """
    assume(not isnan(value))

    # if value is close to +/-180 then round trip can flip the sign
    assume(not abs((abs(value) - 180.0)) < float_info.epsilon)

    tvalue = locations.translate(value)
    ttvalue = locations.translate(tvalue)

    delta = ttvalue - value
    
    assert(abs(delta) <= 100.0 * float_info.epsilon)

@given(lists(floats(min_value=-180.0, max_value=180.0)))
@example([-179, 179, 0])
def test_find_biggest_gap(lons):

    assume(lons)
    
    start, end = locations.find_biggest_gap(lons)

    note("start, end: {}. {}".format(start, end))

    # so all the other lons lie between end and start
    xstart = start
    if start <= end:
        xstart += 360.0

    epsilon = .1
    for lon in lons:

        if abs(lon - start) < epsilon: continue
        if abs(lon - end) < epsilon: continue

        if lon < end:
            lon += 360.0

        assert(lon <= xstart)
        

@given(lists(
    tuples(floats(min_value=-90., max_value=90.0),
           floats(min_value=-180.0, max_value=180.0))))
def test_bounding_box(data):

    lats = [x[0] for x in data]
    lons = [x[1] for x in data]

    minlat, maxlat, minlon, maxlon = locations.get_bounding_box(lats, lons)

    note("Bounding box: {} {} {} {}".format(minlon, maxlon, minlat, maxlat))

    epsilon = float_info.epsilon
    border = 100.0 * epsilon
    border = 0.1
    minlat -= border
    minlon -= border
    maxlat += border
    maxlon += border

    note("Border: {}".format(border))
    
    note("Bounding epsilon box: {} {} {} {}".format(
        minlon, maxlon, minlat, maxlat))

    note("Minlon - Maxlon: {} {}".format(minlon, maxlon))

    note("biggest gap: {} {}".format(*locations.find_biggest_gap(lons)))

    for lat in lats:
        #assert((lat - minlat) >= (100.0 * epsilon))
        assert(minlat <= lat)
        #assert((maxlat - lat) >= (100.0 * epsilon))
        assert(lat <= maxlat)

    for lon in lons:

        if minlon <= maxlon:
            assert(minlon <= lon)
            assert(lon <= maxlon)
        else:
            if lon < minlon:
                lon += 360.0

            assert(minlon <= lon)
            assert(lon <= (maxlon + 360.0))
                     
            

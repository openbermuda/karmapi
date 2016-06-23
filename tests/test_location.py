""" Testing airport with hypothesis """

from sys import float_info
from math import isinf, isnan
from decimal import Decimal, localcontext, BasicContext

import pandas
from collections import Counter

from hypothesis.strategies import (lists, tuples,
                                   floats, integers, decimals,
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

    value = twoplaces(value)

    # if value is close to +/-180 then round trip can flip the sign
    assume(not abs((abs(value) - Decimal(180.0))) < float_info.epsilon)

    tvalue = locations.translate(value)
    ttvalue = locations.translate(tvalue)

    ttvalue = twoplaces(ttvalue)

    assert(value == ttvalue)


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

    xstart = twoplaces(xstart)
    end = twoplaces(end)

    epsilon = .1
    for lon in lons:

        lon = twoplaces(lon)

        if lon < end:
            lon += Decimal('360.0')

        assert(lon <= xstart)
        

@given(lists(
    tuples(floats(min_value=-90., max_value=90.0),
           floats(min_value=-180.0, max_value=180.0))))
def test_bounding_box(data):

    lats = [x[0] for x in data]
    lons = [x[1] for x in data]

    b = locations.get_bounding_box(lats, lons)

    minlon, maxlon, minlat, maxlat = b.minlon, b.maxlon, b.minlat, b.maxlat

    note("Bounding box: {} {} {} {}".format(minlon, maxlon, minlat, maxlat))

    note("Minlon, Maxlon: {} {}".format(minlon, maxlon))

    note("biggest gap: {} {}".format(*locations.find_biggest_gap(lons)))

    minlat, maxlat, minlon, maxlon = [
        twoplaces(x) for x in (minlat, maxlat, minlon, maxlon)]

    assert(minlat <= maxlat)
    assert(minlon <= maxlon)

    for lat in lats:
        lat = twoplaces(lat)
        #assert((lat - minlat) >= (100.0 * epsilon))
        assert(minlat <= lat)
        #assert((maxlat - lat) >= (100.0 * epsilon))
        assert(lat <= maxlat)

    for lon in lons:
        lon = twoplaces(lon)

        if lon < minlon:
            lon += Decimal('360.0')

        assert(minlon <= lon)
        assert(lon <= maxlon)
                     

@given(lists(
    tuples(floats(min_value=-90., max_value=90.0),
           floats(min_value=-180.0, max_value=180.0))))
def test_transposed_lat_lons(data):

    lats = [x[0] for x in data]
    lons = [x[1] for x in data]

    if len(data):
        assert(locations.lats_and_lons_are_transposed(lats, lons, 181.0)
               == False)
    else:
        assert(locations.lats_and_lons_are_transposed(lats, lons, 181.0)
               == None)

            
def twoplaces(x):
    """ Convert x to a decimal with two decimal places """
    tp = Decimal('0.01')
    return Decimal(x).quantize(tp)

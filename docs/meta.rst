===========
 Meta data
===========

The meta data for all this data needs a bit of a re-think.

There is the meta data that tells you about the raw data and how to
build stuff.

Then there is the meta data that people using the data want to see.

Some of this is common to both.

Paths and parms
===============

weather.py is getting a bit messy with gymnastics going from paths to
parms.

It would be neat if weather.py just worked with parms and we have ways
to convert between the two.

The meta matching code already creates parms from paths.


Dates, JSON and hierarchy
=========================

The weather data is arranged by year/month/day.

It is accessed with paths like::

    euro/time/2015/11/05/tmax

Or to access data for a latitude and longitude::

    euro/space/75.0/36.0/tmin

For web server calls you just need to give the path::

    http://karmapi/euro/time/2015/11/05/tmax

Each path splits into three pieces:

base:
    eg http://karmapi

source:
    euro

dataset:
    time/2016/02/29/tmax  - Max temperature data for 29th February 2016    

Date handling is messy.  JSON doesn't do dates, you have to pass them
around as strings.

If you have a date and want to get the path it can be error prone, for
example str(date(2016, 2, 29) gives "2016-02-29"

But there is always "".format()::

  "{:%Y/%m/%d}".format(date(1979, 11, 5))

Gives:

  "1979/11/05"

Example
=======

As an example, suppose we want to write some code to sum the data for
all days in a month.

The path to hit would be:

   [karmapi]/build/euro/total/<year>/<month>

For example:

   karmapi/euro/total/2015/02

Working with karmapi
====================

The aim is that karmapi data can either be on a webserver, accessed
via a RESTful interface or just on a local disk.

The goal is to avoid as much duplication of code as possible.

Build a module that works with the data on a file system and have the
same module magically work for the web based access.


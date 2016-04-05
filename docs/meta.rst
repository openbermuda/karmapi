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

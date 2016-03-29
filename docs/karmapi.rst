==========
 Karma Pi
==========

Karma Pi stores and serve csv data (also in JSON format) for physical
readings. 

CSV - Comma Separated Values

CVS - Concurrent Version System, jumbled CSV.

Pharmacy - front end to CVS, CVS is a US pharmacy.

Carma Phy - Jumbled pharmacy.

Karma Phy - Looks better spelt with a K

Karma Pi - Phy for physics, pi for math.

Interface
=========

Data is stored on disk with a folder for each source.

To support queries by time it will be organised in.

year/month/day

folders.

Meta Data
=========

Store this in git.

Includes the module to use for the folder.  If no module, use the
parent folder's module.

Checksums
=========

Store these with git too.

Sub-totals
==========

For each year make it easy to create totals for each month and day.

Have totals, but other moments too, standard deviation would be good
too.

pandas.DataFrame().describe() would be a good start.

Builds
======

Data for a path might not be available yet.  You can ask for it to be
built.

This might take a while, if karmpi can it will give you an estimate.

Calculated Data
===============

Some paths the data does not exist on disk but can be calculated if
desired and stored to disk.

Monitoring calls
================

How much data is created?  How long does it take?


Zeronet
=======

This is just one solution to syncing data.  It has a built in file
server too.

The idea would be to serve the metadata with zeronet and let other
processes figure out what data to pull.


Keeping the disk from filling up
================================

This is karma-pi.  One goal is to run it on raspberry-pi's.  SD cards
are fast and cheap these days.  64GB should be enough for some large
datasets.

Further, the storage can be distributed.

Store more detailed data at your location (and time), but have global
data to see the bigger picture.

Now there will be plenty of data that nobody has looked at for a
while, is large and easy to recalculate.

No need to be too aggressive here.  Monitor how disk use is growing,
know how much is spare and start deleting at around 50% use.

Bayesian Data
=============

Each source can be assigned likelihoods.  For example, for re-analysis
weather data, how close are the values to what was actually
experienced?  Can you give a distribution around the means?

When data sets are combined we can combine likelihoods too.

We can do the same with estimates of if the data will be needed in the
next day or other time horizon.

It is all about the prior distributions here, the assumptions you are
feeding into your data.

Notebooks
=========

Notebooks can be provided to illustrate how the data is used.

Documentation
=============

It would be wonderful if the documentation could be turned into the module
to access the data.

sphinx at least allows the code to be turned into docs.

Build the interface as you wrangle the data
===========================================

The idea here is to be systematic about the process of creating the
data.

So, when you have something that generates data from one folder to
another try and make it into something that works in a karmapi module.

Accessing data
==============

get_meta_data(path)
-------------------

Returns the meta data for the given path.

get_data(path)
--------------

Returns the data for the given path.

build(path)
-----------

Build data at path

Security
========

This is not a focus of the project.  The aim is to run it on pi's, so
the security just comes from physical access to the pi.

Data integrity, trust and collaborative sharing of data will be more
of a focus.  Trust across networks.

Privacy
=======

Karma Pi is about open data.  Data that people want to share.

Data that can help them understand their world.

Astro Pi
========

The astro pi plugs into a raspberry pi and has pressure, humidity and
temperature sensors.

It also has a compass, accelerometer, an 8x8 screen and a tiny
joy-stick.

They make simple, mobile weather stations.

The plan is to store astro pi data here, or rather the tools here will
make that easy.

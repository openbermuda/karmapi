==========
 Karma Pi
==========

Time for an update, things moving along.

Bits slowly evolving as time passes by.

Finding the core, 3.6, idle, async await.

Data and plotting and models to fit.

Forecasts to make, but how to share?

This is a place to share my ideas.

Forks are welcome, don't be afraid.

Check the commit log, what catches your eye?

Click on the delta, see what changed?

What was I doing and why might it matter?

A checksum from git, to log a commit.

A seed from a chain to see if it runs.

And a checksum with zeroes to see if its right.

Collect the statistics a map reduce.

And check the statistics with the same zero sum.

Rewarding the miners with information.

Combining the skill of the players.

With their shared observations in time.
 
A commit with a future, when will its time be?

Karma pi -- tools to help people of all ages to explore our world.

Working with python, pi and jupyter.

On earth and beyond, to look to the future.

Out will come what we put in, with feedback learning and value therein.


Get out what you put in
=======================

Cooperative and collaborative multi tasking are a core idea.  If we
know all processes running on the network are good actors, then we can
make very much better use of the available compute resources.

Further, this will also ease the flow of information across processes.

Keep it small
=============

Karma pi tries to turn problems into things that others have already
solved.  *pandas*, *matplotlib*, *jupyuter*, *scipy* and *numpy*
provide most of what is needed.

Python3.5 provides significant new features that make writing of
cooperative multi-tasking code very much easier.  *curio* simplifies
the use further, making it very easy to write high performance
dynamic applications.

Pig Farm and Currie
===================

Pig, piglet and joy are attempts at providing a simple graphical user
interface to plots from matplotlib.  It also supports the tkinter
Canvas and a number of other widgets.

*currie* uses these libraries to manage a collection of these widgets
 (or *piglets*).  Each widget is a single window, a single window is shown at once.

Piglets have *start()* and *run()* co-routines. *start* is *await*'ed
when the piglet is constructed, *run() is awaited each time the piglet
becomes the active one and canceled when the user switches to another
piglet.

Press 'h' for help on which keyboard presses do what.

Pig Farm started life as part of currie, but now has a life of its
own.

It has a PigFarm where you can run piglets.  Piglets are just windows
displaying something.

There are also *micks*.  These are time stamped streams of data, that
piglets can display, using artists.


Hush
====

*hush* turns signal into noise.

For now, it uses *pyaudio* to read data from any microphones connected to the device.

How Karma Pi  got its name
==========================

The project started as a place to store and serve csv data (also in JSON
format) for physical readings.

These readings might come from anything from a raspberry pi sense hat,
a satellite orbitting the earth, or logs kept by astronomers over the
centuries.

CSV - Comma Separated Values

CVS - Concurrent Version System, jumbled CSV.

Pharmacy - front end to CVS, CVS is a US pharmacy.

Carma Phy - Jumbled pharmacy.

Karma Phy - Looks better spelt with a K

Karma Pi - Phy for physics, pi for math.

Install
=======

Using pip::

   pip install karmapi

From source (eg git repository)::

   pip install ,


To install in development mode,   Navigate to the karmapi folder, then run::

  pip install -e .

The *-e* flag just says *install in editable mode*.

python and pip
==============

The current (0.6x) release requires python3.6.

You may need to run *pip3.6*  to get the *pip* that goes with your python3.6.

Ubuntu on Pi
============

So far have not got this working.  Sticking with raspbian for now.

http://releases.ubuntu.com/ubuntu-core/16/ubuntu-core-16-pi3.img.xz

# Note: replace /dev/sdX with the device name of your SD card (e.g. /dev/mmcblk0, /dev/sdg1 ...)

xzcat ~/Downloads/ubuntu-core-16-pi3.img.xz | sudo dd of=/dev/sdX bs=32M
sync


Learning python
===============

The python 3 tutorial is a great place to start:

https://docs.python.org/3/tutorial/

Pick a section that interests you.



curio
=====

Asynchronous magic library.


jupyter
=======

Inspiration, matplotlib, numpy, pandas, scipy and more.


matplotlib
==========

Plotting wonder.

pandas
======

Data frames, time series, statistics.


tkinter
=======

Simple, fast widgets

CKAN
====

Open data repositories.

FIXME
=====

Need to do a release with a sane set of requirements,   GETTING THERE

Want something that installs on a pi reasonably quickly,   GETTING THERE

[Assume pi already has python3.6]

Documentation
=============

This README is the most current at the moment.

Most code modules have some commentary at the top.

The git commit log is a good place to browse.  Commit messages are
brief, follow one that interests you.

There are *rst* files in the *docs* folder and a *conf.py* for *sphinx*::

  pip install sphinx

(pip3.6 if you have multiple pythons).

After that just run:

   make html

This should build html docs in the folder *_build/html*.

These can be served with python3::

    python -m http.server

This is not a secure server, but great for testing and on a trusted
network.

sphinx-autodoc
--------------

It would be good to get this working to see what the docs extracted
from the code look like.

Readthedocs
-----------

This might already be working.  FIXME check,

Docs need a fair bit of work, but better docstrings in the code turn into pretty good docs.

Release
=======

A release is overdue.  The next one will require python3.6.

For now, probably best to install from source code,

Making a new release
--------------------

Install some stuff needed to help with building releases::

   pip3.6 install twine wheel

Build a source releas (this just creates a tarball in the dists/ subfolder)::

   python setup.py sdist

Build a binary release::

   python setup.py bdist

Upload to PyPi with twine (you will need a username and password that
has access to the project you are trying to update)::

   twine upload dist/*

Develop
=======

git clone https://github.com/openbermuda/karmapi

cd karmapi

pip3.6 -e .

Python3.6 on Ubuntu 16.04 and raspbian
======================================

    git clone https://github.com/python/cpython

checkout v3.6.1 tag, then:

    ./configure
    make
    make install

Note: python3.6 can be installed (from universe) with apt on Ubuntu >=
16.10.

Things to do first
------------------

Some dev libraries need installing into Ubuntu for certain features to be built into the python.

tkinter is one part you need to make sure *tk-8.6-dev* is installed before ./configure.

The good news is that after the intitial build it all runs pretty fast.

* tk-8.6-dev -- for tkinter

* libbz2-dev -- compression library

* libssl-dev -- for ssl support required for pip3.6 to work.

TODO
====  

Eric IDLE.  Take a closer look at event handling.  Unify with pigfarm
event handling.

Be smarter about opening files with eric.  Add --file option to
command line tools?

MagicCarpet v Canvas: are they the same thing?

Sense Hat:  record and display data.   

Hush: use rate to figure out time when reading.  Adjust rate so we can
keep up?

Eigen-vectors: more on principal components.

Sync movement of sonogram with beat

Share micks with others.

Share yossers with others,

# Karma Pi

Karma pi is a place to come to find tools to help turn data into information.

Tools to help visualise and explore that data.  Tools that come with *python* batteries included.

Tools to help people of all ages to explore our world.

## Get out what you put in

Cooperative and collaborative multi tasking are a core idea.  If we
know all processes running on the network are good actors, then we can
make very much better use of the available compute resources.

Further, this will also ease the flow of information across processes.

## Keep it small

Karma pi tries to turn problems into things that others have already
solved.  *pandas*, *matplotlib*, *jupyuter*, *scipy* and *numpy*
provide most of what is needed.

Python3.5 provides significant new features that make writing of
cooperative multi-tasking code very much easier.  *curio* simplifies
the use further, making it very easy to write high performance
dynamic applications.

## Pigs and Currie

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


## Hush

*hush* turns signal into noise.

For now, it uses *pyaudio* to read data from any microphones connected to the device.

## How it got its name

The project start as a place to store and serve csv data (also in JSON
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

# Install

To install from source:

   python setup.py install


To install in development mode:

   python setup.py develop --user


## Ubuntu on Pi


http://releases.ubuntu.com/ubuntu-core/16/ubuntu-core-16-pi3.img.xz

# Note: replace /dev/sdX with the device name of your SD card (e.g. /dev/mmcblk0, /dev/sdg1 ...)

xzcat ~/Downloads/ubuntu-core-16-pi3.img.xz | sudo dd of=/dev/sdX bs=32M
sync


## Learning python

The python 3 tutorial is a great place to start:

https://docs.python.org/3/tutorial/

Pick a section that interests you.



## curio


## jupyter


## matplotlib


## pandas


## tkinter

## CKAN



## Install

pip install karmapi

### FIXME

Need to do a release with a sane set of requirements,

Want something that installs on a pi reasonably quickly,

[Assume pi already has python3.6]

## Readthedocs

This might already be working.  FIXME check,

Docs need a fair bit of work, but better docstrings in the code turn into pretty good docs.

## Release


## Develop

git clone https://github.com/openbermuda/karmapi

cd karmapi

python3 setup.py develop --user


## TODO

### Piglets

Console -- take a look at IDLE

MagicCarpet

### Hush

Eigen-vectors

Sync movement of sonogram with beat

Share micks with others.

Share yossers with others,

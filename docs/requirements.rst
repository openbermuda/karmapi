==============================
 What you need to get started
==============================


requirements.txt
================

jupyter, pandas, matplotlib, curio

note: check the requirements.txt for an alternate truth.

curio
-----

This is a new David Beazley project, so karmapi is using the latest
from github.  Add the following to requirements.txt:

   # curio, live on the edge, run from source
   -e git://github.com/dabeaz/curio.git


Alternatively, clone the repository and use:

   python setup.py develop --user

To install curio in development mode.
   
In Dave we trust.

flask_restplus
==============

Add this if you need hipflask.py to work.

imageio
=======

Working towards just using matplotlib.

pyqt5
=====

For the pig module (a pyqt graphical user interface) pyqt5 is required::

  pip3 install pyqt5

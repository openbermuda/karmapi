===========
 Eric Idle
===========

Eric Idle was a python.

So when Guido needed a simple development environment to show people
python, IDLE was born,


IDLE gives you a python prompt and a simple editor that knows a little
about python,


Python Console
==============

Since *currie* is currently running using tkinter and *currie* could
do with a console, time to take a look at IDLE.


Editor
======

An editor might be handy too,

It might be easy to get these working in a *PigFarm*.


idlelib
=======

The code for IDLE comes with python, you can import it with *idlelib*.

A quick look at the code and pig farm integration does not look too
hard.

The main obstacle is that *idlelib* had solved a lot of what *PigFarm*
and *piglets* are doing here.

Who knew that a library called *idlelib* written 20 years ago might
have saved some work?

async idle
==========

On a PigFarm the eventloop will be run by *curio*.



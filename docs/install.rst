=================
 Install Process
=================

If you are trying to install on Ubuntu 18.04 the following dialogue
may help.

Short version::

  python3.6 -m pip install karmapi


If that fails read on.

Preliminaries
=============

Hi Colin,

I hope this finds you well.

I have been working on some code to simulate and visualise waves
propagating through nested spheres.

I have it at the stage where it at least produces pretty images.  You
can find the code here:

https://github.com/swfiua/karmapi/blob/master/karmapi/cpr.py

It is at early stages for now, but soon should be able to include
modelling of time passing at different radii.

Once I get the code closer I expect to see some fascinating patterns emerging.

The goal is to be able to simulate the changing waves emerging from
the vicinity of a neutron star.

Once I have that we can then embed these in De Sitter space, per your
book/Gamma Ray paper and explore how the changing waves may interact.

So one of my next steps is to take another look at the Gamma Ray paper.

All the best.

Johnny



Colin Jun 7 (4 days ago) to me
=====================================

Hi

Just tried to run cpr.py.  I copied the code and added:

#! /usr/bin/env python

at the top to call python.  I got::

    cpr@poincare ~ 12:11pm > ./cpr.py
      File "./cpr.py", line 92
          async def run(self):
                  ^
    SyntaxError: invalid syntax

Did I do something silly?  Let me know when you'll be around and I'll
make the effort to come to the dept and chat.

Cheers


Jun 7 (4 days ago) to Colin
===========================

Hi Colin,
 
That's great that you tried to run it.

Nothing silly it looks like you are getting python 2.7 which is still
the default on a lot of linuxes.

The code requires python3.6 and other bits from karmapi, which in turn
depends on some other libraries.

git clone https://github.com/swfiua/karmapi

will get you the latest version of all the code.

I've just added a bin/karma script to the code that tries to run with
python3 -- hopefully 3.6+

I'd be curious what sort of error message that generates -- but may be
simpler to do this stuff when I am there.

I expect it will be some time the first week of July that I will be at
Warwick -- will update when I have firmer plans.

I hope by then to have the installation of karmapi a little smoother.
And with luck some interesting things to see.

All the best.

Johnny

	
Colin Jun 8 (3 days ago) to me
=====================================

git doesn't mean anything to my machine (Ubuntu 16.04LTS).  Do you know
the linux command to collect the files and install them?  I can collect
them with wget but would have to guess where to put them and how to
configure (if necessary).  C


Jun 8 (3 days ago) to Colin
===========================

I think it might be best to wait until we meet to see how best to get
this going on your machine -- or maybe find someone your end who knows
a little about python and git.

In the meanwhile I will do another release of the code to the python
packaging system which ought to make it easier to install.

If you can upgrade to Ubuntu 18.04 LTS that will get you python3.6
which should also simplify the process and ensure we are running the
same python.

You can get git installed with "sudo apt install git".

Thanks very much for trying with the code.

Johnny


Colin Jun 9 (2 days ago) to me
=====================================

I've upgraded to UBUNTU 18.04 BUT::

    cpr@poincare ~ 5:16pm > /usr/bin/env python --version
    Python 2.7.15rc1
    cpr@poincare ~ 5:17pm >

So how do I upgrade to python 3.6 from here?


swfiua@gmail.com <swfiua@gmail.com> Jun 9 (2 days ago) to Colin
===============================================================

OK, this is good.

18.04 has both python2.7 and python3.6

But 2.7 is still the default, so just type python3 and you should get python 3.6

I am going to work on the install for this stuff over the weekend, so
it is probably going to be worth waiting for that.

But meanwhile:

sudo apt install git 

and

git clone https://github.com/swfiua/karmapi

Will get you the latest karmapi.

Once you have that you will be able to update to my latest with a simple "git pull"

Good luck.

Johnny


Colin Jun 10 (1 day ago) to me
=====================================

I already cloned your karmapi directory and you're roght about python:

cpr@poincare ~ 10:13am > /usr/bin/env python3 --version
Python 3.6.5

Changing the top line of cpr.py to

##! /usr/bin/env python3

gets rid of the syntax error, but now I get:

cpr@poincare ~ 10:07am > ./cpr.py
Unmatched '"'.

which is very odd because I checked and they all match.  I must have a
corrupted input file .... any ideas?


Colin 12:25 PM (23 hours ago)to me
=========================================

Or maybe I've put your karmapi directory in a silly place.  It is in my
home directory where cpr.py is running.  C


4:23 PM (19 hours ago) to Colin
===============================

The unmattched " is a bit of a mystery.  

I have done a release of the project to the python package land.

You should be able to install this release with:

python3.6 -m pip install karmapi

This should download the dependencies and installs everything.

Once it is done you should be able to do:

python3.6 -m karmapi.cpr

And the cpr code should run.

Good luck!

Johnny


Colin 7:34 AM (4 hours ago) to me
========================================

Not out of the woods yet! :

cpr@poincare ~ 12:32pm > python3.6 -m pip install karmapi
/usr/bin/python3.6: No module named pip
cpr@poincare ~ 12:32pm >


swfiua@gmail.com <swfiua@gmail.com> 9:22 AM (2 hours ago) to Colin
==================================================================

Oh my... I thought that one was fixed these days.

There is a chicken and egg problem with python packaging:  you have to install the pip (python install package) module before you can install packages.

But pip itself is a package -- I thought it was now bundled with the core python, but apparently not.

sudo apt install python3-pip

Should get you the pip module.

I'm afraid the code is going to be super disappointing after all this.

Johnny


Colin Rourke10:59 AM (45 minutes ago) to me
===========================================

STILL not out of the woods::

    cpr@poincare ~ 3:42pm > python3.6 -m karmapi.cpr
    Traceback (most recent call last):
      File "/usr/lib/python3.6/runpy.py", line 193, in _run_module_as_main
          "__main__", mod_spec)
            File "/usr/lib/python3.6/runpy.py", line 85, in _run_code
                exec(code, run_globals)
                  File
                  "/home/cpr/.local/lib/python3.6/site-packages/karmapi/cpr.py",
                  line 30, in <module>
                      from PIL import Image, ImageTk
                        File
                        "/home/cpr/.local/lib/python3.6/site-packages/PIL/ImageTk.py",
                        line 31, in <module>
                            import tkinter
                            ModuleNotFoundError: No module named 'tkinter'
    cpr@poincare ~ 3:42pm > python3.6 -m pip install tkinter
      Collecting tkinter
      Could not find a version that satisfies the requirement tkinter (from versions: )
      No matching distribution found for tkinter
    cpr@poincare ~ 3:43pm > sudo apt install python3-tkinter
      Reading package lists... Done
      Building dependency tree
      Reading state information... Done
      E: Unable to locate package python3-tkinter

This is very odd because tkinter is a key module for a python program
labelpin that was written to go with my labelling package pinlabel so I
know it's on my computer.  It's obviously a version problem. How do I
trick python/tkinter into accepting a module written for python2 ???


swfiua@gmail.com <swfiua@gmail.com> 11:11 AM (33 minutes ago) to Colin
======================================================================

Try:

sudo apt install python3-tk

So this goes back to the default python on Ubuntu is still python2.7
-- so Ubuntu base install gives you everything you need for python2.7

For 3.6 it has all the packages available, but some fairly basic stuff
isn't there.

I use tk for simple user interfaces mainly because I thought it would
always be there :(

With luck you will get to run some see some of these soon.

Then we are into a whole different world of problems.

Johnny


Colin 11:20 AM (24 minutes ago) to me
============================================

I already found the tk-install command and I had to do this with version
2 as well for labelpin to run.  I also had to install pyaudio and now
cpr.py runs::


    cpr@poincare ~ 4:09pm > python3.6 -m karmapi.cpr
    pigfarm adding <class 'karmapi.mclock2.GuidoClock'> dict_keys([])
    pigfarm adding <class '__main__.NestedWaves'> dict_keys(['n', 'inc',
    'base'])
    <curio.sync.Event object at 0x7efcd5e6d1d0 [unset,waiters:1]>
    spawning <coroutine object EventLoop.run at 0x7efcd993da40>

    building piglet: <class 'karmapi.mclock2.GuidoClock'>
    core pig creating self.event_queue
    Creating Pig with event queue <curio.queue.UniversalQueue object
    at 0x7efcd5e6d5f8>
    <method-wrapper '__init__' of PillBox object at 0x7efcd5e6d550>
    built <class 'karmapi.mclock2.GuidoClock'> <karmapi.mclock2.GuidoClock
    object at 0x7efcd5e6d470>
    building piglet: <class '__main__.NestedWaves'>
    core pig creating self.event_queue
    Creating Pig with event queue <curio.queue.UniversalQueue object
    at 0x7efcd5e6da20>
    <method-wrapper '__init__' of Canvas object at 0x7efcd5e6d9b0>
    built <class '__main__.NestedWaves'> <__main__.NestedWaves object
    at 0x7efcd5e6d908>


BUT all I get is a blank tk terminal and no real output.  What next?


Colin 11:31 AM (13 minutes ago) to me
=====================================

Hold on.  If I type pig I get a varying screen colour and if I type
piglet I get a lulti-coloured clock.  Can I have a list of commands?


Colin 11:37 AM (7 minutes  to me
================================

Hold on again.  I just noticed another error on the main terminal::

  File "/home/cpr/.local/lib/python3.6/site-packages/karmapi/eric.py",
  line 49, in <module>
      from idlelib import pyshell
      ModuleNotFoundError: No module named 'idlelib'


And this time I get:

cpr@poincare ~ 4:32pm > sudo apt install python3-idlelib
[sudo] password for cpr:
Reading package lists... Done
Building dependency tree
Reading state information... Done
E: Unable to locate package python3-idlelib

????

swfiua@gmail.com <swfiua@gmail.com> 11:38 AM (6 minutes ago) to Colin
=====================================================================

sudo apt install idle-python3.6


swfiua@gmail.com <swfiua@gmail.com>11:37 AM (7 minutes ago) to Colin
====================================================================

type 'h' at any time for a list of keypresses that might do things.

the idea is 'n' and 'p' take you to next and previous widgets.

I usually throw in the clock -- it's mostly Guido van Rossum's code,
he had a clock like that at home growing up.

One other thing, type 'e' and it will show you the code for the module
using Idle, python's build in editor.

(oh great just seen latest email -- built in editor is AWOL)

The varying coloured screen is the NestedWave thing.   

The defaults have waves in the inner and outer spheres and then random
data in between.

As the spheres are stepped the waves propogate.

Johnny

	

Colin 3:07 PM (2 hours ago)
===========================

to me 
Well it's all installed and running.  Send me instructions for getting
the most interesting pictures.  And explain the connection with the new
paradigm! C


swfiua@gmail.com <swfiua@gmail.com>
4:59 PM (23 minutes ago)
to Colin 
python3 -m karmapi.cpr -n 10 --inc 10 --base 100

Will give you 10 nested spheres.   The inner sphere has a 100x100 grid.

The next 110x110 .. adding 10 to the grid size as you go out.

On my machine it is a little slow at this resolution.  If it is too
slow, drop the base number to say 50.

Once you see an image j and k will step you through the layers.    

Oh and 'r' is useful: it re-randomises everything so you can watch how
things settle down.

I tend to run it with the tk window filling half the screen and the
console so I can see the print's littered in the code.

I found with these parameters you see some stunning patterns emerging.

Now these are to some degree artifacts of my coding, in particular how
I update the inner spheres.

You will see square patterns in the images: I give equal weight to all
cells in the inner/outer spheres that lie in a square centred around
the point.

At this point there is nothing from paradigm in how the code works,
but there are some hooks to help add this in.

The plan is to set the mass and the radii of each spherical shell and
so be able to have waves propogate at different rates based on
relative time.

So, I think the way forward from here is to look at geodesics as per
the gamma ray paper.

I am going to be giving a talk to the python group back here in Ottawa
in late July, so I hope to have something closer to the paradigm by
then.

Johnny


swfiua@gmail.com <swfiua@gmail.com> 5:15 PM (7 minutes ago) to Colin
====================================================================


Forgot to say, the patterns on the inner spheres tend to converge to a
fixed pattern if you let it run long enough.  Or maybe it is something
like Conway's game of life.  I just let it run and it has ended up all
black.  So file that one under bugs?

Also, all the inner spheres seem to converge to the same pattern.

Again, all just artifacts of the code (and the quantisation that is
going on too and the order in which I do updates) and bugs, lots of
those.

The key bits of code for the images are in the cpr.Sphere object.

The run, end_run and sample methods.

Johnny

PS there is an unfortunate typo in the help message you get when you
type 'h' on Guido's clock.

Post Install
============

If you want to take a look at the latest code::

  git clone https://github.com/karmapi/swfiua

This should give you a folder, *karmapi*::

  cd karmapi

If you want to install that version under the local user try::

  python3 setup.py install --user

To refresh to the latest code on github::

  git pull

And re-run the install::

  python3 setup.py install --user
 
I have this little function devined in .bashrc::

  function karma
  {
     module=karmapi.$*
     python3.6 -m $module
  }

Which allows me to type things like::

  karma cpr

  karma currie

  karma zen

  karma wc

To get help on options that may be available::

  karma cpr -h

Many karma pi modules can be run this way.

Check the code to see what the options actually do.

The *argparse* module is used for option parsing.
  
  
Raspberry Pi
============

That is a whole other adventure.

But Raspbian Stretch may have python 3.6.   Fingers crossed.

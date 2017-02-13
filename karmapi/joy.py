"""
Magic backend selector for pig.

Called joy because of Great Uncle Urban's letter, where joy looked like pig

Here is where base classes for backends are defined.

joy also allows you to set the backend

currie is an evolving example of how to use joy.

And then there is piglet and widgets.

Time to rationalise all this and add some events.

So the plan today is:

joy:

   Base classes such as EventLoop, Piglet and PigFarm.

piglet:

   General purpose piglet widgets, built with joy.

   Imports according to setting of joy backend at time of import:

      This backend switching complicates things a little on the 
      code and usability side, but at this point knowing new backends 
      might be very easy to add is a good thing.
   
 
currie:

    An example of how to do magic,


To resolve:

    Get keyboard events flowing through to piglets.

    First stage: use the eventloop to get the events to the PigFarm.

    PigFarm can then just let the piglets suck the events off a queue.
"""

import os

BACKEND = 'tk'

if 'PIG' in os.environ:
    BACKEND = os.environ['PIG']

def set_backend(backend):

    global BACKEND

    BACKEND = backend

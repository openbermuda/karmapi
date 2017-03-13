""" Eric - grandpa time machine


Idle (named after python Eric Idle)

Thing of Eric as grandpa.  Somewhere you can go to find new, maybe
old, ways of doing things.

grandpa is the one who shows a grandchild how to make jelly after a
hurricane when the electricity is gone and the fridge is off.

Make a cradle with string and lower the bowl of jelly so it rests in
the water of the water tank.  This is cool, after a couple of hours
the jelly will be set.

No jelly here, but Idle: an interactive python promt.

You can ask the prompt about python, see how it works,

Come here to import a module, see what it does, read the code.

Change the code, see what happens.


IDLE
----

IDLE is built with *idlelib*, part of core python.

It implements some interesting widgets, in tkinter.  There is quite a
bit of duplication between karmapi piglets, PigFarm and IDLE.

Making it all async might be interesting.

For now, aiming for a python console. 


Getting a curious "AttributeError:  'Eric' object has no attribute _w"

This happens in PigFarm.build().

_w might be meant to be some sort of file descriptor, maybe output files?

Finding IDLE fun to use.

"""
import inspect

from idlelib import pyshell

from karmapi import piglet

def doc(x):

    print(x.__doc__)

def luke(x):

    print(inspect.getsource(x))

class Eric(piglet.Pig):
    """ An async python console, using IDLE """

    def __init__(self, parent, filename=None):

        #flist=None, filename=None, key=None, root=None):
        flist = pyshell.PyShellFileList(parent)
        pyshell.use_subprocess = True
        
        flist.open_shell()

        # FIXME -- add files to open in idle editor
        filename = filename or __file__

        self.console = pyshell.PyShellEditorWindow(
            flist, filename, None,  parent)

    async def run(self):

        pass

    async def start(self):

        if self.farm.current:
            self.filename = instpect.getsourcefile(self.farm.current)




    



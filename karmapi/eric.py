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

"""

from idlelib import pyshell

from karmapi import piglet

class Eric(piglet.Pig):
    """ An async python console, using IDLE """

    def __init__(self, parent):

        #flist=None, filename=None, key=None, root=None):
        flist = pyshell.PyShellFileList(parent)
        pyshell.use_subprocess = True
        
        flist.open_shell()
        self.console = pyshell.PyShellEditorWindow(
            flist, None, None,  parent)




    



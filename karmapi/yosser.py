"""
Yosser, the builder.

Back in the early 80's the BBC made a mini series, "The boys from the
blackstuff".  It was about builders working on the roads in Liverpool
and unemployment.

There was a character, "Yosser, Hughes", desperate for a job.  He'd
say, "Go on gi' us a job, I can do that".

So this is Yosser.  If you have some compute intensive stuff to do
then yosser can help you.

Just tell him what to build, and he will give it a go.
"""
from karmapi import base

def look_for_a_job():
    """ Returns the path of something to build """
    raise NotImplemented

def build():
    """FIXME: need to time builds and how much disk gets filled.

    Jobs should aim to be low memory demand, say 500MB.

    Or rather, we should know what resources are available 
    and proceed accordingly.

    On a pi, there are four cores.  

       one core can run communications, 
       one core can build
       one can be used by the processes directing operations
       one can manage the disk space

    Add more pi's and change the mix as necessary.
    """
    raise NotImplemented
    
def sleep():
    """ Even Yosser needs to sleep now and then """
    raise NotImplemented




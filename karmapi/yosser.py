"""Yosser, the builder.

Back in the early 80's the BBC made a mini series, "The boys from the
blackstuff".  It was about builders working on the roads in Liverpool
and unemployment.

There was a character, "Yosser, Hughes", desperate for a job.  He'd
say, "Go on gi' us a job, I can do that".

So this is Yosser.  If you have some compute intensive stuff to do
then yosser can help you.

Just tell him what to build, and he will give it a go.

curio
=====

So, the author says that at some point it will fly at you like a swarm
of stinging bees.

So, yosser, meet curio.

**Stands well back**

So the idea is a micro service that listens for jobs.

Let's call it *icandothat*

Just send it your message and yosser will take care of the rest.

So we need a server to send messages to, curio.socket should have most
of what is needed.

We need a queue to save messages in.   curio.queue works here.

And we need a way to pop messages off the queue and turn them into tasks.
The queue does the popping and so we just need to fire off tasks.

Finally, we need some way to let clients know when the taks is done.

Now the tasks are the tricky bit, because they might take a while.

They just need to farm out the actual work to another process.  This
looks to be the job of curio.workers.  run_in_process() sounds like it
might do the trick.

No threads, otherwise there will be stinging bats.

This thing should just run.

"""
import curio

from curio import socket, queue, workers

from karmapi import base

# last in first out seems right for yosser
# but there is also queue.EpicQueue -- not sure if that comes with bats.
lifo = queue.LifoQueue()

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


def run():
    """ Start yosser runnint """

    # create a server
    server = icandothat()

    # queue
    queue = queue.EpicQueue()

    # now make it work...

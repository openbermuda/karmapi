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

Multiple yossers would be good.  So when a job needs to be start,
await yosser, then let it build in its own process.

No threads, otherwise there will be stinging bats.

This thing should just run.

Oh, and there is a sneaking suspicion curio.queue.EpicQueue does all
of this.  Or very nearly, but then there might be stinging bats.


So yosser is now mostly working, in so far as clients can get it to fire off a job.

At this point some sort of protocol is needed.

A client end and a server,

A client running as a curio task.

A server running as another curio task in a separate process.


"""
import argparse
import random
from multiprocessing import cpu_count
import time
import sys
import functools

# make print flush
print = functools.partial(print, flush=True)

import curio

from curio import socket, queue, workers

from karmapi import base

# last in first out seems right for yosser
# but there is also queue.EpicQueue -- not sure if that comes with bats.
LIFO = queue.LifoQueue()
PORT = 2469

def meta():

    return dict(name='yosser', karma='build')

def build(meta):
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
    # lets see how this goes -- just do a random sleep for now
    nap = random.randint(0, 10)
    time.sleep(nap)
    return nap
    

async def yosser_handler(client, addr):
    print('Connection from', addr)
    
    s = client.as_stream()
    async for line in s:
        try:
            #meta = json.loads(line.encode('ascii'))
            meta = line

            # FIXME: parse line to get instruction
            # path:  path_to_build
            # meta:  meta data for thing to build

            result = await workers.run_in_process(build, meta)
            print('got result:', result)

            # send the result back
            resp = str(str(result) + '\n')
            await s.write(resp.encode('ascii'))
            print('result sent to client')
            
            # yosser now ready for another build
            await YOSSERS.put(yosser)

        except ValueError:
            await s.write(b'Bad input\n')
    print('Connection closed')
    await client.close()

start_event = curio.Event()


async def yosser(*args, **kwargs):
    """ A yosser example 

    This is just an adapted version of the curio hello example.


    """

    while True:
        try:
            print('Go on, giusajob?')
            await curio.timeout_after(1, start_event.wait())
            break
        except curio.TaskTimeout:
            print('I can do that!?!')
    try:
        # 
        print('Building the Millenium Falcon in Minecraft')

        # ok at this point run a server to wait for work
        total = 0
        total = await curiot.tcp_server('', args.port, yosser_handler)

    except curio.CancelledError:
        # need a way to send yosser home
        print('Off home status:', total)
        # hmm.. missing yosser status reports never get here?


async def client(path=None, meta=None, host='localhost', port=PORT):
    """ Client to submit tasks to yosser """
    s = await socket.socket()

    c = await s.connect((host, port))

    if path is not None:
        result = await s.send('path: {}\n'.format(path))
    else:
        result = await s.send('path: {}\n'.format(meta))

    answer = await s.recv(10000)

    return answer


class Yosser:
    """ An asynchronous job server """

    def __init__(self):

        self.queue = curio.Queue()

    def put(self, task):
        """ Maybe EventLoop is just a curio.EpicQueue? """
        self.queue.put(task)

        
    async def giusajob(self):
        """  Wait for an event to arrive in the queue """

        while True:
            
            task = await self.queue.get()

            await curio.run_in_process(task)


    async def run(self):

        giusajob_task = await curio.spawn(self.giusajob())

        tasks = [giusajob_task]

        await curio.gather(tasks)

    
def get_parser():
    
    parser = argparse.ArgumentParser()

    # default, take half the cores
    share = 0.5
    
    yossers = cpu_count()
    parser.add_argument('-n', type=int, default=yossers)
    parser.add_argument('--port', type=int, default=PORT)
    parser.add_argument('--host', default='')
    parser.add_argument('--share', type=float)

    return parser
    
def main():

    parser = get_parser()
    args = parser.parse_args()

    curio.run(curio.tcp_server(args.host, args.port,
                               yosser_handler))
    

if __name__ == '__main__':

    main()

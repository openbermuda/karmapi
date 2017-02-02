"""
Currie -- you can do magic.

Goal here is to have a thread launching piglets.

And curio controlling the operation.

Aim to use joy to control which widget loop to use.

No piglets known to be harmed with this code.

So there is a pig farm and piglets running everywhere.

And currie doing magic.
"""
from karmapi import pig, piglet
from karmapi import widgets
import curio
import tkinter



class PigFarm:
    """ A pig farm event loop """

    def __init__(self, meta=None, events=None):

        self.event = events # curio.UniversalQueue()

        self.piglet_event = curio.UniversalQueue()

        self.piglets = curio.UniversalQueue()

        self.builds = curio.UniversalQueue()

        # start a gui eventloop
        self.eloop = piglet.EventLoop()
        self.piglets.put(self.eloop.run())


    def add(self, pig):

        self.builds.put(pig)
    

    async def build(self):
        """ Do the piglet build """

        while True:
            meta = await self.builds.get()
        
            #piglet = pig.build(meta)
            
            piglet = meta(self.eloop.app.winfo_toplevel())
            piglet.pack()
            print('built', piglet)

            await self.piglets.put(piglet.run())


    async def run(self):
        """ Make the pigs run """

        # spawn a task for each piglet

        # spawn a task to deal with keyboard events

        # spawn a task to deal with mouse events

        # ... spawn tasks to deal with any events

        builder = await curio.spawn(self.build())

        while True:
            while self.piglets:
                print('piglets', self.piglets.qsize())
                # spawn a task for each piglet
                piglet = await self.piglets.get()

                print('spawning', piglet)

                await curio.spawn(piglet)

            # wait for an event
            event = await self.event.get()
            print(self, event)


def main():

    farm = PigFarm()

    farm.add(widgets.InfinitySlalom)

    curio.run(farm.run())


if __name__ == '__main__':

    main()
    

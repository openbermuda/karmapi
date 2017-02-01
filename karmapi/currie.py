"""
Goal here is to have a thread launching piglets.

And curio controlling the operation.

Aim to use joy to control which widget loop to use.

No piglets known to be harmed with this code.
"""
from karmapi import pig
import curio
import tkinter



class PigFarm:
    """ A pig farm event loop """

    def __init__(self, meta=None, events=None):

        self.event = events # curio.UniversalQueue()

        self.piglet_event = curio.UniversalQueue()

        self.piglets = curio.UniversalQueue()

        # start a gui eventloop
        pass



    def build(self, meta):
        """ Do the piglet build """

        piglet = backend.build(meta)

        self.piglets.push(piglet)



    async def run(self):
        """ Make the pigs run """

        # spawn a task for each piglet

        # spawn a task to deal with keyboard events

        # spawn a task to deal with mouse events

        # ... spawn tasks to deal with any events
        

        while True:
            while self.piglets:
                # spawn a task for each piglet
                piglet = self.piglets.pop()

                await curio.spawn(piglet.run())

            # wait for an event
            event = await self.event.pop()

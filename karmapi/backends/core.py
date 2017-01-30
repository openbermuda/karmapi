"""
Common backend core.

This provides stuff that everything needs.

Backends should build with what is here,
"""

import curio

class Widget:

    def __init__(self, *args, **kwargs):

        
        self.event_queue = curio.UniversalQueue()

    async def karma(self, event):
        """ Turn events into karma """

        await self.event_queue.push(event)


    async def run(self):

        while True:
            await event = self.event_queue.pop()

            await self.process(event)


    async def process(self):
        """ Make it do something """
        passs

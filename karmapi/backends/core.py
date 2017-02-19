"""
Common backend core.

This provides stuff that everything needs.

Backends should build with what is here,
"""

import curio

class Pig:

    # default mapping of keys to karma
    keymap_karma = dict(
        a='begin',
        e='end',
        u='up',
        d='down',
        p='previous',
        n='next',
        z='zoom',
        )

    def __init__(self, *args, **kwargs):

        self.keymap = self.keymap_karma.copy()

        print('core pig creating self.event_queue')
        self.event_queue = curio.UniversalQueue()

        print('Creating Pig with event queue', self.event_queue)

        self.event_map = {}

    def add_event_map(self, event, coro):

        self.event_map[event] = coro

    async def karma(self, event):
        """ Turn events into karma """

        await self.event_queue.push(event)


    async def start(self):
        pass
    
    async def run(self):

        print(Pig, 'run cooroutine starting')

        while True:
            event = await self.event_queue.get()

            print(self, 'got an event', event)
            await self.process(event)


    async def process(self, event):
        """ Process events """

        method = getattr(self, str(event))

        if method:

            return await method()
        

        

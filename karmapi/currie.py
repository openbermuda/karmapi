"""
Currie -- you can do magic.

Goal here is to have a thread launching piglets.

And curio controlling the operation.

Aim to use joy to control which widget loop to use.

No piglets known to be harmed with this code.

So there is a pig farm and piglets running everywhere.

And currie doing magic.
"""
from collections import deque
import curio

from karmapi import hush


class PigFarm:
    """ A pig farm event loop """

    def __init__(self, meta=None, events=None):

        self.event = curio.UniversalQueue()

        self.piglet_event = curio.UniversalQueue()

        self.piglets = curio.UniversalQueue()

        self.builds = curio.UniversalQueue()

        self.widgets = deque()
        self.current = None

        from karmapi import piglet

        # this probably needs to be a co-routine?
        self.eloop = piglet.EventLoop()
        self.eloop.set_event_queue(self.event)
        
        self.piglets.put(self.eloop.run())

        self.micks = curio.UniversalQueue()

    def status(self):

        print('builds: ', self.builds.qsize())
        print('piglets::', self.piglets.qsize())
        print('micks:', self.micks.qsize())


    def add(self, pig, kwargs=None):

        kwargs = kwargs or {}
        print('pigfarm adding', pig, kwargs)

        self.builds.put((pig, kwargs))

    def add_mick(self, mick):

        self.micks.put(mick)
    

    async def build(self):
        """ Do the piglet build """

        while True:
            meta, kwargs = await self.builds.get()
            print('building piglet:', meta)
        
            #piglet = pig.build(meta)

            piglet = meta(self.eloop.app.winfo_toplevel(), **kwargs)
            piglet.bind('<Key>', self.keypress)

            self.widgets.append(piglet)

            # let the piglets see the farm
            piglet.farm = self
            print('built', meta, piglet)

            await self.piglets.put(piglet.run())

    def next(self):
        """ Show next widget """
        print('current', self.current)
        if self.current:
            self.current.pack_forget()

            self.widgets.append(self.current)

        self.current = self.widgets.popleft()
        self.current.pack(fill='both', expand=1)
        

    def keypress(self, event):
        
        print('currie event', event)
        # Fixme -- turn these into events that we can push onto piglet queues

        self.events.put(event)

    async def run(self):
        """ Make the pigs run """

        # spawn a task for each piglet

        # spawn a task to deal with keyboard events

        # spawn a task to deal with mouse events

        # ... spawn tasks to deal with any events

        builder = await curio.spawn(self.build())

        while True:
            while self.piglets.qsize():
                # spawn a task for each piglet
                piglet = await self.piglets.get()

                print('spawning', piglet)

                await curio.spawn(piglet)

                await curio.sleep(1)

            # wait for an event
            #event = await self.event.get()
            #print(self, event)

            # cycle through the widgets
            print()
            print('next widget')
            self.next()
            await curio.sleep(1)



def main():

    import argparse
    
    parser = argparse.ArgumentParser()

    parser.add_argument('--pig', default='tk')
    parser.add_argument('--wave')
    parser.add_argument('--gallery', nargs='*', default=['../gallery'])
    
    parser.add_argument('--thresh', type=float, default=10.0)

    parser.add_argument('--monitor', action='store_true')

    
    args = parser.parse_args()

    # import from pig stuff here, after talking to joy
    from karmapi import joy
    joy.set_backend(args.pig)

    
    from karmapi import pig, piglet
    from karmapi import widgets

    # what's this doing here?
    #import tkinter

    farm = PigFarm()

    print('building farm')
    farm.status()
    from karmapi.mclock2 import GuidoClock
    from karmapi.bats import StingingBats

    if args.monitor:

        farm.add(widgets.Curio)

    im_info = dict(galleries=args.gallery, image='princess')
    print(piglet.Image, im_info)
    
    #farm.add(piglet.Image, im_info)
    farm.add(StingingBats)
    farm.add(widgets.SonoGram)
    #farm.add(piglet.XKCD)
    farm.add(widgets.InfinitySlalom)
    farm.add(GuidoClock)
    #farm.add(piglet.Label)

    # add a couple of micks to the Farm
    if args.wave:
        farm.add_mick(hush.Connect(hush.open_wave(args.wave)))
        farm.add_mick(hush.Connect(hush.open_wave(args.wave)))
    else:
        farm.add_mick(hush.Connect())
        farm.add_mick(hush.Connect())

    farm.status()

    curio.run(farm.run(), with_monitor=True)


if __name__ == '__main__':

    main()
    

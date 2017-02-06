"""
Currie -- you can do magic.

Goal here is to have a thread launching piglets.

And curio controlling the operation.

Aim to use joy to control which widget loop to use.

No piglets known to be harmed with this code.

So there is a pig farm and piglets running everywhere.

And currie doing magic.
"""
import curio



class PigFarm:
    """ A pig farm event loop """

    def __init__(self, meta=None, events=None):

        self.event = events # curio.UniversalQueue()

        self.piglet_event = curio.UniversalQueue()

        self.piglets = curio.UniversalQueue()

        self.builds = curio.UniversalQueue()

        from karmapi import piglet

        # this probably needs to be a co-routine?
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
            piglet.bind('<Key>', self.keypress)
            piglet.pack()
            print('built', piglet)

            await self.piglets.put(piglet.run())

    def keypress(self, event):
        
        print('currie event', event)
        # Fixme -- turn these into events that we can push onto piglet queues

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

    import argparse
    
    parser = argparse.ArgumentParser()

    parser.add_argument('--pig', default='tk')
    parser.add_argument('--file')
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

    from karmapi.mclock2 import GuidoClock

    if args.monitor:

        farm.add(widgets.Curio)

    #farm.add(widgets.SonoGram)
    farm.add(widgets.InfinitySlalom)
    farm.add(GuidoClock)

    curio.run(farm.run(), with_monitor=True)


if __name__ == '__main__':

    main()
    

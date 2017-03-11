""" Pig Farm

A collection of pigs and piglets.

Pigs are windows, piglets are things running in the pig farm.

"""

from collections import deque
import curio
from pathlib import Path
import inspect

from PIL import Image

from karmapi import hush
from karmapi import pig

from tkinter import Toplevel


class PigFarm:
    """ A pig farm event loop """

    def __init__(self, meta=None, events=None):

        self.event = curio.UniversalQueue()

        self.piglet_event = curio.UniversalQueue()

        self.piglets = curio.UniversalQueue()

        self.builds = curio.UniversalQueue()

        self.widgets = deque()
        self.current = None
        self.eric = None

        self.create_event_map()

        from karmapi import piglet

        # this probably needs to be a co-routine?
        self.eloop = piglet.EventLoop()
        self.eloop.set_event_queue(self.event)

        self.piglets.put(self.eloop.run())

        self.micks = curio.UniversalQueue()

    def add_event_map(self, event, coro):

        self.event_map[event] = coro

    def create_event_map(self):

        self.event_map = {}
        self.add_event_map('p', self.previous)
        self.add_event_map('n', self.next)
        self.add_event_map('h', self.help)
        self.add_event_map('c', self.show_monitor)
        self.add_event_map('e', self.show_eric)


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
        self.piglets.put(mick.start())

    def toplevel(self):
        """ Return toplevel piglet """
        return self.eloop.app.winfo_toplevel()


    async def build(self):
        """ Do the piglet build """

        while True:
            meta, kwargs = await self.builds.get()
            print('building piglet:', meta)

            #piglet = pig.build(meta)

            piglet = meta(self.toplevel(), **kwargs)
            piglet.bind('<Key>', self.keypress)

            self.widgets.append(piglet)

            # let the piglets see the farm
            piglet.farm = self
            print('built', meta, piglet)

            await self.piglets.put(piglet.start())

    async def start_piglet(self):

        self.current.pack(fill='both', expand=1)
        self.current_task = await curio.spawn(self.current.run())

    async def stop_piglet(self):

        await self.current_task.cancel()
        self.current.pack_forget()

    async def help(self):
        """ Show help """
        print('Help')
        print(self.event_map)

        keys = {}
        if self.current:
            keys = self.current.event_map.copy()

        keys.update(self.event_map)
        msg = ''
        for key, value in sorted(keys.items()):
            msg += '{} {}\n'.format(key, value.__doc__)

        from karmapi import piglet

        piglet.Help(msg)


    async def next(self):
        """ Show next widget """
        print('current', self.current)
        if self.current:
            self.widgets.append(self.current)

            await self.stop_piglet()

        self.current = self.widgets.popleft()
        await self.start_piglet()


    async def previous(self):
        """ Show previous widget """
        print('going to previous', self.current)
        if self.current:

            self.widgets.appendleft(self.current)

            await self.stop_piglet()

        self.current = self.widgets.pop()
        await self.start_piglet()

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

            # wait for an event
            #event = await self.event.get()
            #print(self, event)

            # cycle through the widgets
            print()
            #self.next()
            #await curio.sleep(1)

            event = await self.event.get()

            await self.process_event(event)

            print(event, type(event))

            print('eq', self.event.qsize())



    async def process_event(self, event):
        """ Dispatch events when they come in """

        coro = self.event_map.get(event)

        if coro is None and self.current:
            coro = self.current.event_map.get(event)

        if coro:
            await coro()
        else:
            print('no callback for event', event)


    async def show_monitor(self):
        """ Show curio monitor """
        
        from karmapi import widgets
        farm = PigFarm()
        farm.add(widgets.Curio)
        await curio.spawn(farm.run())

    async def mon_update(self, mon):

        while True:
            #await mon.update()
            await mon.next()
            await curio.sleep(1)

    async def show_eric(self):
        """ Show eric idle """

        if self.eric:
            return
        self.eric = True
        
        from karmapi.eric import  Eric
        farm = PigFarm()
        filename = None
        if self.current:
            filename = inspect.getsourcefile(self.current.__class__)
        farm.add(Eric, dict(filename=filename))

        await curio.spawn(farm.run())

        farm.toplevel().withdraw()
        



class Pig:
    """ Display piglets, part of a farm 


    This will set up event bindings for changes.

    faster, slower

    larger, smaller

    fewer, more

    next, previous

    compare
    """
    pass


class Yard(pig.Canvas):
    """ A place to draw piglets """
    def __init__(self, parent, *args, **kwargs):

        super().__init__(parent)

        self.scale = 400
        self.fade = 30
        self.sleep = 0.05
        self.naptime = self.sleep
        self.images = {}


        self.add_event_map('s', self.sleepy)
        self.add_event_map('w', self.wakey)
        
        self.add_event_map('d', self.slow_fade)
        self.add_event_map('f', self.fast_fade)

        self.add_event_map('l', self.larger)
        self.add_event_map('k', self.smaller)
        

    async def larger(self):
        """ Larger pictures """
        self.scale += 50

    async def smaller(self):
        """ Smaller pictures """

        self.scale -= 50
        
    async def slow_fade(self):
        """ Fade slower """

        self.fade += 5

    async def fast_fade(self):
        """ Fade faster """

        if self.fade > 5:
            self.fade -= 5

    async def sleepy(self):
        """ sleep more """
        self.sleep += self.naptime

    async def wakey(self):
        """ more awake """
        if self.sleep > self.naptime:
            self.sleep -= self.naptime
        

    def load_image(self, name):

        ximage = self.images.get(name)

        if ximage:
            image, scale = ximage
            if scale == self.scale:
                return image

        image = Image.open(name)

        width, height = image.size

        wscale = width / self.scale

        height /= wscale
        width /= wscale

        print(f'load {width} {height}')
        
        image = image.resize((int(width), int(height))).convert('RGBA')

        # cache image
        self.images[name] = image, self.scale

        return image

class Piglet:
    """ A base piglet class 

    This will provide ways to draw, listen to data, plot, provide data.

    Run tasks.
    """
    pass

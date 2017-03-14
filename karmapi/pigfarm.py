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
from karmapi import piglet

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

            piglet = meta(self.toplevel(), **kwargs)

            self.widgets.append(piglet)

            # let the piglets see the farm
            piglet.farm = self
            print('built', meta, piglet)

            await piglet.start()

    async def start_piglet(self):

        self.current.pack(fill='both', expand=1)
        self.current_task = await curio.spawn(self.current.run())

    async def stop_piglet(self):

        await self.current_task.cancel()
        self.current.pack_forget()

    async def help(self):
        """ Show help """
        print('Help')

        keys = {}
        if self.current:
            keys = self.current.event_map.copy()
            print('current keys:', keys)

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
        
        from karmapi import milk
        farm = PigFarm()
        farm.add(milk.Curio)
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


class Space:

    def __init__(self):

        self.scale = 400
        self.fade = 30
        self.sleep = 0.05
        self.naptime = self.sleep
        self.images = {}
        self.artist = None
        self.event_map = {}


        self.add_event_map('s', self.sleepy)
        self.add_event_map('w', self.wakey)
        
        self.add_event_map('d', self.slow_fade)
        self.add_event_map('f', self.fast_fade)

        self.add_event_map('l', self.larger)
        self.add_event_map('k', self.smaller)

    def add_event_map(self, event, coro):

        self.event_map[event] = coro
        

    def __getattr__(self, attr):
        """ Delegate to artist """
        
        return getattr(self.artist, attr)
        

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


class Yard(Space):
    """ A place to draw piglets """
    def __init__(self, parent, *args, **kwargs):

        super().__init__()

        self.artist = piglet.Canvas(parent)
        

class MagicCarpet(Space):

    def __init__(self, parent=None, axes=None):
        
        super().__init__()

        self.artist = piglet.PlotImage(parent, axes=axes)

        self.log = False
        self.add_event_map('l', self.log_toggle)

        self.clear = True
        self.add_event_map('a', self.clear_toggle)

        self.plot = False
        self.add_event_map('g', self.plot_toggle)

        self.table = False
        self.add_event_map('t', self.table_toggle)

    async def log_toggle(self):
        """ toggle log scale """
        self.log = not self.log

    async def clear_toggle(self):
        """ toggle axes clear """
        self.clear = not self.clear

    async def plot_toggle(self):
        """ toggle plot image """
        self.plot = not self.plot

    async def table_toggle(self):
        """ toggle show table """
        self.table = not self.table



class Docs(piglet.Docs):
    pass
    
    
class Piglet:
    """ A base piglet class 

    This will provide ways to draw, listen to data, plot, provide data.

    Run tasks.
    """
    pass

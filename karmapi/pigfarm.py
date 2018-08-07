""" Pig Farm

A collection of pigs and piglets.

Pigs are windows, piglets are things running in the pig farm.

"""
import pandas   # piglets and pandas together
np = pandas.np
try:

    from pandas.core.indexes.datetimes import DatetimeIndex
except:
    from pandas.tseries.index import DatetimeIndex

from collections import deque
import curio
from curio import spawn, sleep

from pathlib import Path
import inspect

from datetime import datetime

from PIL import Image

from karmapi import hush
from karmapi import piglet
from karmapi import toy

from tkinter import Toplevel

BIGLY_FONT = 'helvetica 20 bold'

class PigFarm:
    """ A pig farm event loop """

    def __init__(self, meta=None, events=None):

        self.event = curio.UniversalQueue()

        self.piglet_event = curio.UniversalQueue()

        self.piglets = curio.UniversalQueue()

        self.builds = curio.UniversalQueue()

        self.data = curio.UniversalQueue()

        self.micks = curio.UniversalQueue()

        self.widgets = deque()
        self.current = None
        self.eric = None

        self.create_event_map()

        from karmapi import piglet

        # this probably needs to be a co-routine?
        self.eloop = piglet.EventLoop()
        self.eloop.set_event_queue(self.event)
        self.eloop.farm = self

        self.piglets.put(self.eloop.run())
        displays = getattr(self.eloop, 'displays', [])
        for output in displays:
            self.piglets.put(output)


    def add_event_map(self, event, coro):

        self.event_map[event] = coro

    def create_event_map(self):

        self.event_map = {}
        self.add_event_map('p', self.previous)
        self.add_event_map('n', self.next)
        self.add_event_map('h', self.help)
        self.add_event_map('c', self.show_monitor)
        self.add_event_map('e', self.show_eric)
        self.add_event_map('q', self.quit)


    def status(self):

        print('builds: ', self.builds.qsize())
        print('piglets::', self.piglets.qsize())
        print('micks:', self.micks.qsize())


    def add(self, pig, kwargs=None):

        kwargs = kwargs or {}
        print('pigfarm adding', pig, kwargs.keys())

        self.builds.put((pig, kwargs))

    def add_mick(self, mick):

        self.micks.put(mick)
        #self.piglets.put(mick.start())

    def toplevel(self):
        """ Return toplevel piglet """
        return self.eloop.app.winfo_toplevel()


    async def build(self):
        """ Do the piglet build """

        while True:
            meta, kwargs = await self.builds.get()
            print('building piglet:', meta, kwargs)

            piglet = meta(self.toplevel(), **kwargs)

            self.widgets.append(piglet)

            # let the piglets see the farm
            piglet.farm = self
            print('built', meta, piglet)

            await piglet.start()

    async def start_piglet(self):

        self.current.pack(fill='both', expand=1)
        self.current_task = await spawn(self.current.run())

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
            msg += '{} {}\n'.format(key,
                                    self.doc_firstline(value.__doc__))

        from karmapi import piglet

        piglet.Help(msg)

    def doc_firstline(self, doc):
        """ Return first line of doc """
        if doc:
            return doc.split('\n')[0]
        else:
            return "????"
        

    async def quit(self):
        """ quit the farm """

        await self.quit_event.set()

    async def next(self):
        """ Show next widget """
        if not len(self.widgets): return
        print('current', self.current)
        if self.current:
            self.widgets.append(self.current)

            await self.stop_piglet()

        self.current = self.widgets.popleft()
        await self.start_piglet()


    async def previous(self):
        """ Show previous widget """
        if not len(self.widgets): return
        print('going to previous', self.current)
        if self.current:

            self.widgets.appendleft(self.current)

            await self.stop_piglet()

        self.current = self.widgets.pop()
        await self.start_piglet()


    async def tend(self):
        """ Make the pigs run """

        # spawn a task for each piglet

        # spawn a task to deal with keyboard events

        # spawn a task to deal with mouse events

        # ... spawn tasks to deal with any events
        print(self.quit_event)
        builder = await curio.spawn(self.build())

        while True:
            while self.piglets.qsize():
                # spawn a task for each piglet
                piglet = await self.piglets.get()

                print('spawning', piglet)

                await spawn(piglet)

            # wait for an event
            #event = await self.event.get()
            #print(self, event)

            # cycle through the widgets
            print()
            #self.next()
            #await curio.sleep(1)

            event = await self.event.get()

            await self.process_event(event)

            #print(event, type(event))

            print('eq', self.event.qsize())


    async def run(self):

        self.quit_event = curio.Event()
        
        runner = await spawn(self.tend())

        await self.quit_event.wait()

        print('over and out')

        await runner.cancel()

        print('runner gone')


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
        await spawn(farm.run())

    async def mon_update(self, mon):

        while True:
            #await mon.update()
            await mon.next()
            await sleep(1)

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

        await spawn(farm.run())

        farm.toplevel().withdraw()
        

def sty(clazz=None, parms={}):
    
    farm = PigFarm()
    
    from karmapi.mclock2 import GuidoClock
    
    farm.add(GuidoClock)

    if clazz:
        farm.add(clazz, parms)

    return farm

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
        self.sleep = 1.0
        self.napcount = 0
        self.naptime = self.sleep
        self.images = {}
        self.artist = None
        self.event_map = {}
        self.event = curio.UniversalQueue()


        self.add_event_map('s', self.sleepy)
        self.add_event_map('w', self.wakey)
        self.add_event_map(' ', self.waity)
        
        self.add_event_map('d', self.slow_fade)
        self.add_event_map('f', self.fast_fade)

        self.add_event_map('l', self.larger)
        self.add_event_map('k', self.smaller)

        self.fix = False
        self.add_event_map('x', self.fix_something)

    def add_event_map(self, event, coro):

        self.event_map[event] = coro
        

    def __getattr__(self, attr):
        """ Delegate to artist """
        return getattr(self.artist, attr)
        
    async def fix_something(self):
        """ Fix """
        self.fix = not self.fix
        
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
        self.napcount += 1
        
        self.sleep += self.naptime * self.napcount
        print(self.sleep, self.naptime, self.napcount)
        
    async def wakey(self):
        """ more awake """
        self.sleep -= self.naptime * self.napcount

        if self.napcount:
            self.napcount -=1

        print(self.sleep, self.naptime, self.napcount)    
        self.sleep = max(self.sleep, 0)
        

    async def waity(self):
        """ pause """
        self.napcount += 20 * 60

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

        print(width, height)
        
        image = image.resize((int(width), int(height))).convert('RGBA')

        # cache image
        self.images[name] = image, self.scale

        return image

    async def load_data(self, data):

        await self.data.put(data)



class Yard(Space):
    """ A place to draw piglets """
    def __init__(self, parent, *args, **kwargs):

        super().__init__()

        self.artist = piglet.Canvas(parent)
        

class PillBox(Space):
    """ A place to draw piglets """
    def __init__(self, parent, *args, **kwargs):

        super().__init__()

        self.artist = piglet.PillBox(parent)


    def grid(self, data, alpha=1.0):
        """ Display data as a grid 
        
        really what matplotlib.imshow does, but on a PIL
        """
        width = self.width
        height = self.height

        rows = len(data)
        cols = len(data[0])

        xx = width / rows
        yy = height / cols

        for row in data:
            for col in row:
                self.rectangle()

        
class MagicCarpet(Space):

    def __init__(self, parent=None, axes=None, data=None,
                 begin=None, end=None, title=None):
        
        super().__init__()

        axes = axes or [211, 212]
        self.artist = piglet.PlotImage(parent, axes=axes)

        self.log = False
        self.add_event_map('l', self.log_toggle)

        self.clear = True
        self.add_event_map('a', self.clear_toggle)

        self.plot = True
        self.add_event_map('g', self.plot_toggle)

        self.table = True
        self.add_event_map('t', self.table_toggle)

        self.subtract_means = False
        self.add_event_map('m', self.subtract_means_toggle)

        self.groups = []
        self.group = None
        self.add_event_map(' ', self.next_group)
        self.add_event_map(';', self.previous_group)


        # set intitial data
        self.title = title
        self.begin = begin
        self.end = end
        data = data or toy.distros(
            trials=1000,
            groups=['abc', 'cde', 'xyz'])


        self.data = data
        self.tests = 0

        if data:
            self.process_data()

            
    def frame_to_stats(self, frame):

        stats = frame.describe()

        ef = pandas.io.formats.format.EngFormatter(1, True)

        cells = []

        for name, col in stats.items():
            cells.append([ef(x) for x in col.values])

        cells = np.array(cells).T

        cols = stats.columns.values
        rows = stats.index.values

        return stats, cells, rows, cols


    async def load_data(self):

        while True:
            self.data = await self.farm.data.get()

            self.process_data()
            
            
    def process_data(self):

        data = self.data
        frames = {}
        groups = []
        for group, frame in data.items():

            frame = pandas.DataFrame(frame)
            print(group)
            frame = pandas.DataFrame(frame)

            sortflag = True
            if 'timestamp' in frame.columns.values:
                print('got timestamp column')
                frame = make_timestamp_index(frame)
                #print(frame.info())
                print(type(frame.index))
                if self.begin or self.end:
                    frame = filter_frame(frame, self.begin, self.end)
                
            if isinstance(frame.index, DatetimeIndex):
                sortflag = False

            frames[group] = dict(frame=frame, sort=sortflag)
            groups.append(group)

        self.frames = frames
        self.group = 0
        self.groups = groups
        

    async def log_toggle(self):
        """ toggle log scale """
        self.log = not self.log
        await self.redraw_group()

    async def clear_toggle(self):
        """ toggle axes clear """
        self.clear = not self.clear

    async def plot_toggle(self):
        """ toggle plot image """
        self.plot = not self.plot
        await self.redraw_group()

    async def table_toggle(self):
        """ toggle show table """
        self.table = not self.table
        await self.redraw_group()

    async def subtract_means_toggle(self):
        """ Toggle mean shifting """
        self.subtract_means = not self.subtract_means
        await self.redraw_group()

    async def next_group(self):
        """ Next group """
        if self.group is None:
            self.process_groups()
            return
        
        self.group += 1

        if self.group == len(self.groups):
            self.group = 0

        await self.redraw_group()

    async def redraw_group(self):
        """ Trigger a redraw of current group """
        await self.event.put(self.group)

    async def previous_group(self):
        """ Previous group """
        if self.group is None:
            return await self.next_group()

        self.group -= 1
        if self.group < 0:
            self.group = len(self.groups) - 1

        await self.redraw_group()
        
    def clear_axes(self):

        for axis in self.subplots:
            axis.clear()

    def clear_figure(self):
        self.fig.clear()


    def draw_table(
            self,
            data=None,
            title=None,
            loc='top',
            bbox=None,
            row_colours=None,
            col_colours=None):
        """ Draw a table on the axes """

        from matplotlib import colors, cm, table
        norm = colors.Normalize()

        stats, cells, rows, cols = self.frame_to_stats(data)

        if self.log:
            print('taking log of colour data')
            import numpy as np
            stats = np.log(stats)
            
        colours = cm.get_cmap()(norm(stats.values))
        alpha = 0.2
        colours[:, :, 3] = alpha

        print(rows)
        print(cols)
        print(len(cells), len(cells[0]))
        

        bbox = (0.0, 0.0, 1.0, 1.0)
        tab = self.axes.table(
            rowLabels=rows,
            rowColours=row_colours,
            colLabels=cols,
            colColours=col_colours,
            cellText=cells,
            cellColours=colours,
            cellEdgeColours=colours,
            bbox=bbox,
            loc=loc)

        acell = tab._cells[0, 0]
        print('fontsize', acell.get_fontsize())

        title = title or 'table location ' + str(loc)
        self.axes.set_title(title)
        self.axes.set_axis_off()


    def draw_plot(self):

        if self.group is None:
            return
        
        group = self.groups[self.group]
        fdata = self.frames[group]
        frame = fdata['frame']
        sortflag = fdata['sort']

        xx = frame.index
        
        axes = self.subplots[0]
        axes.clear()

        if self.title:
            axes.set_title(self.title)

        # sort columns on mean
        mean = frame.mean()
        mean.sort_values(inplace=True)
        frame = frame.ix[:, mean.index]

        # subtract the mean
        if self.subtract_means:
            plot_frame = frame - mean
            plot_frame /= frame.std()
        else:
            plot_frame = frame
        
        col_colours = []
        delta_y = 0
        for label in frame.columns:
        
            data = plot_frame[label].copy()

            if delta_y:
                delta_y += data.std() * 2
                
            if sortflag:
                data.sort_values(inplace=True)
            if self.log:
                patch = axes.semilogy(xx, delta_y + data.values, label=label)
            else:
                patch = axes.plot(xx, delta_y + data.values, label=label)

            col_colours.append(patch[0].get_color())

            if self.subtract_means:
                delta_y += data.std() * 2

        from matplotlib import colors
        col_colours = [colors.to_rgba(x, 0.2) for x in col_colours]

        self.axes = self.subplots[1]
        self.axes.clear()
        self.draw_table(frame, loc='center', title=group, col_colours=col_colours)

        self.select_subplots()

        self.draw()

    def select_subplots(self):
        """ Select what to show """
        plot = self.subplots[0]
        table = self.subplots[1]

        if self.plot and self.table:
            plot.set_visible(True)
            table.set_visible(True)

            plot.change_geometry(2, 1, 1)
            table.change_geometry(2, 1, 2)
            

        if not self.plot:
            plot.set_visible(False)
            table.change_geometry(1, 1, 1)

        if not self.table:
            table.set_visible(False)
            plot.change_geometry(1, 1, 1)

        
    async def run(self):

        await spawn(self.load_data())

        while True:
            self.draw_plot()
            self.group = await self.event.get()

        

class Docs(piglet.Docs):
    pass
    
    
class Piglet:
    """ A base piglet class 

    This will provide ways to draw, listen to data, plot, provide data.

    Run tasks.
    """
    pass

def make_timestamps(data):

    result = {}
    for key, frame in data.items():
        result[key] = make_timestamp_index(frame)

    return result


def make_timestamp_index(frame):
    """ Take a frame with a timestamp column and make it the index """

    print('adding index or not to', frame.columns)
    if not hasattr(frame, 'timestamp'):
        return frame

    print(type(frame.index))
    frame.index = pandas.to_datetime(frame.timestamp, unit='s')
    print(type(frame.index))
    del frame['timestamp']

    return frame

def filter_frame(frame, start, end):
    """ FIXME - looks weird and used f-strings """
    d = start
    #start = f'{d.year}-{d.month:02}-{d.day:02} {d.hour:02}:{d.minute:02}:{d.second:02}'
    d = end
    #end = f'{d.year}-{d.month:02}-{d.day:02} {d.hour:02}:{d.minute:02}:{d.second:02}'

    return frame[start:end]    


def run(farm):
    """  Run a farm """
    curio.run(farm.run(), with_monitor=True)

async def aside(coro):

    print('FIXME coro and args need pickling see curio code')
    return

    curio.aside.main(['pigfarm', filename, coro])

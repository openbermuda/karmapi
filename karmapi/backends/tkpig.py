"""
Pi Gui
"""
import argparse
from collections import defaultdict
from pathlib import Path
import os
import time
import math
import sys
import inspect

from multiprocessing import cpu_count

import curio

# import this early, I like pandas.
import pandas
random = pandas.np.random

import tkinter
from tkinter import Tk, ttk, Text, messagebox

from matplotlib.backends.backend_tkagg import FigureCanvas, FigureManager

from matplotlib.backends.backend_tkagg import (
    NavigationToolbar2TkAgg)

from matplotlib.figure import Figure
from matplotlib import pyplot as plt

from pandas.formats.format import EngFormatter

from ripl import imagefind

from karmapi import base, yosser

from . import core

global APP
global YQ

YQ = curio.Queue()
APP = None

def printf(*args, **kwargs):

    print(*args, flush=True, **kwargs)



def bindings():
    """ Return the bindings between widgets and callbacks """
    return {
        'Run': 'runit'}

def bind(piggy, binds):

    for widget, binding in binds.items():

        try:
            w = piggy[widget]
        except:
            continue

        try:
            cb = getattr(piggy, binding)
        except AttributeError:
            cb = base.get_item(binding)

        w.configure(command=cb)


def get_parser():

    parser = argparse.ArgumentParser()

    # parser.add_argument()

    return parser



class Pig(ttk.Frame, core.Pig):

    def __init__(self, parent, *args):

        ttk.Frame.__init__(self, parent)
        core.Pig.__init__(self, parent)

        print(super(core.Pig, self).__init__)

        # FIXME: bind more events -- or let the Farm worry about that?
        self.bind('<Key>', self.keypress)

        
    def setLayout(self, layout):

        pass

    def setWindowTitle(self, title):

        pass

    def show(self):
        pass


    def keypress(self, event):
        """ Pig keypress event """
        print('PIGKEY', event.keycode)
        
        #FIXME -- probably want a string rather than keycode

        self.event_queue.push(event.keycode)


class Help:

    def __init__(self, msg):

        msg = msg or "Help Me!"
        
        messagebox.showinfo(message=msg)
        

class Docs(Pig):
    """ Docs widget """
    def __init__(self, parent, doc=None):
        """ Initialise the widget 

        doc: optional html text to load the widget with.
        """
        print('Docs', parent)
        super().__init__(parent)

        print(self.event_queue)

        self.text = Text(self)

        VBoxLayout().addWidget(self.text)

        if doc is None:
            doc = "Show docs here"
            
        self.message = doc

    def set_text(self, text):

        self.text.config(state='normal')
        self.text.delete('1.0', 'end')
        self.text.insert('end', text)
        self.text.config(state='disabled')

    
def get_widget(path):

    parts = path.split('.')

    if len(parts) == 1:
        pig_mod = sys.modules[__name__]
        return base.get_item(path, pig_mod)

    return base.get_item(path)
    

class ParmGrid(ttk.Frame):

    def build(self, parms=None, parent=None):

        print('PARMGRID', self)
        parms = parms or {}
        
        for row, item in enumerate(parms):

            label = ttk.Label(self, text=item.get('label'))
            label.grid(row=row, column=0)
            entry = ttk.Entry(self)
            entry.grid(row=row, column=1)

        return self

class button(ttk.Button):

    def __init__(self, parent, meta):
        """ Button factory """
        cb = meta.get('callback')
        if cb:
            if str(cb):
                cb = base.get_item(cb)

        super().__init__(parent, text=meta.get('name', 'Push Me'),
                         command=cb)





class Canvas(Pig):

    
    def __init__(self, parent, gallery=None, **kwargs):

        super().__init__(parent)

        self.width = 400
        self.height = 600

        self.canvas = tkinter.Canvas(self)

        self.gallery = gallery or ['.', '../gallery']


        VBoxLayout().addWidget(self.canvas)


        self.canvas.bind("<Configure>", self.on_configure)


    def set_background(self, colour='black'):

        self.canvas.configure(bg=colour)
    
    def on_configure(self, event):

        print('new bad size:', event.width, event.height)
        self.recalc(event.width, event.height)

    def recalc(self, width, height):

        self.width = width
        self.height = height

        self.canvas.configure(scrollregion=(0, 0, width, height))


    def find_image(self, name):
            
        return imagefind.interpret(dict(galleries=self.gallery, image=name))



    
class PlotImage(Pig):
    """ An image widget

    This is just a wrapper around matplotlib FigureCanvas.
    """
    def __init__(self, parent, width=8, height=8, dpi=100, **kwargs):

        super().__init__(parent)

        fig = Figure(dpi=dpi, **kwargs)
        self.image = FigureCanvas(fig, master=self)
        self.image._tkcanvas.pack(expand=1, fill=tkinter.BOTH)

        #self.toolbar = NavigationToolbar2TkAgg(self.image, self)
        #self.toolbar.update()
        #self.toolbar.pack(expand=0)

        self.axes = fig.add_subplot(111)
        self.fig = fig
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)


    def __getattr__(self, attr):

        return getattr(self.image, attr)


    def compute_data(self):
        """ Over-ride to get whatever data you want to see
        
        """
        #self.data = pandas.np.random.normal(size=(100, 100))
        self.data = pandas.np.random.randint(0,100, size=100)

    def plot(self):
        """ Display an image 

        For example:
        
          t = pandas.np.arange(0.0, 3.0, 0.01)
          s = sin(2*pi*t)
          self.axes.plot(t, s)

        """
        self.axes.plot(self.data)
        #self.axes.imshow(self.data)

    async def run(self):
        
        self.compute_data()
        self.plot()



class KPlot(PlotImage):

    def compute_data(self):

        self.data = [list(range(100)) for x in range(100)]

class XKCD(PlotImage):

    def plot(self):
        """ Display plot xkcd style """
        with plt.xkcd():

            np = pandas.np

            data = np.ones(100)
            data[70:] -= np.arange(30)

            self.axes.plot(data)

            self.axes.annotate(
                'THE DAY I REALIZED\nI COULD COOK BACON\nWHENEVER I WANTED',
                xy=(70, 1), arrowprops=dict(arrowstyle='->'), xytext=(15, -10))

            self.axes.set_xlabel('time')
            self.axes.set_ylabel('my overall health')



class Video(PlotImage):
    """ a video widget

    This is currently a matplotlib FigureCanvas
    """

    def __init__(self, parent):
        super().__init__(parent)

        self.interval = 1
    
    async def run(self):
        """ Run the animation """
        # Loop forever updating the figure, with a little
        # sleeping help from curio
        while True:
            await curio.sleep(self.interval)
            self.update_figure()

    def compute_data(self):

        self.data = pandas.np.random.normal(size=(100, 100))

    def __repr__(self):

        return self.data


    def plot(self):

        self.axes.imshow(self.data)

    def update_figure(self):
        """  Update the figure 

        This just re-computes data and replots.
        """
        self.compute_data()
        self.plot()
        self.draw()


class Table(ttk.Widget):
    """ A table, time for dinner 

    Using QTableView

    The data side of this is in PandasModel below.


    To attach the data just do:

    tab = Table()
    tab.setModel(PandasModel(df))

    If filtering and more is needed there is always this:

    https://gist.github.com/jsexauer/f2bb0cc876828b54f2ed    
    """
    def __init__(self, *args, **kwargs):

        super().__init__()
        self.setSortingEnabled(True)
        self.setAlternatingRowColors(True)
        #self.verticalHeader().setSectionResizeMode(
        #    qtw.QHeaderView.ResizeToContents)        


class VBoxLayout:
    """ Layout widgets in a vertical box """
    def __init__(self, *args):
        pass
    
    def addWidget(self, widget):

        widget.pack(side=tkinter.TOP, expand=1, fill=tkinter.BOTH)

class HBoxLayout:
    """ Layout widgets in a horizontal box """
    def __init__(self, *args):
        pass
    
    def addWidget(self, widget):

        widget.pack(side=tkinter.LEFT, expand=1, fill=tkinter.BOTH)

class GridLayout:        
    """ Layout widgets in a grid """
    def __init__(self, *args):
        self.spacing = 1

    def setSpacing(self, space):

        self.spacing = space
    
    def addWidget(self, widget, row, col):

        widget.grid(row=row, column=col,
                    padx=self.spacing, pady=self.spacing,
                    sticky='nsew')
    

class AppEventLoop:
    """ An event loop

    tk specific application event loop
    """
    def __init__(self, app=None):

        if app is None:
            self.app = Tk()

        self.events = curio.UniversalQueue()
        self.app.bind('<Key>', self.keypress)

    def set_event_queue(self, events):

        self.events = events

    def keypress(self, event):
        """ Just use this to check key events hitting top level """
        print('tk app event loop', event)
        print(event.char, event.keysym, event.keycode)

        self.events.put(event.char)
        
        return True

    async def flush(self):
        """  Wait for an event to arrive in the queue.
        """
        while True:

            event = await self.queue.get()

            self.app.update_idletasks()
            self.app.update()


    async def poll(self):

        # Experiment with sleep to keep gui responsive
        # but not a cpu hog.
        event = 0

        nap = 0.05
        while True:

            # FIXME - have Qt do the put when it wants refreshing
            self.put(event)
            event += 1

            nap = await self.naptime(nap)

            # FIXME should do away with the poll loop and just schedule
            # for some time in the future.
            await curio.sleep(nap)

    async def naptime(self, naptime=None):
        """ Return the time to nap 
        
        FIXME: make this adaptive, but keep it responsive

        The idea would be to see how many events each poll produces.

        So, if there are a lot of events, shorten the naps.

        If there are not so many take a longer nap


        This should take into account how fast events are taking to arrive and
        how long they are taking to process and balance the two.

        And don't sleep too long, in case some other task wakes up and starts talking.

        Better still, might be to have something else managing nap times.

        For now, keep it simple.
        """

        if naptime is None:
            nap = 0.05

        return naptime


class Application(Tk):


    def __init__(self, *args):

        super().__init__()

    def toplevel(self):
        return self

    
class Label(ttk.Label):

    def __init__(self, parent, text=None):


        text = text or 'hello world'
        super().__init__(parent, text=text)


class TabWidget(ttk.Notebook):

    def add_tab(self, name):

        widget = ttk.Frame(self)

        self.add(widget, text=name)

        return widget
        
LineEdit = ttk.Entry        

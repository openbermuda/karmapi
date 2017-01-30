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
from tkinter import Tk, ttk, Text

from matplotlib.backends.backend_tkagg import FigureCanvas, FigureManager

from matplotlib.backends.backend_tkagg import (
    NavigationToolbar2TkAgg)

from matplotlib.figure import Figure
from matplotlib import pyplot as plt

from pandas.formats.format import EngFormatter

from karmapi import base, yosser

from . import core

global APP
global YQ

YQ = curio.Queue()
APP = None

def printf(*args, **kwargs):

    print(*args, flush=True, **kwargs)


def xmeta():
    """ Return description of a pig """
    info = dict(
        title = "PIGS",
        info = dict(foo=27, bar='open'),
        parms = [{'label': 'path'}],
        tabs = [
            {'name': 'curio',
             'widgets': [
                 ["karmapi.widgets.Curio"]]},
                 
            {'name': 'example',
             'widgets': [
                 ["PlotImage", "Video"],
                 ["karmapi.widgets.Circle"],
                 ["Docs", "KPlot"],
                 [{'name': 'Run'}]]},
                 
            {'name': 'perspective',
             'widgets': [["XKCD"]]},
             
            {'name': 'interest',
             'widgets': [
                 ["karmapi.widgets.InfinitySlalom",
                  "karmapi.widgets.InfinitySlalom"]]},
                 
            {'name': 'goals'},
            {'name': 'score'},
            {'name': 'table'},
            {'name': 'yosser'}]) 
    return info

def meta():
    """ Return description of a pig """
    info = dict(
        title = "PIGS",
        info = dict(foo=27, bar='open'),
        parms = [{'label': 'path'}],
        tabs = [
            {'name': 'curio',
             'widgets2': [['PlotImage', 'XKCD']],
             'widgets': [
                 ["karmapi.widgets.Curio"]]},
            {'name': 'curio2'},
            {'name': 'goals'},
            {'name': 'interest',
             'widgets': [
                 ["karmapi.widgets.InfinitySlalom",
                  "karmapi.widgets.InfinitySlalom"]]},
            {'name': 'score'},
            {'name': 'table'},
            {'name': 'yosser'}])
    
    return info


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


    def keyPressEvent(self, event):
        """ Transalte tk keypresses into karma """
        print('key pressed', event)
        

    def setLayout(self, layout):

        pass

    def setWindowTitle(self, title):

        pass

    def show(self):
        pass



class Docs(Text):
    """ Docs widget """
    def __init__(self, parent, doc=None):
        """ Initialise the widget 

        doc: optional html text to load the widget with.
        """
        print('Docs', parent)
        super().__init__(parent)

        if doc is None:
            "Show docs here"
            
        self.text = "<b>hello world</b>"

    def set_text(self, text):

        print(text)
        #self.delete('start', 'end')
        self.insert('end', text)

    def bindkey(self, f):
        from functools import partial
        self.bind('<Key>', partial(self.keypress, cb=f))

    def keypress(self, event, cb):

        print(dir(event))
        print(event.keycode)
        print(event, cb)
        cb(str(event.keycode))
    
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


class Image(ttk.Label):

    def __init__(self, parent, meta=None):

        super().__init__(parent)

        self.setAutoFillBackground(True)
        
        meta = meta or {}

        path = meta.get('path',
                        Path(__file__).parent / 'pig.png')

        p = self.palette()
        image = qtgui.QPixmap(str(path))
        #self.setPixmap(image.scaled(image.width(), image.height(),
        #                            qt.KeepAspectRatio))
        self.setPixmap(image.scaled(self.size(),
                                    qt.KeepAspectRatio,
                                    qt.SmoothTransformation))
        self.setScaledContents(True)
        

class PlotImage(core.Pig, ttk.Frame):
    """ An image widget

    This is just a wrapper around matplotlib FigureCanvas.
    """
    def __init__(self, parent, width=5, height=4, dpi=100, **kwargs):

        super().__init__(parent)

        fig = Figure(figsize=(width, height), dpi=dpi, **kwargs)
        self.image = FigureCanvas(fig, master=self)
        self.image._tkcanvas.pack(expand=1, fill=tkinter.BOTH)

        #self.toolbar = NavigationToolbar2TkAgg(self.image, self)
        #self.toolbar.update()
        #self.toolbar.pack(expand=0)

        self.axes = fig.add_subplot(111)
        self.fig = fig
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)

        self.compute_data()
        self.plot()


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



class ZoomImage(Image):
    pass
        
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

        while True:

            # FIXME - have Qt do the put when it wants refreshing
            self.put(event)
            event += 1

            await curio.sleep(0.05)


def build(recipe, pig=None):


    app = Tk()
    eloop = EventLoop(app)
    
    title = recipe.get('title', 'TkPig')

    if pig is None:
        pig = Pigs(app, recipe, [])
    
    app.title(title)
    #pig.show()
    pig.eloop = eloop

    # need to hang on to a reference to window o/w it gets garbage
    # collected and disappears.
    app.windows = [pig]
    app.pig = pig

    
    app.pig.runners.add(eloop.run())


    return app

class Application(Tk):


    def __init__(self, *args):

        super().__init__()

    def toplevel(self):
        return self

    
class Label(ttk.Label):

    def __init__(self, parent, text):

        super().__init__(parent, text=text)


class TabWidget(ttk.Notebook):

    def add_tab(self, name):

        widget = ttk.Frame(self)

        self.add(widget, text=name)

        return widget
        
LineEdit = ttk.Entry        

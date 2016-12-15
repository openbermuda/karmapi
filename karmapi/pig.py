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

#import qtconsole.mainwindow as qtc

from PyQt5 import QtWidgets as qtw

from PyQt5.QtCore import Qt as qt

from PyQt5 import QtCore as qtcore
from PyQt5 import QtGui as qtgui

from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas)

from matplotlib.backends.backend_qt5agg import (
    NavigationToolbar2QT)

from matplotlib.figure import Figure
from matplotlib import pyplot as plt

from pandas.formats.format import EngFormatter

from karmapi import base, yosser

global APP
global YQ

YQ = curio.Queue()
APP = None

def printf(*args, **kwargs):

    print(*args, flush=True, **kwargs)


def meta():
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

def bindings():
    """ Return the bindings between widgets and callbacks """
    return {
        'Run': 'runit'}

def bind(piggy, binds):

    for widget, binding in binds.items():

        w = piggy[widget]

        try:
            cb = getattr(piggy, binding)
        except AttributeError:
            cb = base.get_item(binding)
        
        w.clicked.connect(cb)


def get_parser():

    parser = argparse.ArgumentParser()

    # parser.add_argument()

    return parser

class Pigs(qtw.QWidget):

    def __init__(self, recipe=None, args=None):

        super().__init__()

        self.meta = recipe or meta()
        self.args = args

        # keep a list of asynchronous tasks needed to run widgets
        self.runners = set()
        self.lookup = {}
        self.build()

    def build(self):

        self.layout = qtw.QVBoxLayout(self)

        widget = self.build_info()
        if widget:
            self.layout.addWidget(widget)
            
        widget = self.build_parms()
        if widget:
            self.layout.addWidget(widget)

        widget = self.build_tabs()
        if widget:
            self.layout.addWidget(widget)

    def build_tabs(self):
        """ Build tabs """

        self.tb = qtw.QTabWidget()
        self.tabs = {}
        for tab in self.meta.get('tabs', []):

            w = qtw.QWidget()

            name = tab['name']
            self.tb.addTab(w, name)

            self.tabs[name] = {}

            widgets = tab.get('widgets')

            if widgets:
                grid = self.build_widgets(widgets, w)
                self.tabs[name] = grid

                self.lookup.update(grid.lookup)

        #self.tb.setCurrentIndex(2)

        return self.tb

    def build_info(self):
        """ Build info """
        pass
    
    def build_parms(self):
        """ Build parms """

        return ParmGrid(self.meta.get('parms', {}))

    def build_widgets(self, widgets, parent=None):

        grid = Grid(widgets, parent)

        for widget in grid.grid.values():
            if hasattr(widget, 'run'):
                self.runners.add(widget.run())

        return grid

    def __getitem__(self, item):

        if item in self.lookup:
            return self.lookup.get(item)

        raise KeyError

    def runit(self):
        
        print('pig runit :)')

        self.eloop.submit_job(doit)
        self.eloop.submit_job(self.doit())

    async def doit(self):
        """  Async callback example for yosser

        See Pig.runit()
        """
        from datetime import datetime
        sleep = random.randint(1, 20)
        printf("running doit doit doit {} {}".format(sleep, datetime.now()))
        start = time.time()
        await curio.sleep(sleep)
        end = time.time()
        printf('actual sleep {} {} {}'.format(
            sleep, end-start, datetime.now()))
        return sleep


    async def run(self):
        """ Make the pig run """
        # spawn task for each runner
        coros = []
        for item in self.runners:
            if inspect.iscoroutine(item):
                coros.append(await(curio.spawn(item)))

        await curio.gather(coros)

def doit():
    """  Callback example for yosser

    See Pig.runit()
    """
    n = random.randint(35, 40)
    start = time.time()
    #time.sleep(sleep)
    sleep = fib(n)
    end = time.time()
    print('actual sleep {} {}'.format(sleep, end-start))
    return n, sleep

def fib(n):
    if n <= 2:
        return 1
    else:
        return fib(n-1) + fib(n-2)

class Widget(qtw.QWidget):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.layout

    def keyPressEvent(self, event):

        print('key pressed', event)

class Text(qtw.QTextEdit):
    """ Text edit widget """
    def __init__(self, meta=None):
        """ Initialise the widget 

        doc: optional html text to load the widget with.
        """

        super().__init__()

        meta = meta or {}


class Docs(qtw.QTextBrowser):
    """ Docs widget """
    def __init__(self, doc=None):
        """ Initialise the widget 

        doc: optional html text to load the widget with.
        """

        super().__init__()

        if doc is None:
            "Show docs here"
            
        self.setHtml("<b>hello world</b>")


class Grid(qtw.QWidget):
    """ A grid of widgets """

    def __init__(self, widgets=None, parent=None):

        super().__init__()

        self.grid = {}
        self.lookup = {}
        self.build(widgets, parent)

    def build(self, widgets, parent):
        
        rows = widgets

        # FIXME create the widget
        vlayout = qtw.QVBoxLayout(parent)
        for irow, row in enumerate(rows):
            wrow = qtw.QWidget()
            vlayout.addWidget(wrow)
            hlayout = qtw.QHBoxLayout(wrow)
            for icol, item in enumerate(row):

                # using isinstance makes me sad..
                # but i will make an exception
                if isinstance(item, str):
                    # assume it is a path to a widget
                    widget = get_widget(item)(None)
                    
                elif isinstance(item, dict):
                    # see if dict specifies the widget
                    widget = item.get('widget', button)

                    if isinstance(widget, str):
                        # maybe it is a path to a widget
                        # eg "karmapi.tankrain.TankRain"
                        widget = get_widget(widget)

                    # build the widget
                    widget = widget(item)

                    # add reference if given one
                    name = item.get('name')
                    if name:
                        self.lookup[name] = widget
                else:
                    widget = item(None)

                self.grid[(irow, icol)] = widget

                hlayout.addWidget(widget)

    def __getitem__(self, item):

        if item in self.lookup:
            return self.lookup.get(item)

        return self.grid.get(item)

def get_widget(path):

    parts = path.split('.')

    if len(parts) == 1:
        pig_mod = sys.modules[__name__]
        return base.get_item(path, pig_mod)

    return base.get_item(path)
    

class ParmGrid(Grid):
    def build(self, parms=None, parent=None):

        layout = qtw.QGridLayout()
        self.setLayout(layout)

        parms = parms or {}
        
        for row, item in enumerate(parms):

            label = qtw.QLabel(item.get('label'))
            layout.addWidget(label, row, 0)
            entry = qtw.QLineEdit()
            layout.addWidget(entry, row, 1)
            

        return self

                
def button(meta):
    """ Button factory """
    b = qtw.QPushButton(meta.get('name', 'Push Me'))

    cb = meta.get('callback')
    if cb:
        if str(cb):
            cb = base.get_item(cb)
        b.clicked.connect(cb)

    return b

class Image(qtw.QLabel):

    def __init__(self, meta=None):

        super().__init__()

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
        

class PlotImage(qtw.QWidget):
    """ An image widget

    This is just a wrapper around matplotlib FigureCanvas.
    """
    def __init__(self, parent=None, width=5, height=4, dpi=100, **kwargs):

        super().__init__()

        fig = Figure(figsize=(width, height), dpi=dpi, **kwargs)
        layout = qtw.QVBoxLayout(self)
        self.image = FigureCanvas(fig)
        layout.addWidget(self.image)

        self.toolbar = NavigationToolbar2QT(self.image, self)
        layout.addWidget(self.toolbar)
        #self.toolbar.hide()

        self.axes = fig.add_subplot(111)
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)

        self.compute_data()
        self.plot()

        self.setParent(parent)

        FigureCanvas.setSizePolicy(self.image,
                                   qtw.QSizePolicy.Expanding,
                                   qtw.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self.image)


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

    def __init__(self, *args, **kwargs):

        super().__init__()

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
    def __init__(self, interval=1, *args, **kwargs):

        super().__init__(**kwargs)
        self.interval = interval or 1

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


class Table(qtw.QTableView):
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


class PandasModel(qtcore.QAbstractTableModel):
    def __init__(self, data, parent=None):
        qtcore.QAbstractTableModel.__init__(self, parent)
        self._data = data
        self.formatter = EngFormatter(accuracy=0, use_eng_prefix=True)

    def rowCount(self, parent=None):
        return len(self._data.values)

    def columnCount(self, parent=None):
        return self._data.columns.size

    def data(self, index, role=qt.DisplayRole):
        if index.isValid():
            if role == qt.DisplayRole:
                data = self._data.values[index.row()][index.column()]
                try:
                    # format data with formatter function
                    value = self.formatter(data)
                except:
                    # anything goes wrong, just show with str
                    value = str(data)
                return qtcore.QVariant(value)
        return qtcore.QVariant()


    def headerData(self, section, orientation, role):
        """ Return header for given column """
        if role == qt.DisplayRole and orientation == qt.Horizontal:

            return self._data.columns.values[section]

        return qtcore.QAbstractTableModel.headerData(
            self, section, orientation, role)

    def sort(self, ncol, order):
        """Sort table by given column number. """
        self.layoutAboutToBeChanged.emit()

        self._data.sort_values(by=self._data.columns[ncol], 
                               ascending=order == qt.AscendingOrder,
                               inplace=True)
        
        self.layoutChanged.emit()


class EventLoop:
    """ An event loop

    For now, this is just here to make a Qt app run
    under curio,

    For now it has two tasks.

    flush:  wait for an event, then process it

    poll: periodically tests if the app has pending events


    FIXME: add a magic task that magically knows when there
           are events pending without having to poll.

           Somewhere in the depths of Qt there has to be an
           event queue.  If that code can be fixed to let
           this event loop know when the queue is not empty
           then we'd have magic.

           somewhere there is a magic file or socket?
    """

    def __init__(self, app=None):

        self.app = app
        
        self.queue = curio.Queue()

        self.event_loop = qtcore.QEventLoop()


    def put(self, event):
        """ Maybe EventLoop is just a curio.EpicQueue? """
        self.queue.put(event)

        
    async def flush(self):
        """  Wait for an event to arrive in the queue.
        """
        while True:

            event = await self.queue.get()

            self.event_loop.processEvents()
            self.app.sendPostedEvents(None, 0)


    async def poll(self, yq):

        # Experiment with sleep to keep gui responsive
        # but not a cpu hog.
        event = 0

        while True:

            if self.app.hasPendingEvents():

                # FIXME - have Qt do the put when it wants refreshing
                self.put(event)
                event += 1

            await curio.sleep(0.05)

    def submit_job(self, coro):
        """ Submit a coroutine to the job queue """
        self.yq.put(coro)

    async def yosser(self, yq):

        self.yq = yq
        while True:
            job = await yq.get()

            print('yay!! yosser got a job {}'.format(job))

            start = time.time()
            # fixme: want curio run for
            if inspect.iscoroutine(job):
                result = await job
            else:
                result = await curio.run_in_process(job)
            end = time.time()

            print("doit slept for {} {}".format(result, end-start))
            

    def magic(self, event, *args, **kwargs):
        """ Gets called when magic is needed """
        printf('magic', flush=True)
        self.put(event)


    async def run(self):

        poll_task = await curio.spawn(self.poll(YQ))

        flush_task = await curio.spawn(self.flush())

        yosser_tasks = []
        for yosser in range(cpu_count()):
        
            yosser_tasks.append(await curio.spawn(self.yosser(YQ)))

        tasks = [flush_task, poll_task] +  yosser_tasks

        await curio.gather(tasks)



def build(recipe, pig=None):


    app = qtw.QApplication([])
    eloop = EventLoop(app)
    
    title = recipe.get('title', app.applicationName())

    if pig is None:
        pig = Pigs(recipe, app.arguments()[1:])
    
    pig.setWindowTitle(title)
    pig.show()
    pig.eloop = eloop

    # need to hang on to a reference to window o/w it gets garbage
    # collected and disappears.
    app.windows = [pig]
    app.pig = pig

    
    app.pig.runners.add(eloop.run())


    return app

def win_curio_fix():
    """ Kludge alert 

    On windows, select.select() with three empty sets throws an exception.

    On Linux, select.select() sleeps and waits for something to appear.

    This adds dummy read socket to the selector and so ensures it never 
    gets called with three empty sets.

    Just pass it into curio.run(...., selector=win_curio_fix())
    """
    
    import selectors
    import socket

    dummy_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    selector = selectors.DefaultSelector()
    selector.register(dummy_socket, selectors.EVENT_READ)

    return selector

def run(app):

    # add qt event loop to the curio tasks

    selector = win_curio_fix()
    curio.run(app.pig.run(), with_monitor=True, selector=selector)



def print_thread_info(name):
    import threading
    print()
    print(name)
    print(globals().keys())
    print(locals().keys())
    print(threading.current_thread())
    print(threading.active_count())
    print('YQ:', YQ.qsize())


    

if __name__ == '__main__':

    # Let curio bring this to life
    print('build pig')
    
    APP = build(meta())

    # apply bindings
    bind(APP.pig, bindings())

    print('make pig run')
    run(APP)


    

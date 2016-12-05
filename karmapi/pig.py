"""
Pi Gui
"""
import argparse
from collections import defaultdict
from pathlib import Path

import sys

import curio

# import this early, I like pandas.
import pandas
random = pandas.np.random

import qtconsole.mainwindow as qtc

from PyQt5 import QtWidgets as qtw

from PyQt5.QtCore import Qt as qt

from PyQt5 import QtCore as qtcore

from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas)

from matplotlib.figure import Figure
from pandas.formats.format import EngFormatter

from karmapi import base, yosser

def printf(*args, **kwargs):

    print(*args, flush=True, **kwargs)

def meta():
    """ Return description of a pig """
    info = dict(
        title = "PIGS",
        info = dict(foo=27, bar='open'),
        parms = ['path'],
        tabs = [
            {'name': 'example',
             'widgets': [[Image, Video], [Docs, KPlot],
                         [{'name': 'Run', 'callback': hello}]]},
            {'name': 'perspective'},
            {'name': 'interest'},
            {'name': 'goals'},
            {'name': 'score'},
            {'name': 'table'},
            {'name': 'yosser'}]) 
    return info

def hello():
    print('hello')

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
        self.runners = []
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
        self.tabs = []
        for tab in self.meta.get('tabs', []):
            printf(tab)

            w = qtw.QWidget()
            self.tabs.append(w)
            
            self.tb.addTab(w, tab['name'])

            widgets = tab.get('widgets')

            if widgets:
                self.build_widgets(widgets, w)

        return self.tb

    def build_info(self):
        """ Build info """
        pass
    
    def build_parms(self):
        """ Build parms

        Use arg parser to get at args
        """
        parser = get_parser()
        args = parser.parse_args(self.args)

        # Now just need to loop round the args
        # and display the values:  K:   VALUE


    def build_widgets(self, widgets, parent=None):

        grid = Grid(widgets, parent)

        return grid

    
class Console(qtc.MainWindow):
    """ A console widget

    This just needs to wrap qtconsole.
    """
    pass

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
        
        if widgets is None:
            rows = [[Plotter, Table], [Docs, Console]]
            rows = [[Console, Console], [Console, Console]]
            rows = [[Image, Image]]
            rows = [[Table, Table]]
            rows = [[KPlot, Video]]
        else:
            rows = widgets

        # FIXME create the widget
        vlayout = qtw.QVBoxLayout(parent)
        for row in rows:
            print(row)
            wrow = qtw.QWidget()
            vlayout.addWidget(wrow)
            hlayout = qtw.QHBoxLayout(wrow)
            for item in row:
                printf(item)

                # using isinstance makes me sad.. but i will make an exception
                if isinstance(item, dict):
                    widget = button(item)
                else:
                    widget = item(None)



                hlayout.addWidget(widget)


def button(meta):
    """ Button factory """
    b = qtw.QPushButton(meta.get('name', 'Push Me'))

    cb = meta.get('callback')
    if cb:
        b.clicked.connect(cb)

    return b
                
class Image(FigureCanvas):
    """ An image widget

    This is just a wrapper around matplotlib FigureCanvas.
    """
    def __init__(self, parent=None, width=5, height=4, dpi=100):

        fig = Figure(figsize=(width, height), dpi=dpi)
        super().__init__(fig)

        self.axes = fig.add_subplot(111)
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)

                
        self.compute_data()
        self.plot()
        #
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   qtw.QSizePolicy.Expanding,
                                   qtw.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


    def compute_data(self):
        """ Over-ride to get whatever data you want to see
        
        """
        self.data = pandas.np.random.normal(size=(100, 100))

    def plot(self):
        """ Display an image 

        For example:
        
          t = arange(0.0, 3.0, 0.01)
          s = sin(2*pi*t)
          self.axes.plot(t, s)

        """
        self.axes.imshow(self.data)
        
class KPlot(Image):

    def compute_data(self):

        self.data = [list(range(100)) for x in range(100)]
        

class ZoomImage(Image):
    pass
        
class Video(Image):
    """ a video widget 

    This is currently a matplotlib FigureCanvas
    """
    def __init__(self, interval=1, *args, **kwargs):
        super().__init__()
        self.interval = interval or 1

        timer = qtcore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(1000)
        
    async def xrun(self):
        """ Run the animation """
        # Loop forever updating the figure, with a little
        # sleeping help from curio
        while True:
            await curio.sleep(self.interval)
            self.update_figure()

    def compute_data(self):

        self.data = pandas.np.random.normal(size=(100, 100))
        #self.n = 4
        #self.k = 20
        #self.data = [random.randint(0, self.n) for i in range(self.n)]

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
        #self.verticalHeader().setResizeMode(
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


class PiWidget(qtw.QWidget):

    def __init__(self, recipe):

        super().__init__()
        
        self.recipe = recipe

    def build(self):

        layout = QVBoxLayout(self)

        build(self.recipe, layout)

        return


async def qt_app_runner(app):

    # FIXME -- without yosser nothing works
    # may be a windows thing select([], [], []) on windows
    # doesn't block, instead throws an error.
    printf('spawn yosser')

    yoss = await curio.spawn(curio.tcp_server(
        '', 2469, yosser.yosser_handler))
      
    event_loop = await curio.spawn(qtloop(app))

    print('event loop running')
    await event_loop.join()



async def qtloop(app):

    event_loop = qtcore.QEventLoop()

    while True:
        #for win in app.allWindows():
        #    win.show()
        event_loop.processEvents()
        app.sendPostedEvents(None, 0)

        # Experiment with sleep to keep gui responsive
        # but not a cpu hog.
        await curio.sleep(0.05)
    

def build(recipe):


    app = qtw.QApplication([])

    
    title = recipe.get('title', app.applicationName())
    
    window = Pigs(recipe, app.arguments()[1:])
    #window = qtw.QProgressBar()
    #window.setRange(0, 99)

    #window.setWindowTitle(title)
    window.show()

    # need to hang on to a reference to window o/w it gets garbage
    # collected and disappears.
    app.windows = [window]

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

    selector = win_curio_fix()

    curio.run(qt_app_runner(app), with_monitor=True, selector=selector)
    

if __name__ == '__main__':

    # Let curio bring this to life
    app = build(meta())
    run(app)


    

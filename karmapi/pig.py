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

from karmapi import base

from karmapi.embedding_in_qt4 import MyStaticMplCanvas, MyDynamicMplCanvas

def meta():
    """ Return description of a pig """
    info = dict(
        title = "PIGS",
        info = dict(foo=27, bar='open'),
        parms = ['path'],
        tabs = ['perspective', "interest", "goals",
                "score", "table", "yosser"])
        
    return info

def get_parser():

    parser = argparse.ArgumentParser()

    # parser.add_argument()

    return parser

class Pigs(qtw.QWidget):

    def __init__(self, recipe=None, args=None):

        super().__init__()
        self.meta = recipe or meta()
        self.args = args
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
            print(tab)

            w = qtw.QWidget()
            self.tabs.append(w)
            
            self.tb.addTab(w, tab)

            # FIXME recurse?
            target = 'build_{}'.format(tab)

            if hasattr(self, target):
                getattr(self, target)(w)

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


    def build_yosser(self, parent=None):

        return Yosser(parent)

    
class Plotter:
    """ A plot widget 

    FIXME: this just needs to wrap matplotlib qt viewer.

    more generally, ipywidgets might be worth a look.
    """
    pass

class Console(qtc.MainWindow):
    """ A console widget

    This just needs to wrap qtconsole.
    """
    pass

class Data:
    """ Data widget """
    pass

class Docs:
    """ Docs widget """
    pass


class Yosser(qtw.QWidget):
    """ A builder widget 


    more generally, ipywidgets might be worth a look.
    """

    def __init__(self, parent=None):

        super().__init__()
        
        rows = [[Plotter, Data], [Docs, Console]]
        rows = [[Console, Console], [Console, Console]]
        rows = [[Image, Video]]

        # FIXME create the widget
        vlayout = qtw.QVBoxLayout(parent)
        for row in rows:
            wrow = qtw.QWidget()
            vlayout.addWidget(wrow)
            hlayout = qtw.QHBoxLayout(wrow)
            for item in row:
                print(item)
                widget = item(None)
                hlayout.addWidget(widget)

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
        


class Video(Image):
    """ a video widget 

    This is currently a matplotlib FigureCanvas
    """
    def __init__(self, interval=1, *args, **kwargs):
        super().__init__()

        curio.spawn(self.run)

    async def run(self):
        # Loop forever updating the figure, with a little
        # sleeping help from curio
        while True:
            await curio.sleep(interval)
            self.update_figure()

    def compute_data(self):

        self.n = 4
        self.k = 20
        self.data = [random.randint(0, self.n) for i in range(self.n)]

    def __repr__(self):

        return self.data


    def plot(self):

        self.axes.plot(self.data)

    def update_figure(self):
        # Build a list of 4 random integers
        # between 0 and 10 (both inclusive)
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
    def __init__(self):

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
                # FIXME -- format this pretty
                data = self._data.values[index.row()][index.column()]
                try:
                    value = self.formatter(data)
                except:
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




def build(recipe, parent=None, row=True):

    if parent is None:
        parent = QVBoxLayout()

    for item in recipe:

        if isinstance(item, dict):
            parent.addWidget(build_widget(item))

        else:
            if row:
                layout = QHBoxLayout(window)
            else:
                layout = QVBoxLayout(window)

            parent.addWidget(window)

            build(item, layout, not row)

    return parent

def build_widget(item):

    return QLabel(item.get(name, 'noname'))


class PiWidget(qtw.QWidget):

    def __init__(self, recipe):

        super().__init__()
        
        self.recipe = recipe

    def build(self):

        layout = QVBoxLayout(self)

        build(self.recipe, layout)

        return


async def qtloop(app):

    event_loop = qtcore.QEventLoop()

    while True:
        event_loop.processEvents()
        app.sendPostedEvents(None, 0)

        # Experiment with sleep to keep gui responsive
        # but not a cpu hog.
        await curio.sleep(0.05)
    

def build(recipe):


    print(sys.argv)
    app = qtw.QApplication(sys.argv)

    
    title = recipe.get('title', app.applicationName())
    
    window = Pigs(recipe, app.arguments()[1:])
    window.setWindowTitle(title)
    window.show()

    return app


if __name__ == '__main__':

    # Let curio bring this to life
    curio.run(qtloop(build(meta())))

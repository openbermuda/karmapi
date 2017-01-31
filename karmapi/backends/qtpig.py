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


def printf(*args, **kwargs):

    print(*args, flush=True, **kwargs)

def bind(piggy, binds):

    for widget, binding in binds.items():

        w = piggy[widget]

        try:
            cb = getattr(piggy, binding)
        except AttributeError:
            cb = base.get_item(binding)
        
        w.clicked.connect(cb)


class Pig(qtw.QWidget):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.layout

    def keyPressEvent(self, event):

        print('key pressed', event)



class Text(qtw.QTextEdit):
    """ Text edit widget """
    def __init__(self, parent, meta=None):
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

    def set_text(self, text):
        
        self.setHtml('<pre>' + text + '</pre>')

    def bindkey(self, f):

        pass


class HeaderLabel(qtw.QLabel):

    def __init__(self, name=None):

        name = name or ''
        
        super().__init__(name)
            
        self.setStyleSheet('background: #ff00ff')
        self.setAlignment(qt.AlignCenter)
        self.setMargin(5)

    def set_text(self, text):

        self.setText(text)

class GridLabel(qtw.QLabel):

    def __init__(self, name=None):

        name = name or ''
        
        super().__init__(name)
            
        #label.setStyleSheet('border: 1px solid black;')
        self.setStyleSheet('background: #eeeeee')
        self.setAlignment(qt.AlignRight)
        self.setMargin(5)
        self.font().setPointSize(10)


    def set_text(self, text):

        self.setText(text)
    
                    

def button(parent, meta):
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
        self.fig = fig
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
        


class Table(qtw.QTableView):
    """ A table, time for dinner 

    Using QTableView

    The data side of this is in PandasModel below.


    To attach the data just do:

    tab = Table()
    tab.load(df))

    If filtering and more is needed there is always this:

    https://gist.github.com/jsexauer/f2bb0cc876828b54f2ed 
    """
    def __init__(self, *args, **kwargs):

        super().__init__()
        self.setSortingEnabled(True)
        self.setAlternatingRowColors(True)

        if not hasattr(self, 'header'):
            self.header = self.horizontalHeader

        header = self.header()

        # make table autoresize
        header.setSectionResizeMode(qtw.QHeaderView.ResizeToContents)

        # tell it to just use 50 rows to do the sizing, otherewise it
        # gets painfully slow.
        header.setResizeContentsPrecision(50)
        #self.setUniformRowHeights(True)

        self.filter_model = FilterModel()
        self.setModel(self.filter_model)


    def keyPressEvent(self, event):
        """ If keypress is a return then filter on current value """
        key = event.key()

        if key != qtcore.Qt.Key_Return:
            return super().keyPressEvent(event)
        
        ix = self.currentIndex()
        data = self.model().itemData(ix)

        if data:
            text = data[0]
            self.toggle_filter(ix.column(), text)
        else:
            self.remove_filter()
        
        return super().keyPressEvent(event)

    def toggle_filter(self, column, text):
        """ Toggle filtering """
        self.filter_model.modelAboutToBeReset.emit()
        model = self.model()
        text = qtcore.QRegExp('^' + text + '$')
        if model.filterRegExp() == text and model.filterKeyColumn() == column:
            self.remove_filter()
        else:
            model.setFilterKeyColumn(column)
            model.setFilterRegExp(text)
        self.filter_model.modelReset.emit()
            
    def remove_filter(self):
        self.filter_model.setFilterRegExp('')

    def load(self, df):
        """ Load a dataframe into the table """
        self.hide()
        self.df = df
        header = self.header()
        #header.setSectionResizeMode(qtw.QHeaderView.ResizeToContents)
        self.filter_model.modelAboutToBeReset.emit()
        self.remove_filter()
        source = PandasModel(df)
        self.filter_model.setSourceModel(source)
        #self.filter_model.sort = source.sort
        self.filter_model.modelReset.emit()

        #header.setSectionResizeMode(qtw.QHeaderView.Fixed)
        self.show()

    def contextMenuEvent(self, event):
        """Implements right-clicking on cell.

        NOTE: You probably want to overrite make_cell_context_menu, not this
        function, when subclassing.
        """
        row_ix = self.rowAt(event.y())
        col_ix = self.columnAt(event.x())

        if row_ix < 0 or col_ix < 0:
            return #out of bounds

        menu = qtw.QMenu(self)
        menu.addAction("Open in Excel",
                       self._to_excel)

        menu.exec_(self.mapToGlobal(event.pos()))

    def _to_excel(self):
        from subprocess import Popen
        self.df.to_excel('temp.xls')
        Popen('temp.xls', shell=True)
        
class PandasModel(qtcore.QAbstractTableModel):
    ROW_BATCH_COUNT = 50
    
    def __init__(self, data, parent=None):
        qtcore.QAbstractTableModel.__init__(self, parent)
        self._data = data
        self.formatter = EngFormatter(accuracy=0, use_eng_prefix=True)

        self.rows_loaded = self.ROW_BATCH_COUNT

    def rowCount(self, parent=None):

        if len(self._data) < self.rows_loaded:
            return len(self._data)
        
        return self.rows_loaded

    def canFetchMore(self, index=None):

        if index:
            print('canfetchmore', index.row())
        print('canfetchmore', self.rows_loaded, flush=True)
        return self.rows_loaded < len(self._data)

    def fetchMore(self, index=None):

        print('fetching more', self.rows_loaded, flush=True)
        remainder = len(self._data) - self.rows_loaded

        items_to_fetch = min(remainder, self.ROW_BATCH_COUNT)

        self.beginInsertRows(qtcore.QModelIndex(), self.rows_loaded,
                             self.rows_loaded + items_to_fetch - 1)
        self.rows_loaded += items_to_fetch
        self.endInsertRows()

    def columnCount(self, parent=None):
        return self._data.columns.size

    def data(self, index, role=qt.DisplayRole):

        #print('data', len(self._data), index.row(), flush=True)
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
        printf('sorting', ncol, order)
        self.layoutAboutToBeChanged.emit()

        data = self._data
        data.head(self.rows_loaded).sort_values(
            by=data.columns[ncol], 
            ascending=order == qt.AscendingOrder,
            inplace=True)
        
        self.layoutChanged.emit()


class FilterModel(qtcore.QSortFilterProxyModel):
    
    def sort(self, ncol, order):
        """Sort table by given column number. """
        printf('sorting filtermodel', ncol, order)
        return self.sourceModel().sort(ncol, order)


class AppEventLoop:
    """ An event loop
    
    Qt specific event loop base
    """

    def __init__(self):

        self.event_loop = qtcore.QEventLoop()

    async def flush(self):
        """  Wait for an event to arrive in the queue.
        """
        while True:

            event = await self.queue.get()

            self.event_loop.processEvents()
            self.app.sendPostedEvents(None, 0)


    async def poll(self):

        # Experiment with sleep to keep gui responsive
        # but not a cpu hog.
        event = 0

        while True:

            if self.app.hasPendingEvents():

                # FIXME - have Qt do the put when it wants refreshing
                self.put(event)
                event += 1

            await curio.sleep(0.05)

class Label(qtw.QLabel):

    def __init__(self, parent, text=None):

        super().__init__(parent)
        self.setText(text)
            
class TabWidget(qtw.QTabWidget):

    def add_tab(self, name):
        """ Add a tab and return widget to hold contents of tab """
        w = Pig(self)

        self.addTab(w, name)

        return w

    
class Application(qtw.QApplication):

    def __init__(self, *args):

        super().__init__(*args)

        self.top = qtw.QFrame()
        self.top.show()

    def toplevel(self):

        return self.top
    
HBoxLayout = qtw.QHBoxLayout
VBoxLayout = qtw.QVBoxLayout
GridLayout = qtw.QGridLayout
LineEdit = qtw.QLineEdit




    

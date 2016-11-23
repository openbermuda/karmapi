"""
Pi Gui
"""
import argparse
from collections import defaultdict
from pathlib import Path

import sys

import qtconsole.mainwindow as qtc

from PyQt5 import QtWidgets as qtw

from PyQt5.QtCore import Qt as qt

from PyQt5.QtWidgets  import (
    QApplication, QWidget, QLabel, QLineEdit, QTextEdit,
    QGridLayout, QBoxLayout, QHBoxLayout, QVBoxLayout)

from karmapi import base

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

        # FIXME create the widget
        vlayout = qtw.QVBoxLayout(parent)
        for row in rows:
            wrow = qtw.QWidget()
            vlayout.addWidget(wrow)
            hlayout = qtw.QHBoxLayout(wrow)
            for item in row:
                print(item)
                hlayout.addWidget(item(None))


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


class PiWidget(QWidget):

    def __init__(self, recipe):

        super().__init__()
        
        self.recipe = recipe

    def build(self):

        layout = QVBoxLayout(self)

        build(self.recipe, layout)

        return


def run(recipe):


    print(sys.argv)
    app = QApplication(sys.argv)

    
    title = recipe.get('title', app.applicationName())
    
    window = Pigs(recipe, app.arguments()[1:])
    window.setWindowTitle(title)
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':

    run(meta())

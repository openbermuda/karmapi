"""
Pi Gui
"""
import argparse
from collections import defaultdict
from pathlib import Path

from karmapi import base

import sys
from PyQt5 import QtWidgets as qtw

from PyQt5.QtCore import Qt as qt

from PyQt5.QtWidgets  import (
    QApplication, QWidget, QLabel, QLineEdit, QTextEdit,
    QGridLayout, QBoxLayout, QHBoxLayout, QVBoxLayout)

def meta():
    """ Return description of a pig """
    info = dict(
        title = "PIGS",
        info = dict(foo=27, bar='open'),
        parms = ['path'],
        tabs = ['perspective', "interest", "goals", "score", "table"])
        
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

        self.tb = qtw.QTabBar()
        for tab in self.meta.get('tabs', []):
            w = self.tb.addTab(tab)
            # FIXME recurse?

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
        

    
class Plotter:
    """ A plot widget 

    FIXME: this just needs to wrap matplotlib qt viewer.

    more generally, ipywidgets might be worth a look.
    """
    pass

class Console:
    """ A console widget

    FIXME: this just needs to wrap qtconsole.
    """
    pass
    


def hello():

    app = QApplication(sys.argv) #ignore()
    window = QWidget()
    window.setWindowTitle("Hello World")
    window.show()

    # [Add widgets to the widget]

    # Create some widgets (these won't appear immediately):
    nameLabel = QLabel("Name:")
    nameEdit = QLineEdit()
    addressLabel = QLabel("Address:")
    addressEdit = QTextEdit()

    # Put the widgets in a layout (now they start to appear):
    layout = QGridLayout(window)
    layout.addWidget(nameLabel, 0, 0)
    layout.addWidget(nameEdit, 0, 1)
    layout.addWidget(addressLabel, 1, 0)
    layout.addWidget(addressEdit, 1, 1)
    layout.setRowStretch(2, 1)

    # [Resizing the window]

    # Let's resize the window:
    window.resize(480, 160)

    # The widgets are managed by the layout...
    window.resize(320, 180)

    # [Run the application]

    # Start the event loop...
    sys.exit(app.exec_())

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

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

from concurrent.futures import ProcessPoolExecutor

import curio

# import this early, I like pandas.
import pandas
random = pandas.np.random

from karmapi import base, yosser

global APP

from karmapi.piglet import (
    # widgetw
    Pigs, Text, Docs, Grid, ParmGrid, GridBase, Canvas,
    LabelGrid, Image, PlotImage, KPlot, XKCD, Video,
    Table, EventLoop, Application, Piglet, TabWidget,
    GridLayout, VBoxLayout, HBoxLayout)

APP = None

BIGLY_FONT = 'helvetica 20 bold'


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
    selector = None
    curio.run(app.pig.run(), with_monitor=True, selector=selector)




def build(recipe, pig=None):


    app = Application([])
    eloop = EventLoop(app)
    
    title = recipe.get('title', 'PIGS')

    layout = VBoxLayout(app.toplevel())
    if pig is None:
        pig = Pigs(app, recipe)
        layout.addWidget(pig)
    
    pig.setWindowTitle(title)
    pig.show()
    pig.eloop = eloop

    # need to hang on to a reference to window o/w it gets garbage
    # collected and disappears.
    app.windows = [pig]
    app.pig = pig

    
    app.pig.runners.add(eloop.run())


    return app
    


    

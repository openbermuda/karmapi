"""
Widgets for pig
"""

#from qtconsole import jupyter_widget


#class Jupyter(jupyter_widget.JupyterWidget):
#    pass

from numpy import random

from karmapi import pig

class Friday(pig.Video):


    def compute_data(self):

        #self.data = random.randint(0, 100, size=100)
        self.data = list(range(100))

    def plot(self):

        self.axes.plot(self.data)

"""
Stuff to do with time.
"""

from collections import Counter

import pandas
from matplotlib import pyplot
from mpl_toolkits import basemap

from karmapi.weather import Location

def day_plot(dates):
    """ Plot day distributions """
    vc = dates.value_counts()

    data = [x for x in vc.items()]
    data.sort()

    pyplot.plot([x[0] for x in data], [y[1] for y in data])
    
    return data


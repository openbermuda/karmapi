from karmapi import pig

import curio
import random

from pathlib import Path

class Sunspot(pig.Video):


    def compute_data(self):

        pass


    def plot(self):

        jup = 11.86
        nep = 164.8
        sat = 29.4571

        x = (1/jup - 1/sat)

        jupsat = 1/(2 * x)

        x = (1/jup - 1/nep)
        jupnep = 1/(2 * x)

        jupsat, jupnep


        period = [jupsat, 10.87, jup, 11.07]

        phase = [2000.475, 2002.364, 1999.381, 2009]

        weight = [0.83, 1.0, 0.55, 0.25]

        import datetime
        import pandas
        import math

        from karmapi import base

        infile = Path('~/devel/karmapi/notebooks/SN_m_tot_V2.0.csv').expanduser()
        
        df = pandas.read_csv(
            infile, 
            names=['year', 'month', 'time', 'sunspot', 'sd', 'status'], 
            sep=';',
            header=None,
            index_col=False)

        def add_date(x):
    
            # FIXME -- turn time into day
            return datetime.date(int(x.year), int(x.month), 1)

        
        df.index = df.apply(add_date, axis=1)

        df.index = pandas.date_range(
            datetime.date(int(df.index[0].year), int(df.index[0].month), 1), 
            periods=len(df), freq='M')


        df['year2'] = pandas.np.linspace(1749, 2016.67, 3212)


        pi = math.pi
        cos = pandas.np.cos
        for ii in range(4):
    
            df['h{}'.format(ii + 1)] = weight[ii] * cos((2 * pi) * ((df.year2 - phase[ii]) / period[ii]))
    
        df['model'] = df.h1 + df.h2 + df.h3 + df.h4



        df['guess'] = df.model.clip_lower(0.0) * 150


        self.axes.hold(True)
        self.axes.plot(df['guess'] / 2.0, 'b')

        self.axes.plot((df.h3 * 20) -10, 'g')
        self.axes.plot((df.h2 * 20) -40,'k')
        self.axes.plot((df.sunspot / 2) + 100,'r')



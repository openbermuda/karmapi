from datetime import datetime

import PIL

from collections import deque

from karmapi import pigfarm
from karmapi import base
from karmapi import hush
import curio

import pandas
np = pandas.np

from matplotlib import ticker
from matplotlib.mlab import PCA

from numpy import random

import math

PI = math.pi


class SonoGram(pigfarm.MagicCarpet):

    def __init__(self, parent):

        super().__init__(parent)

        self.plottype = 'wave'

        self.data = deque()

        self.create_event_map()
        self.samples = 1
        self.channel = 0
        #self.sleep = 0.1

        # power spectrum so log may work better
        self.log = True

        # fix sonogram scale
        self.vmax = None
        self.vmin = None


    def create_event_map(self):

        self.add_event_map('d', self.down)
        self.add_event_map('u', self.up)
        self.add_event_map('w', self.wide)
        self.add_event_map('i', self.slim)
        self.add_event_map('t', self.toggle_plottype)
        self.add_event_map('c', self.toggle_channel)
        self.add_event_map('m', self.next_mick)

        self.pca = None
        self.add_event_map('M',  self.do_principal_components)

    async def toggle_plottype(self):
        """ Toggle between wave and sonogram """

        if self.plottype != 'sono':
            self.plottype = 'sono'
        else:
            self.plottype = 'wave'

    async def down(self):
        """ Increase offset  """
        self.offset += 1
        self.end += 1

    async def up(self):
        """ Decrease offset """

        self.offset -= 1
        self.end -= 1

    async def slim(self):
        """ Shrink frequency window """

        self.end -= 5

    async def wide(self):
        """ Widen frequency window """

        self.end += 5

    async def toggle_channel(self):
        """ Toggle channel """

        if self.channel:
            self.channel = 0
        else:
            self.channel = 1


    def plot(self):
        pass

    async def get_source(self):
        return await self.farm.micks.get()

    def sono_calc(self, data):

        nn = int(len(data) / 2)

        start = nn * self.channel
        end = start + nn

        return base.fft.fft(data[start:end])


    async def next_mick(self):
        """ Move to next mick source """
        await self.farm.micks.put(self.mick)

        self.mick = await self.get_source()


    async def read(self):


        # need to fire up the frames co-routine?
        while True:

            data = await self.mick.get()

            self.data.append(data)

            while len(self.data) > 100:
                self.data.popleft()


    async def start(self):

        self.farm.status()
        self.mick = await self.get_source()

    async def do_principal_components(self):
        """ Do principal component analysis of sonos """
        if self.pca:
            print('PCA OFF')
            self.pca = None
            return

        # want to reduce dimensions of sono
        #sono = base.sono(self.data[-1][::2])
        width, height self.sono.shape
        if width < height:
            # FIXME: tell them to come back latet
            return
        
        sono = pandas.np.array([x[0] for x in self.sonos])

        sono = sono[:, self.offset:self.end]

        print('calculating PCA', sono.shape)

        self.pca = PCA(sono)

    async def draw_sono(self, timestamp=None):
        """ Dras sonograph """

        timestamp = timestamp or hush.utcnow()
        #sono = base.sono(self.data[-1][::2])
        sono = pandas.np.array([x[0] for x in self.sonos])

        sono = sono[:, self.offset:self.end]

        if self.pca:
            print('PCA', sono.shape)
            sono = self.pca.project(sono, minfrac=0.8)
            print(sono.shape)

        power = abs(sono)

        if self.log:
            power = np.log(power)

        vmin = 0
        if self.vmax is None:
            vmax = power[-1].max()
            vmax = max([max(x) for x in power])

        if self.fix:
            if self.vmax is None:
                self.vmax = vmax

            vmax = self.vmax
        else:
            self.vmax = self.vmin = None

        # sometimes vmax is negative
        vmin = min(vmin, vmax)

        self.axes.imshow(power.T.real, aspect='auto', vmax=vmax, vmin=vmin)
        title = 'offset: {} end: {} channel: {} delay: {} {}'.format(
            self.offset, self.end, self.channel,
            str(datetime.now() - timestamp), timestamp)

        def freq_format(x, pos=None):

            rate = self.mick.rate()
            frames = self.mick.frame_size()

            xx = x + self.offset

            hertz = (xx / frames) * (rate * 2.0)

            return '{:.1f}'.format(hertz)

        self.axes.yaxis.set_major_formatter(ticker.FuncFormatter(freq_format))

        title = title
        if self.pca:
            title += " PCA"
        self.axes.set_title(title)


    async def run(self):
        """ Run the animation

        Loop forever updating the figure

        A little help sleeping from curio
        """
        #self.axes.hold(True)

        self.offset = 0
        self.end = 100
        self.sonos = deque()

        await curio.spawn(self.read())

        while True:

            if self.clear:
                self.clear_axes()

            if not self.data:
                await curio.sleep(0.01)
                continue

            data, timestamp = await self.mick.get()

            self.sonos.append((self.sono_calc(data), timestamp))

            if self.plottype != 'sono':
                samples = int(len(data) / 2)
                start = self.channel * samples
                end = start + samples

                self.axes.plot(data[start:end])
                self.axes.set_ylim(ymin=-30000, ymax=30000)

                self.axes.set_title('{}'.format(str(datetime.now() - timestamp)))

            else:
                await self.draw_sono(timestamp)
            self.draw()

            while len(self.sonos) > 100:
                self.sonos.popleft()

def main(args=None):

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--infile')
    parser.add_argument('--nomick', action='store_true')
    
    args = parser.parse_args(args)

    from karmapi import mclock2
    farm = pigfarm.PigFarm()

    farm.add(SonoGram)
    farm.add(mclock2.GuidoClock)

    farm.add_mick(hush.Wave(mode='square'))
    farm.add_mick(hush.Wave())

    if args.infile:
        farm.add_mick(Connect(mick=open(args.infile, 'rb')))

    if not args.nomick:
        farm.add_mick(hush.Connect())


    pigfarm.run(farm)
                

if __name__ == '__main__':

    main()

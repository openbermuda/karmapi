"""
Widgets for pig
"""
from datetime import datetime

import PIL

from collections import deque

from karmapi import pig, base

import curio

import pandas
np = pandas.np

from matplotlib import ticker

from numpy import random

import math

PI = math.pi

class Circle(pig.PlotImage):


    def compute_data(self):

        r = 50

        self.x = range(-50, 51)

        self.y = [(((r * r) - (x * x)) ** 0.5) for x in self.x]


    def plot(self):

        self.axes.hold(True)
        self.axes.plot(self.x, self.y)

        
        self.axes.plot(self.x, [-1 * y for y in self.y])


class Friday(pig.Video):


    def compute_data(self):

        #self.data = random.randint(0, 100, size=100)
        self.data = list(range(100))

    def plot(self):

        self.axes.plot(self.data)

class MapPoints(pig.PlotImage):

    def compute_data(self):

        self.df = base.load(self.path)

    def plot(self):
        """ See Maps.plot_points_on_map """

        self.df.plot(axes=self.axes)
        
        self.axes.plot(self.data)

        
class InfinitySlalom(pig.Video):

    def compute_data(self):

        #self.data = random.randint(0, 100, size=100)
        self.waves_start = random.randint(5, 10)
        self.waves_end = random.randint(32, 128)
        nwaves = random.randint(self.waves_start, self.waves_end)
        self.x = np.linspace(
            0,
            nwaves,
            512) * PI
        
        self.y = np.sin(self.x / PI) * (64 * PI)

    def plot(self):

        #selector = pig.win_curio_fix()
        #curio.run(self.updater(), selector=selector)
        pass

    async def get_source(self):

        return await self.farm.micks.get()

    async def start(self):

        self.mick = await self.get_source()


    async def run(self):
        """ Run the animation 
        
        Loop forever updating the figure

        A little help sleeping from curio
        """
        
        self.axes.hold(True)

        while True:


            #data = await mick.get()
            #print('infinite data:', len(data))
            
            await curio.sleep(self.interval)

            if random.random() < 0.25:
                print('clearing axes', flush=True)
                self.axes.clear()

            self.compute_data()

            colour = random.random()
            n = len(self.x)
            background = np.ones((n, n))

            background *= colour

            background[0, 0] = 0.0
            background[n-1, n-1] = 1.0
        
            for curve in range(random.randint(3, 12)):


                self.axes.fill(self.x, self.y * 1 * random.random(),
                               alpha=0.3)
                self.axes.fill(self.x, self.y * -1 * random.random(),
                               alpha=0.3)
                self.axes.imshow(background, alpha=0.1, extent=(
                    0, 66 * PI, -100, 100))
                self.draw()
                
                await curio.sleep(1)

class SonoGram(pig.Video):

    def __init__(self, parent):

        super().__init__(parent)

        self.plottype = 'wave'

        self.create_event_map()
        self.samples = 1
        self.channel = 0


    def create_event_map(self):

        self.add_event_map('d', self.down)
        self.add_event_map('u', self.up)
        self.add_event_map('w', self.wide)
        self.add_event_map('s', self.slim)
        self.add_event_map('t', self.toggle_plottype)
        self.add_event_map('c', self.toggle_channel)
        self.add_event_map('m', self.next_mick)

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


    async def start(self):

        self.mick = await self.get_source()


    async def run(self):
        """ Run the animation 
        
        Loop forever updating the figure

        A little help sleeping from curio
        """
        #self.axes.hold(True)

        self.offset = 0
        self.end = 100
        self.sonos = deque()
        
        while True:


            data, timestamp = await self.mick.get()

            self.sonos.append((self.sono_calc(data), timestamp))
            
            if self.plottype != 'sono':
                #self.axes.hold(True)
                samples = int(len(data) / 2)
                start = self.channel * samples
                end = start + samples
                
                self.axes.plot(data[start:end])
                #self.axes.plot(data[-1][1::2])
                self.axes.set_ylim(ymin=-30000, ymax=30000)
                #self.axes.plot(range(100))
                #self.axes.plot(range(10, 110))

                self.axes.set_title('{}'.format(str(datetime.now() - timestamp)))

            else:
                #sono = base.sono(self.data[-1][::2])
                sono = pandas.np.array([x[0] for x in self.sonos])

                print(self.sonos[0][1], self.sonos[-1][1])

                sono = sono[:, self.offset:self.end]
                
                power = abs(sono)
                    
                self.axes.imshow(power.T.real, aspect='auto')
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
                
                self.axes.set_title(title)

            self.draw()
            
            while len(self.sonos) > 100:
                self.sonos.popleft()

            await curio.sleep(0.01)

            
class CurioMonitor:

    def __init__(self):

        import socket

        self.mon = socket.socket()

        host = curio.monitor.MONITOR_HOST
        port = curio.monitor.MONITOR_PORT
        self.mon.connect((host, port))

        self.info = self.mon.recv(10000)

    def ps(self):

        self.mon.send(b'ps\n')
        return self.mon.recv(100000)
                
    def where(self, n):

        self.mon.send('where {}\n'.format(n).encode())
        return self.mon.recv(100000)

class Curio(pig.Docs):
    """ A Curio Monitor 

    ps: show tasks
    where: show where the task is
    cancel: end the task
    """
    def __init__(self, parent=None):
        """ Set up the widget """
        super().__init__(parent)

        self.create_event_map()


    def create_event_map(self):

        self.add_event_map(' ', self.update)
        self.add_event_map('j', self.previous)
        self.add_event_map('k', self.next)

    async def previous(self):

        text, tasks = self.get_tasks()

        max_id = max(tasks)

        while True:
            self.task_id -= 1
            if self.task_id < 0:
                self.task_id = max_id
                
            if self.task_id in tasks:
                text += "\nWhere {}:\n\n".format(self.task_id)
                text += self.mon.where(self.task_id).decode()
                break

        self.set_text(text)
        
            
    async def next(self):

        text, tasks = self.get_tasks()

        max_id = max(tasks)

        while True:
            self.task_id += 1
            if self.task_id > max_id:
                self.task_id = 0
            if self.task_id in tasks:
                text += "\nWhere {}:\n\n".format(self.task_id)
                text += self.mon.where(self.task_id).decode()

                break

        self.set_text(text)


    def get_tasks(self):

        tasks = set()

        # get set of tasks -- be better to find the
        # curio kernel
        text = self.mon.ps().decode()
        for line in text.split('\n'):
            task = line.split()[0]
            if task.isdigit():
                tasks.add(int(task))

        return text, tasks


    async def update(self):

        self.set_text(self.get_tasks()[0])

    async def start(self):

        self.mon = CurioMonitor()
        self.task_id = 0

    async def run(self):

        await self.update()


def get_widget(path):

    parts = path.split('.')

    if len(parts) == 1:
        pig_mod = sys.modules[__name__]
        return base.get_item(path, pig_mod)

    return base.get_item(path)

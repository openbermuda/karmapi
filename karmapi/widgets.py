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


    def create_event_map(self):

        self.add_event_map('d', self.down)
        self.add_event_map('u', self.up)
        self.add_event_map('w', self.wide)
        self.add_event_map('s', self.slim)
        self.add_event_map('a', self.upsample)
        self.add_event_map('z', self.downsample)
        self.add_event_map('t', self.toggle_plottype)

    async def toggle_plottype(self):

        if self.plottype != 'sono':
            self.plottype = 'sono'
        else:
            self.plottype = 'wave'

    async def down(self):

        self.offset += 1
        self.end += 1

    async def up(self):

        self.offset -= 1
        self.end -= 1

    async def upsample(self):

        self.samples += 1
        self.init_data()

    async def downsample(self):

        if self.samples > 1:
            self.samples -= 1
            self.init_data()

    async def slim(self):

        self.end -= 5

    async def wide(self):

        self.end += 5

    def plot(self):
        pass
    
    async def get_source(self):

        return await self.farm.micks.get()

    async def read(self):


        print('xxxxxxxxxxxxxx', self.mick)

        # need to fire up the frames co-routine?
        print('firing up frame reader')
        await curio.spawn(self.mick.frames())

        self.data = deque()

        while True:
            #print('waiting on data')
            data = b''

            nsample = self.samples
            for sample in range(self.samples):
                data, timestamp = await self.mick.get()
                data += data

            if nsample != self.samples:
                continue

            #print('got data in sonogram', len(data), type(data))
            if 0 != (len(data) % 2048): break

            # quit reading if no data
            if not data:
                break
            
            data = self.mick.decode(data)
            sono = base.fft.fft(data[::2 * self.samples])

            #data = data[::2]
            #data = data[1::2]
            #data = np.arange(1024)
            #data = data * math.pi / random.randint(1, 10)
            #data = np.sin(data)

            self.data.append((data, sono, timestamp))

            while len(self.data) > 100:
                data, sono, timestamp = self.data.popleft()
                

    def init_data(self):

        self.sono = deque()
        self.data = deque()

    async def start(self):

        self.init_data()

        self.mick = await self.get_source()

        await curio.spawn(self.read())
        

    async def run(self):
        """ Run the animation 
        
        Loop forever updating the figure

        A little help sleeping from curio
        """
        #self.axes.hold(True)

        self.offset = 0
        self.end = 20
        
        while True:

            if not self.data:
                await curio.sleep(0.2)
                continue

            #print(len(self.sono), len(self.data))
            #sono = pandas.np.array([x for x in self.sono])
            #print('full sono size', sono.T.real.shape)
            #print('part sono size', sono[:, offset:end].T.shape)

            #self.axes.set_title('{} {}'.format(offset, end))

            data, sono, timestamp = self.data[-1]
            print(timestamp)
            if self.plottype != 'sono':
                
                #self.axes.hold(True)
                self.axes.plot(data[::2])
                #self.axes.plot(data[-1][1::2])
                self.axes.set_ylim(ymin=-30000, ymax=30000)
                #self.axes.plot(range(100))
                #self.axes.plot(range(10, 110))

                self.axes.set_title('{}'.format(str(datetime.now() - timestamp)))

            else:
                #sono = base.sono(self.data[-1][::2])
                sono = [x[1] for x in self.data]
                sono = pandas.np.array(sono)

                #print(sono.shape, len(self.data))

                #print(self.offset, self.end)
                sono = sono[:, self.offset:self.end]

                power = ((sono.real * sono.real) + (sono.imag * sono.imag)) ** 0.5

                #self.axes.imshow(sono.T.real, aspect='auto')
                self.axes.imshow(power.T.real, aspect='auto')
                title = 'offset: {} end: {} samples: {} {}, {}'.format(
                    self.offset, self.end, self.samples,
                    str(timestamp), str(datetime.now()))
                
                self.axes.set_title(title)

            self.draw()
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

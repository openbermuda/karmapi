"""
Widgets for pig
"""
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

    async def read(self):


        print('xxxxxxxxxxxxxx', self.mick)

        # need to fire up the frames co-routine?
        await curio.spawn(self.mick.frames())

        while True:
            data = await self.mick.get()

            data = self.mick.decode(data)
            
            self.sono.append(base.fft.fft(data))
            


    async def run(self):
        """ Run the animation 
        
        Loop forever updating the figure

        A little help sleeping from curio
        """
        from karmapi import hush

        self.sono = []

        self.mick = await self.get_source()

        await curio.spawn(self.read())
        
        self.axes.hold(True)

        while True:

            if not self.sono:
                await curio.sleep(0.2)
                continue
                
            sono = pandas.np.array(self.sono)
            print(sono.T.real.shape)
            
            self.axes.imshow(sono.T.real, aspect='auto')
            self.draw()
            await curio.sleep(0.2)

            #### FIXME temp hacking
            continue

            data = await mick.get()
            print('infinite data:', len(data))
            
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

    def plot(self):
        pass
    
    async def get_source(self):

        return await self.farm.micks.get()

    async def read(self):


        print('xxxxxxxxxxxxxx', self.mick)

        # need to fire up the frames co-routine?
        await curio.spawn(self.mick.frames())

        self.data = deque()

        while True:
            data = await self.mick.get()

            print('got data in sonogram', len(data), type(data))
            if len(data) != 2048: break

            # quit reading if no data
            if not data:
                break
            
            data = self.mick.decode(data)
            #data = data[::2]
            #data = data[1::2]

            self.data.append(data)

            self.sono.append(base.fft.fft(data))

            while len(self.sono) > 100:
                self.sono.popleft()

                
            while len(self.sono) > 100:
                self.data.popleft()
                
            

    async def run(self):
        """ Run the animation 
        
        Loop forever updating the figure

        A little help sleeping from curio
        """
        from karmapi import hush

        self.sono = deque()

        self.mick = await self.get_source()

        await curio.spawn(self.read())
        
        #self.axes.hold(True)

        while True:

            if not self.sono:
                await curio.sleep(0.2)
                continue

            print(len(self.sono), len(self.data))
            sono = pandas.np.array([x for x in self.sono])
            print('full sono size', sono.T.real.shape)
            offset = 800
            end = 1000
            #print('part sono size', sono[:, offset:end].T.shape)

            #self.axes.set_title('{} {}'.format(offset, end))

            self.axes.imshow(sono[:, offset:end].T.real, aspect='auto')
            #print(sono)
            #self.axes.imshow(sono.T.real, aspect='auto')

            #self.axes.plot(self.data[random.randint(len(self.data))])
            self.draw()
            await curio.sleep(0.2)

            offset += 1
            end += 1
            if offset > 1000:
                offset = 0
                end = 30

            # FIXME: shrink sono from time to time
            
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


    def show_previous(self):

        text, tasks = self.get_tasks()

        max_id = max(tasks)

        while True:
            self.task_id -= 1
            if self.task_id < 0:
                self.task_id = max_id
                
            if self.task_id in tasks:
                text += "\nWhere {}:\n\n".format(self.task_id)
                text += self.mon.where(self.task_id).decode()
                return text
        
        
    def show_next(self):

        text, tasks = self.get_tasks()

        max_id = max(tasks)

        while True:
            self.task_id += 1
            if self.task_id > max_id:
                self.task_id = 0
            if self.task_id in tasks:
                text += "\nWhere {}:\n\n".format(self.task_id)
                text += self.mon.where(self.task_id).decode()
                return text


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
        

    def dokey(self, key):

        m = self.mon
        
        text = m.ps().decode()
            
        if key.isdigit():

            ikey = int(key)
            text += "\nWhere {}\n\n".format(ikey)
            text += m.where(ikey).decode()

        elif key == 'J':
            text = self.show_previous()

        elif key == 'K':
            text = self.show_next()
            
        self.set_text(text)


    async def run(self):
        

        # spawn super()'s run co-routine
        await curio.spawn(super().run())
        
        self.mon = CurioMonitor()
        self.task_id = 0
        self.dokey('P')

        while True:
            event = await self.event_queue.get()

            print('curio monitor:', event)
            self.dokey(event)


        
def get_widget(path):

    parts = path.split('.')

    if len(parts) == 1:
        pig_mod = sys.modules[__name__]
        return base.get_item(path, pig_mod)

    return base.get_item(path)

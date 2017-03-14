""" Milk Monitor """
import numpy as np

import curio

from karmapi import pigfarm

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
        return self.mon.recv(100000).decode()
                
    def where(self, n):

        self.mon.send('where {}\n'.format(n).encode())
        return self.mon.recv(100000).decode()

    def task_info(self):

        text = self.ps()
        for line in text.split('\n'):
            
            if line.startswith('Task'):
                continue
            elif line.startswith('----'):
                continue
            elif line.startswith('curio'):
                continue
                
            tid, state, cycles, timeout, name = line.split()

            tid = int(tid)
            cycles = int(cycles)
            if timeout == 'None':
                timeout = 0.0
            else:
                timeout = float(timeout)
            
            yield dict(
                tid=tid,
                state=state,
                cycles=cycles,
                timeout=timeout,
                name=name)



class Curio(pigfarm.Docs):
    """ A Curio Monitor 

    ps: show tasks
    where: show where the task is
    cancel: end the task
    """
    def __init__(self, parent=None):
        """ Set up the widget """
        super().__init__(parent)

        self.add_event_map(' ', self.poll)
        self.add_event_map('j', self.previous)
        self.add_event_map('k', self.next)
        self.add_event_map('m', self.magic)

    async def previous(self):

        text, tasks = self.get_tasks()

        max_id = max(tasks)

        while True:
            self.task_id -= 1
    def task_info(self):

        text = self.mon.ps()
        for line in text.split('\n'):
            
            if line.startswith('Task'):
                continue
            elif line.startswith('----'):
                continue
            elif line.startswith('curio'):
                continue
                
            tid, state, cycles, timeout, name = line.split()

            tid = int(tid)
            cycles = int(cycles)
            timeout = timeout or float(timeout)
            
            yield dict(
                tid=tid,
                state=state,
                cycles=cycles,
                timeout=timeout,
                name=name)



            if self.task_id < 0:
                self.task_id = max_id
                
            if self.task_id in tasks:
                text += "\nWhere {}:\n\n".format(self.task_id)
                text += self.mon.where(self.task_id)
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
                text += self.mon.where(self.task_id)

                break

        self.set_text(text)


    def get_tasks(self):

        tasks = set()

        # get set of tasks -- be better to find the
        # curio kernel
        text = self.mon.ps()
        for line in text.split('\n'):
            task = line.split()[0]
            if task.isdigit():
                tasks.add(int(task))

        return text, tasks

    async def poll(self):

        self.set_text(self.get_tasks()[0])

    async def magic(self):
        """ magic curio 

        Here we really want to keep polling the kernel
        and display the data.

        But I am thinking the curio monitor is really a mick, it is
        as source of data.

        So turn it into frames and then we can feed it to viewers.
        """
        self.farm.add(MilkOnMagicCarpet, dict(mon=self.mon))


    async def start(self):

        self.mon = CurioMonitor()
        self.task_id = 0

    async def run(self):

        await self.poll()


class MilkOnMagicCarpet(pigfarm.MagicCarpet):

    def __init__(self, parent, mon=None):

        super().__init__(parent)

        self.mon = mon
        self.mode = 'timeout'
        self.log = False

        self.state_map = {}
        
        self.add_event_map('s', self.states)
        self.add_event_map('t', self.timeouts)
        self.add_event_map('b', self.cycles)


    def state_code(self, state):

        if state not in self.state_map:
            self.state_map[state] = len(self.state_map)

        return self.state_map[state]

    async def states(self):
        """ Show task states """
        if self.mode != 'states':
            self.frames = []
            
        self.mode = 'state'

    async def timeouts(self):
        """ Plot timeouts """
        if self.mode != 'timeout':
            self.frames = []
            
        self.mode = 'timeout'

    async def cycles(self):
        """ Show task cycles """
        if self.mode != 'cycles':
            self.frames = []

        self.mode = 'cycles'

    async def start(self):

        self.frames = []
        if not self.mon:
            self.mon = CurioMonitor()
        self.task_id = 0

    def get_frame(self):
        
        tasks = list(self.mon.task_info())

        frame = [x[self.mode] for x in tasks]

        if self.mode == 'timeout':
            frame = [x or 0.0 for x in frame]

        elif self.mode == 'state':
            frame = [self.state_code(x) for x in frame]

        return frame                


    async def run(self):
        """ magic curio """

        """
        Here we really want to keep polling the kernel
        and display the data.

        But I am thinking the curio monitor is really a mick, it is
        as source of data.

        So turn it into frames and then we can feed it to viewers.
        """

        while True:
            tasks = list(self.mon.task_info())

            frame = self.get_frame()
            if self.frames:
                if len(frame) != len(self.frames[0]):
                    self.frames = []
                    
            self.frames.append(self.get_frame())
            
            frames = np.array(self.frames)
            if self.log:
                frames = np.log(frames)
            print(frames.shape)

            self.axes.imshow(frames.T)
            self.axes.set_title(f'{self.mode} log: {self.log}')
            self.draw()

            self.prune()
            
            await curio.sleep(self.sleep)
    

    def prune(self):

        if len(self.frames) > 100:
            self.frames = self.frames[-100:]

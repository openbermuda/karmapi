""" Milk Monitor """

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
        return self.mon.recv(100000)
                
    def where(self, n):

        self.mon.send('where {}\n'.format(n).encode())
        return self.mon.recv(100000)

    def task_info(self):

        text = self.mon.ps().decode()
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

        text = self.mon.ps().decode()
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

    async def start(self):

        if not self.mon:
            self.mon = CurioMonitor()
        self.task_id = 0

    async def run(self):
        """ magic curio 

        Here we really want to keep polling the kernel
        and display the data.

        But I am thinking the curio monitor is really a mick, it is
        as source of data.

        So turn it into frames and then we can feed it to viewers.
        """

        self.frames = []
        while True:
            print(self.sleep)
            print('magic time')
            tasks = list(self.mon.task_info())

            self.frames.append([x.cycles for x in tasks])

            self.axes.imshow(self.frames)

            self.prune()
            
            await curio.sleep(self.sleep)
    

    def prune(self):

        if len(self.frames) > 100:
            self.frames = self.frames[-100:]

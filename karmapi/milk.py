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



    async def poll(self):

        self.set_text(self.get_tasks()[0])

    async def magic(self):
        """ magic curio """
        print('magic time')
        for task in self.task_info():
            print(task)


    async def start(self):

        self.mon = CurioMonitor()
        self.task_id = 0

    async def run(self):

        await self.poll()

"""
Pig widgets
"""
import curio

from karmapi import joy

if joy.BACKEND == 'qt':

    from .backends.qtpig import *

else:

    from .backends.tkpog import *

global YQ

YQ = curio.Queue()
    
def printf(*args, **kwargs):

    print(*args, flush=True, **kwargs)

def get_widget(path):

    parts = path.split('.')

    if len(parts) == 1:
        pig_mod = sys.modules[__name__]
        return base.get_item(path, pig_mod)

    return base.get_item(path)
    
class Pigs(Widget):

    def __init__(self, recipe=None, args=None):

        super().__init__()

        self.meta = recipe or meta()
        self.args = args

        # keep a list of asynchronous tasks needed to run widgets
        self.runners = set()
        self.lookup = {}
        self.build()

    def build(self):

        self.layout = VBoxLayout(self)

        widget = self.build_info()
        if widget:
            self.layout.addWidget(widget)
            
        widget = self.build_parms()
        if widget:
            self.layout.addWidget(widget)

        widget = self.build_tabs()
        if widget:
            self.layout.addWidget(widget)

    def build_tabs(self):
        """ Build tabs """

        self.tb = TabWidget()
        self.tabs = {}
        for tab in self.meta.get('tabs', []):

            w = qtw.QWidget()

            name = tab['name']
            self.tb.addTab(w, name)

            self.tabs[name] = {}

            widgets = tab.get('widgets')

            if widgets:
                print(widgets)
                grid = self.build_widgets(w, widgets)
                self.tabs[name] = grid

                self.lookup.update(grid.lookup)

        #self.tb.setCurrentIndex(2)

        return self.tb

    def build_info(self):
        """ Build info """
        pass
    
    def build_parms(self):
        """ Build parms """

        return ParmGrid(self, self.meta.get('parms', {}))

    def build_widgets(self, parent, widgets):

        grid = Grid(parent, widgets)

        for widget in grid.grid.values():
            if hasattr(widget, 'run'):
                self.runners.add(widget.run())

        return grid

    def __getitem__(self, item):

        if item in self.lookup:
            return self.lookup.get(item)

        raise KeyError

    def runit(self):
        
        print('pig runit :)')

        self.eloop.submit_job(doit)
        self.eloop.submit_job(self.doit())

    async def doit(self):
        """  Async callback example for yosser

        See Pig.runit()
        """
        from datetime import datetime
        sleep = random.randint(1, 20)
        printf("running doit doit doit {} {}".format(sleep, datetime.now()))
        start = time.time()
        await curio.sleep(sleep)
        end = time.time()
        printf('actual sleep {} {} {}'.format(
            sleep, end-start, datetime.now()))
        return sleep


    async def run(self):
        """ Make the pig run """
        # spawn task for each runner
        coros = []
        for item in self.runners:
            if inspect.iscoroutine(item):
                coros.append(await(curio.spawn(item)))

        await curio.gather(coros)

class Grid(Widget):
    """ A grid of widgets """

    def __init__(self, parent=None, widgets=None):

        super().__init__()
        self.parent = parent
        self.grid = {}
        self.lookup = {}
        self.build(widgets)

    def build(self, widgets):
        
        rows = widgets

        # FIXME create the widget
        vlayout = VBoxLayout(self.parent)
        for irow, row in enumerate(rows):
            wrow = Widget()
            vlayout.addWidget(wrow)
            hlayout = HBoxLayout(wrow)
            for icol, item in enumerate(row):

                # using isinstance makes me sad..
                # but i will make an exception
                if isinstance(item, str):
                    # assume it is a path to a widget
                    widget = get_widget(item)(None)
                    
                elif isinstance(item, dict):
                    # see if dict specifies the widget
                    widget = item.get('widget', button)

                    if isinstance(widget, str):
                        # maybe it is a path to a widget
                        # eg "karmapi.tankrain.TankRain"
                        widget = get_widget(widget)

                    # build the widget
                    widget = widget(item)

                    # add reference if given one
                    name = item.get('name')
                    if name:
                        self.lookup[name] = widget
                else:
                    widget = item(None)

                self.grid[(irow, icol)] = widget

                hlayout.addWidget(widget)

    def __getitem__(self, item):

        if item in self.lookup:
            return self.lookup.get(item)

        return self.grid.get(item)


class ParmGrid(Grid):
    def build(self, parms=None, parent=None):

        layout = qtw.QGridLayout()
        self.setLayout(layout)

        parms = parms or {}

        print('parms:', parms)
        
        for row, item in enumerate(parms):

            print('parms:', row, item)
            label = qtw.QLabel(item.get('label'))
            layout.addWidget(label, row, 0)
            entry = qtw.QLineEdit()
            layout.addWidget(entry, row, 1)
            

        return self

class EventLoop:
    """ An event loop

    For now, this is just here to make a Qt app run
    under curio,

    For now it has two tasks.

    flush:  wait for an event, then process it

    poll: periodically tests if the app has pending events


    FIXME: add a magic task that magically knows when there
           are events pending without having to poll.

           Somewhere in the depths of Qt there has to be an
           event queue.  If that code can be fixed to let
           this event loop know when the queue is not empty
           then we'd have magic.

           somewhere there is a magic file or socket?
    """

    def __init__(self, app=None):

        self.app = app
        
        self.queue = curio.Queue()

        self.event_loop = qtcore.QEventLoop()

        if sys.platform == 'win32':
            self.ppe = ProcessPoolExecutor()


    def put(self, event):
        """ Maybe EventLoop is just a curio.EpicQueue? """
        self.queue.put(event)

        
    async def flush(self):
        """  Wait for an event to arrive in the queue.
        """
        while True:

            event = await self.queue.get()

            self.event_loop.processEvents()
            self.app.sendPostedEvents(None, 0)


    async def poll(self, yq):

        # Experiment with sleep to keep gui responsive
        # but not a cpu hog.
        event = 0

        while True:

            if self.app.hasPendingEvents():

                # FIXME - have Qt do the put when it wants refreshing
                self.put(event)
                event += 1

            await curio.sleep(0.05)

    def submit_job(self, coro, afters, *args, **kwargs):
        """ Submit a coroutine to the job queue """
        print('SUBMIT', args, kwargs)
        self.yq.put([coro, afters, args, kwargs])

    async def yosser(self, yq):

        self.yq = yq
        while True:
            job, afters, args, kwargs = await yq.get()

            print('yay!! yosser got a job {}'.format(job))

            start = time.time()
            # fixme: want curio run for
            if inspect.iscoroutine(job):
                result = await job
            else:
                if sys.platform != 'win32':
                    result = await curio.run_in_process(job, *args, **kwargs)
                else:
                    result = await curio.run_in_executor(
                        self.ppe, job, *args, **kwargs)
            end = time.time()

            if afters:
                afters(result)

            print("doit slept for {} {}".format(result, end-start))
            

    def magic(self, event, *args, **kwargs):
        """ Gets called when magic is needed """
        printf('magic', flush=True)
        self.put(event)


    async def run(self):

        poll_task = await curio.spawn(self.poll(YQ))

        flush_task = await curio.spawn(self.flush())

        yosser_tasks = []
        for yosser in range(cpu_count()):
        
            yosser_tasks.append(await curio.spawn(self.yosser(YQ)))

        tasks = [flush_task, poll_task] +  yosser_tasks

        await curio.gather(tasks)

    
def print_thread_info(name):
    import threading
    print()
    print(name)
    print(globals().keys())
    print(locals().keys())
    print(threading.current_thread())
    print(threading.active_count())
    print('YQ:', YQ.qsize())


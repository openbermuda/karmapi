"""
Pig widgets
"""

import PIL
import curio
from concurrent.futures import ProcessPoolExecutor

from karmapi import joy

if joy.BACKEND == 'qt':

    from .backends.qtpig import *

else:

    from .backends.tkpig import *

global YQ

YQ = curio.Queue()
    
def printf(*args, **kwargs):

    print(*args, flush=True, **kwargs)

def get_widget(path):

    parts = path.split('.')

    # FIXME look in ./widgets,py as well
    # or rather have a list set up as default and away we go.
    if len(parts) == 1:
        pig_mod = sys.modules[__name__]
        return base.get_item(path, pig_mod)

    return base.get_item(path)
    
class Pigs(Pig):

    def __init__(self, app, recipe=None, args=None):

        super().__init__(app.toplevel())

        self.meta = recipe or meta()
        self.args = args

        # keep a list of asynchronous tasks needed to run widgets
        self.runners = set()
        self.lookup = {}
        self.build()

    def build(self):

        layout = VBoxLayout(self)

        widget = self.build_info()
        if widget:
            layout.addWidget(widget)
            
        widget = self.build_parms()
        if widget:
            layout.addWidget(widget)

        widget = self.build_tabs()
        if widget:
            layout.addWidget(widget)

    def build_tabs(self):
        """ Build tabs """

        self.tb = TabWidget(self)
        self.tabs = {}
        for tab in self.meta.get('tabs', []):

            name = tab['name']
            printf(name)

            widgets = tab.get('widgets')

            w = self.tb.add_tab(name)
            print('frame', w)

            layout = VBoxLayout(w)
            if widgets:
                grid = self.build_widgets(w, widgets)
                self.tabs[name] = grid
                
                self.lookup.update(grid.lookup)

                layout.addWidget(grid)

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

class Grid(Pig):
    """ A grid of widgets """

    def __init__(self, parent=None, widgets=None):

        super().__init__(parent)
        self.parent = parent
        self.grid = {}
        self.lookup = {}
        self.build(widgets)

    def build(self, widgets):
        
        rows = widgets

        # FIXME create the widget
        vlayout = VBoxLayout(self)
        for irow, row in enumerate(rows):
            wrow = Piglet(self)
            vlayout.addWidget(wrow)
            hlayout = HBoxLayout(wrow)
            for icol, item in enumerate(row):

                # using isinstance makes me sad..
                # but i will make an exception
                if isinstance(item, str):
                    # assume it is a path to a widget
                    widget = get_widget(item)(wrow)
                    
                elif isinstance(item, dict):
                    # see if dict specifies the widget
                    widget = item.get('widget', button)

                    if isinstance(widget, str):
                        # maybe it is a path to a widget
                        # eg "karmapi.tankrain.TankRain"
                        widget = get_widget(widget)

                    # build the widget
                    print(widget)
                    widget = widget(wrow, item)

                    # add reference if given one
                    name = item.get('name')
                    if name:
                        self.lookup[name] = widget
                else:
                    widget = item(wrow)

                self.grid[(irow, icol)] = widget

                hlayout.addWidget(widget)

    def __getitem__(self, item):

        if item in self.lookup:
            return self.lookup.get(item)

        return self.grid.get(item)


class ParmGrid(Grid):
    def build(self, parms=None, parent=None):

        layout = GridLayout()
        self.setLayout(layout)

        parms = parms or {}

        print('parms:', parms)
        
        for row, item in enumerate(parms):

            print('parms:', row, item)
            label = Label(self, item.get('label'))
            layout.addWidget(label, row, 0)
            entry = LineEdit(self)
            layout.addWidget(entry, row, 1)

        return self

class GridBase:

    def clear(self):

        for item in self.layout.children():
            self.layout.removeItem(item)
        
    def load(self, data):

        self.data = data

        self.draw()

    def draw(self):
        
        self.clear()

        data = self.data
        
        formatter = EngFormatter(accuracy=0, use_eng_prefix=True)
        layout = self.layout
        
        for column, name in enumerate(data.columns.values):
            button = HeaderLabel(str(name))

            layout.addWidget(button, 0, column + 1)

        nrows = min(len(data) - self.start_row, self.number_of_rows)
        for row in range(nrows):

            for col in range(len(data.columns)):

                value = data.values[row + self.start_row][col]
                try:
                    # format data with formatter function
                    value = formatter(value)
                except:
                    # anything goes wrong, just show with str
                    value = str(value)

                label = GridLabel(value)

                layout.addWidget(label, row+1, col+1)

        pad = Widget()
        layout.addWidget(pad, 0, len(data.columns) + 1,
                         len(data), len(data.columns) + 1)

        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(len(data.columns) + 1, 1)
        
        size = self.inner.minimumSize()
        printf(size.width(), size.height())
        
        return

class LabelGrid(GridBase, Pig):

    def __init__(self, parent=None, widgets=None):

        super().__init__()

        self.number_of_rows = 10
        self.start_row = 0

        self.setLayout(GridLayout())

        self.layout = self.layout()
        self.layout.setSpacing(1)
        self.inner = self

        self.setFocusPolicy(qt.StrongFocus)


    def keyPressEvent(self, event):

        printf(self.start_row, len(self.data))
        key = event.key()
        printf(key)
        if key == qtcore.Qt.Key_Down:
            # scroll down one row
            self.start_row += 1

        elif key == qtcore.Qt.Key_Up:
            self.start_row -= 1

        elif key == qtcore.Qt.Key_PageDown:
            self.start_row += self.number_of_rows

        elif key == qtcore.Qt.Key_PageUp:
            self.start_row -= self.number_of_rows

        self.start_row = max(0, self.start_row)
        self.start_row = min(len(self.data) - self.number_of_rows,
                             self.start_row)

        self.draw()

    
class EventLoop(AppEventLoop):
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

        super().__init__(app)

        if app:
            self.app = app
            
        self.queue = curio.Queue()

        if sys.platform == 'win32':
            self.ppe = ProcessPoolExecutor()


    def put(self, event):
        """ Maybe EventLoop is just a curio.EpicQueue? """
        self.queue.put(event)

    def submit_job(self, coro, afters=None, *args, **kwargs):
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

        poll_task = await curio.spawn(self.poll())

        flush_task = await curio.spawn(self.flush())

        yosser_tasks = []
        for yosser in range(cpu_count()):
        
            yosser_tasks.append(await curio.spawn(self.yosser(YQ)))

        tasks = [flush_task, poll_task] +  yosser_tasks

        await curio.gather(tasks)


class Piglet(Pig):
    pass
        
class MagicCarpet(PlotImage):
    """ Magic data display 

    image, table, plots and more
    """

    def __init__(self, parent, *args):

        super().__init__(parent)

        print('MagicCarpet', *args)

        self.mode = 'plot'

        self.add_event_map('t', self.table)

    async def image(self):
        """ Toggle image state """
        pass

    def compute_data(self):

        self.data = [[random.randint(x, 10 * x) for x in range(1, 6)] for y in range(3)] 

    async def table(self):
        """ Toggle image state """

        nextmode = dict(
            plot='table',
            table='both',
            both='plot')

        self.axes.clear()
        self.mode = nextmode.get(self.mode, 'table')

        if self.mode != 'table':
            self.plot()


        if self.mode != 'plot':
            self.draw_table()
        
        self.draw()

        
        
    def draw_table(self):

        from matplotlib import colors, cm, table
        norm = colors.Normalize()
        #self.axes.clear()
        colours = cm.get_cmap()(norm(self.data))
        print(colours)

        locs = list(table.Table.codes.keys())
        loc = locs[random.randint(1, 17)]

        colours[:, :, 3] = 0.5
        self.axes.table(
            cellText=self.data, cellColours=colours,
            loc=loc)
            #loc='upper_center')
        self.axes.set_title(f'table location {loc}')
        self.axes.set_axis_off()


    async def run(self):

        self.compute_data()
        self.plot()
        self.draw()
        
        
class KPlot(PlotImage):

    def compute_data(self):

        self.data = [list(range(100)) for x in range(100)]

class XKCD(PlotImage):

    def __init__(self, parent, *args, **kwargs):

        super().__init__(parent)

    def plot(self):
        """ Display plot xkcd style """
        with plt.xkcd():

            np = pandas.np

            data = np.ones(100)
            data[70:] -= np.arange(30)

            self.axes.plot(data)

            self.axes.annotate(
                'THE DAY I REALIZED\nI COULD COOK BACON\nWHENEVER I WANTED',
                xy=(70, 1), arrowprops=dict(arrowstyle='->'), xytext=(15, -10))

            self.axes.set_xlabel('time')
            self.axes.set_ylabel('my overall health')


class Image(PlotImage):


    def __init__(self, parent, image=None, title=None, galleries=None):

        from ripl import imagefind
        
        self.path = '/home/jng/devel/karmapi/docs/pycaribbean/princess_cricket.jpg'

        if galleries:
            self.path = imagefind.interpret(dict(galleries=galleries, image=image))

        self.title = title or ''

        super().__init__(parent)


    def plot(self):

        try:
            im = PIL.Image.open(self.path)
            self.axes.imshow(im)
        except:
            pass


        self.axes.set_title(self.title)

        self.axes.set_xticks([])
        self.axes.set_yticks([])
        


        
class Video(PlotImage):
    """ a video widget

    This is currently a matplotlib FigureCanvas
    """
    def __init__(self, parent, interval=1, *args, **kwargs):

        super().__init__(parent, **kwargs)
        self.interval = interval or 1

    async def run(self):
        """ Run the animation """
        # Loop forever updating the figure, with a little
        # sleeping help from curio
        while True:
            await curio.sleep(self.interval)
            self.update_figure()

    def compute_data(self):

        self.data = pandas.np.random.normal(size=(100, 100))

    def __repr__(self):

        return self.data


    def plot(self):

        self.axes.imshow(self.data)

    def update_figure(self):
        """  Update the figure 

        This just re-computes data and replots.
        """
        self.compute_data()
        self.plot()
        self.draw()

def doit():
    """  Callback example for yosser

    See Pig.runit()
    """
    n = random.randint(35, 40)
    start = time.time()
    #time.sleep(sleep)
    sleep = fib(n)
    end = time.time()
    print('actual sleep {} {}'.format(sleep, end-start))
    return n, sleep

def fib(n):
    if n <= 2:
        return 1
    else:
        return fib(n-1) + fib(n-2)

    

        
def print_thread_info(name):
    import threading
    print()
    print(name)
    print(globals().keys())
    print(locals().keys())
    print(threading.current_thread())
    print(threading.active_count())
    print('YQ:', YQ.qsize())


"""
Pi Gui on a Sense Hat
"""

import curio

from . import tkpig

from tkpig import Pig, AppEventLoop



class Help:

    def __init__(self, msg):

        msg = msg or "Help Me!"

        print(msg)
        #messagebox.showinfo(message=msg)



class Canvas(tkpig.Canvas):

    
    def __init__(self, parent):

        super().__init__(parent, **kwargs)

        self.width = 400
        self.height = 400

    

    
class PlotImage(tkpig.PlotImage):
    """ An image widget

    This is just a wrapper around matplotlib FigureCanvas.
    """
    def __init__(self, parent, **kwargs):

        super().__init__(parent, **kwargs)

        

    def plot(self):
        pass
    
    async def run(self):
        """ Over-ride to do your thing """    
        self.compute_data()
        self.plot()



class KPlot(PlotImage):

    def compute_data(self):

        self.data = [list(range(100)) for x in range(100)]

class XKCD(PlotImage):

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



class Video(PlotImage):
    """ a video widget

    This is currently a matplotlib FigureCanvas
    """

    def __init__(self, parent):
        super().__init__(parent)

        self.interval = 1
    
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


class AppEventLoop:
    """ An event loop

    tk specific application event loop
    """
    def __init__(self, app=None):

        if app is None:
            self.app = Tk()

        self.events = curio.UniversalQueue()
        self.app.bind('<Key>', self.keypress)

    def set_event_queue(self, events):

        self.events = events

    def keypress(self, event):
        """ Take tk events and stick them in a curio queue """
        self.events.put(event.char)
        
        return True

    async def flush(self):
        """  Wait for an event to arrive in the queue.
        """
        while True:

            event = await self.queue.get()

            self.app.update_idletasks()
            self.app.update()


    async def poll(self):

        # Experiment with sleep to keep gui responsive
        # but not a cpu hog.
        event = 0

        nap = 0.05
        while True:

            # FIXME - have Qt do the put when it wants refreshing
            await self.put(event)
            event += 1

            nap = await self.naptime(nap)

            # FIXME should do away with the poll loop and just schedule
            # for some time in the future.
            await curio.sleep(nap)

    async def naptime(self, naptime=None):
        """ Return the time to nap 
        
        FIXME: make this adaptive, but keep it responsive

        The idea would be to see how many events each poll produces.

        So, if there are a lot of events, shorten the naps.

        If there are not so many take a longer nap


        This should take into account how fast events are taking to arrive and
        how long they are taking to process and balance the two.

        And don't sleep too long, in case some other task wakes up and starts talking.

        Better still, might be to have something else managing nap times.

        For now, keep it simple.
        """

        if naptime is None:
            nap = 0.05

        return naptime


class Application(Tk):


    def __init__(self, *args):

        super().__init__()

    def toplevel(self):
        return self

    
class Label(ttk.Label):

    def __init__(self, parent, text=None):


        text = text or 'hello world'
        super().__init__(parent, text=text)


class TabWidget(ttk.Notebook):

    def add_tab(self, name):

        widget = ttk.Frame(self)

        self.add(widget, text=name)

        return widget
        
LineEdit = ttk.Entry        

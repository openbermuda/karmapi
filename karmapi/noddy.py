"""
Noddy
=====

Something playful.

A place to try something, see what happens.

Keep it short, go back in time.

"""

import sys

import argparse

import pandas

from karmapi import pigfarm, toy

class Magic(pigfarm.MagicCarpet):

    def __init__(self, parent=None, data=None):

        super().__init__(parent, axes=[211, 212])

        # hmm.. not sure where this belongs
        pandas.set_eng_float_format(1, True)

        data = data or toy.distros(
            trials=1000,
            groups=['abc', 'cde', 'xyz'])

        self.data = data

        if data:
            self.process_data()

        self.add_event_map(' ', self.next_group)

    def process_data(self):

        data = self.data
        frames = {}
        groups = []
        for group, frame in data.items():
            frame = pandas.DataFrame(frame)

            frames[group] = frame
            groups.append(group)

        self.frames = frames
        self.group = 0
        self.groups = groups

    async def next_group(self):
        """ Next group """
        self.group += 1

        if self.group == len(self.groups):
            self.group = 0

        await self.event.put(self.group)


    async def load_data(self):

        while True:
            self.data = await self.farm.data.get()

            self.process_data()
            

    async def tester(self):

        dim = 4
        text = [[42] * dim] * dim
        rows = ['count'] * dim

        ax = self.subplots[0]
        ax.axis('off')
        ax.table(rowLabels=rows, cellText=text, loc='center')

        self.draw()
        await pigfarm.sleep(5)
        
        #ax = self.subplots[1]
        ax.clear()
        ax.axis('off')
        ax.table(rowLabels=rows, cellText=text, loc='center')
        self.draw()
        
        await pigfarm.sleep(5)


    def draw_plot(self):

        group = self.groups[self.group]
        frame = self.frames[group]

        axes = self.subplots[0]
        axes.clear()

        # sort columns on mean
        mean = frame.mean()
        mean.sort()
        frame = frame.ix[:, mean.index]
        
        col_colours = []
        for label in frame.columns:
            data = frame[label].copy()
            data.sort_values(inplace=True)
            if self.log:
                patch = axes.semilogy(data.values, label=label)
            else:
                patch = axes.plot(data.values, label=label)

            col_colours.append(patch[0].get_color())

        from matplotlib import colors
        col_colours = [colors.to_rgba(x, 0.2) for x in col_colours]

        self.axes = self.subplots[1]
        self.axes.clear()
        self.draw_table(frame, loc='center', title=group, col_colours=col_colours)

        self.draw()
        
        
    async def run(self):

        await pigfarm.spawn(self.load_data())

        # have a key to cancel test?
        #await self.tester()

        while True:
            self.draw_plot()
            self.group = await self.event.get()

def play(infile):

    print('infile:', infile)

if __name__ == '__main__':

    print(sys.argv)

    parser = argparse.ArgumentParser()
    parser.add_argument('--file')
    parser.add_argument('--thresh', type=float, default=10.0)

    
    args = parser.parse_args()


    if args.thresh > 10:

        print('bigly')

    elif args.thresh < 5:

        print('fake')

        
    farm = pigfarm.PigFarm()
    farm.add(Magic)

    pigfarm.run(farm)

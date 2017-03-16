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
            trials=10,
            groups=['abc', 'cde', 'xyz'])

        frames = {}
        groups = []
        for group, frame in data.items():
            frame = pandas.DataFrame(frame)

            frames[group] = frame
            groups.append(group)
            
        self.frames = frames
        self.group = groups[0]
        self.groups = groups


    async def run(self):

        frame = self.frames[self.group]

        axes = self.subplots[0]
        for label in frame.columns:
            data = frame[label].copy()
            data.sort()
            axes.plot(data.values, label=label)

        self.axes = self.subplots[1]
        self.draw_table(frame, loc='center')

def play(infile):

    print('infile:', infile)

if __name__ == '__main__':

    print(sys.argv)

    parser = argparse.ArgumentParser()
    parser.add_argument('--file')
    parser.add_argument('--thresh', type=float, default=10.0)

    
    args = parser.parse_args()

    print(args)


    if args.thresh > 10:

        print('bigly')

    elif args.thresh < 5:

        print('fake')

        
    farm = pigfarm.PigFarm()
    farm.add(Magic)

    pigfarm.run(farm)

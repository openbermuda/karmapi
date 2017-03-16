
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

        super().__init__(parent)

        data = data or toy.distros(
            trials=10,
            groups=['abc', 'cde', 'xyz'])

        print('ddddd', len(data))
        print(data)

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

        print(frame.describe())

        for label in frame.columns:
            self.axes.plot(frame[label], label=label)

        self.draw_table(data=frame.describe().values)

def play(infile):

    print('infile:', infile)

if __name__ == '__main__':

    print(sys.argv)

    parser = argparse.ArgumentParser()
    parser.add_argument('--file')
    parser.add_argument('--thresh', type=float, default=10.0)

    
    args = parser.parse_args()

    print(args)

    pandas.set_eng_float_format(1, True)

    if args.thresh > 10:

        print('bigly')

    elif args.thresh < 5:

        print('fake')

        
    farm = pigfarm.PigFarm()
    farm.add(Magic)

    pigfarm.run(farm)

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

    async def tester(self, sleep=2):

        print('NUMBER OF TESTS', self.tests)
        self.tests += 1

        from matplotlib import rcParams
        dim = 1
        text = [[42] * dim] * dim
        rows = ['count'] * dim

        self.subplots[1].axis('off')
        ax = self.subplots[0]
        ax.axis('off')
        ax.table(rowLabels=rows, cellText=text, loc='center')

        print('calling self.draw from tester')
        self.draw()
        await pigfarm.sleep(sleep)
        
        #ax = self.subplots[1]
        ax.clear()
        ax.axis('off')
        ax.table(rowLabels=rows, cellText=text, loc='center')
        self.draw()
        
        await pigfarm.sleep(sleep)


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

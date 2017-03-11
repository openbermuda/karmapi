"""
Currie -- you can do magic.

Goal here is to have a thread launching piglets.

And curio controlling the operation.

Aim to use joy to control which widget loop to use.

No piglets known to be harmed with this code.

So there is a pig farm and piglets running everywhere.

And currie doing magic.
"""
from collections import deque
import curio
from pathlib import Path
import inspect

from karmapi import hush

from tkinter import Toplevel

from karmapi import pigfarm

def main():

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('--pig', default='tk')
    parser.add_argument('--wave')
    parser.add_argument('--gallery', nargs='*', default=['.', '../gallery'])
    parser.add_argument('--images', default=False, action='store_true')

    parser.add_argument('--thresh', type=float, default=10.0)

    parser.add_argument('--monitor', action='store_true')
    parser.add_argument('--nomon', action='store_false', default=True)
    parser.add_argument('--words', default='diceware.wordlist.asc')
    parser.add_argument(
        '--files',
        nargs='+',
        default=__file__)

    args = parser.parse_args()

    # import from pig stuff here, after talking to joy
    from karmapi import joy
    joy.set_backend(args.pig)


    from karmapi import pig, piglet
    from karmapi import widgets
    from karmapi import sonogram

    # what's this doing here?
    #import tkinter

    farm = pigfarm.PigFarm()

    print('building farm')
    farm.status()
    from karmapi.mclock2 import GuidoClock
    from karmapi.bats import StingingBats
    from karmapi.tankrain import TankRain
    from karmapi import diceware as dice
    from karmapi import talk

    if args.monitor:

        farm.add(widgets.Curio)

    images = [
        dict(image='climate_karma_pi_and_jupyter.png', title=''),
        dict(image='gil_ly_.png', title=''),
        dict(image='princess_cricket.jpg', title='Princess Cricket'),
        dict(image='fork_in_road.jpg', title='Fork in the Road'),
        dict(image='tree_of_hearts.jpg', title='Tree of Hearts'),
        #dict(image='chess.jpg', title='Branching'),
        dict(image='lock.jpg', title='Global Interpreter Lock'),
        dict(image='air_water.jpg', title='async def(): await run()'),
        dict(image='venus.jpg', title='Jupyter')]


    from karmapi import sunny

    farm.files = args.files

    print('galleries', args.gallery)

    im_info = dict(galleries=args.gallery)

    if args.images:
        for im in images:
            im_info.update(im)
            farm.add(piglet.Image, im_info.copy())


    words = Path(args.words)
    if words.exists():
        words = words.open()
    else:
        words = None

    farm.add(piglet.MagicCarpet)
    farm.add(talk.Talk)
    farm.add(dice.StingingBats, dict(words=words))
    farm.add(StingingBats)

    farm.add(TankRain)
    #farm.add(sunny.Sunspot)
    farm.add(sonogram.SonoGram)
    farm.add(piglet.XKCD)
    farm.add(widgets.InfinitySlalom)
    farm.add(GuidoClock)

    from karmapi import prime
    farm.add(prime.Prime)

    # add a couple of micks to the Farm
    if args.wave:
        farm.add_mick(hush.Connect(hush.open_wave(args.wave)))
    else:
        farm.add_mick(hush.Connect())
        farm.add_mick(hush.Wave(mode='square'))
        farm.add_mick(hush.Wave())

    farm.status()

    curio.run(farm.run(), with_monitor=args.nomon)


if __name__ == '__main__':

    main()

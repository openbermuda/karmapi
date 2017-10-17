"""
Somewhere

under a rainbow

way up high

Credits:  GOES East Rainbow data from NOAA
"""
import argparse
import datetime
from pathlib import Path
import curio

import requests

from karmapi import base, tpot

URL = "http://www.ssd.noaa.gov/goes/east/tatl/rb-animated.gif"


def get(path, url=URL):
    """ Get latest rainbow """

    with Path(path).open('wb') as out:
        out.write(requests.get(url).content)


async def capture(args):

    
    while True:

        now = datetime.datetime.now()
        path = Path(f'{args.path}/{now.year}/{now.month}/{now.day}')
        path.mkdir(exist_ok=True, parents=True)
        path = path / f'{now.hour:02}{now.minute:02}{now.second:02}.gif'

        print(path)
        get(str(path))        
        await curio.sleep(args.sleep)



def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--sleep', type=float, default=60*60)
    parser.add_argument('path', nargs='?', default='.')

    args = parser.parse_args()

    curio.run(capture(args))


if __name__ == '__main__':

    main()

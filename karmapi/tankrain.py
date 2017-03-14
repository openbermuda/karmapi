""" Bermuda weather
"""
import argparse

import datetime
utcnow = datetime.datetime.utcnow

import requests
from pathlib import Path

from collections import defaultdict

import curio

from karmapi import show, base

from karmapi import pigfarm

# Paths to data
url = 'http://weather.bm/images/'

radar_template = 'Radar/CurrentRadarAnimation_{size}km_sri/{date:%Y-%m-%d-%H%M}_{size}km_sri.png'
parish_template = 'Radar/RadarParish/{date:%Y-%m-%d-%H%M}_ParishRadar.png'

atlantic_chart = 'surfaceAnalysis/Latest/Atlantic.gif'
local_chart = 'surfaceAnalysis/Latest/Local.gif'

target = 'tankrain/{date:%Y}/{date:%m}/{date:%d}/{name}_{date:%H%M}{suffix}'


class TankRain(pigfarm.MagicCarpet):
    """ Widget to show tankrain images """

    def __init__(self, parent, *args):
        
        self.version = 'local'
        self.load_images()

        super().__init__(parent)

        self.add_event_map('w', self.wide)
        self.add_event_map('l', self.local)
        self.add_event_map('b', self.parish)
        self.add_event_map('r', self.reverse)


    def load_images(self):
        
        self.paths = [x for x in self.get_images()]
        self.ix = 0
        self.inc = 1

    def compute_data(self):

        from PIL import Image

        ix = self.ix

        if ix < len(self.paths):
            im = Image.open(self.paths[ix])
        else:
            # FIXME -- create an image that shows there is no data
            # for now, lets just show a rainbow
            rainbow = [x for x in range(100)]
            im = [rainbow] * 100

        ix = ix + self.inc
        if ix == len(self.paths):
            ix = 0
        if ix < 0:
            ix = len(self.paths) - 1
            
        self.ix = ix
                            
        self.data = im 

    def get_images(self):

        # FIXME -- create key bindings to select time
        date = utcnow()
        path = Path(f'~/karmapi/tankrain/{date:%Y}/{date:%m}/{date:%d}').expanduser()

        for image in sorted(path.glob('{}*.png'.format(self.version))):
            yield image


    async def local(self):

        self.version = 'local'
        self.load_images()

    async def wide(self):

        self.version = 'wide'
        self.load_images()

    async def parish(self):

        self.version = 'parish'
        self.load_images()


    async def reverse(self):

        self.inc *= -1

    async def run(self):

        
        while True:

            tt = base.Timer()
            
            tt.time('start')
            self.compute_data()
            tt.time('compute')

            self.axes.imshow(self.data)
            tt.time('plot')


            self.draw()
            tt.time('draw')

            sleep = 0.01
            await curio.sleep(self.sleep)
            tt.time('sleep')

            #print(tt.stats())



def get_parser():

    parser = argparse.ArgumentParser()

    parser.add_argument('--pig', action='store_true')
    parser.add_argument('--minutes', type=int, default=30)

    return parser

def main(args=None):
    """ Retrieve images currently available 

    There are usually six images available from the last half hour.
    """

    parser = get_parser()
    args = parser.parse_args()

    if args.pig:
        import sys
        farm = pigfarm.PigFarm()
        farm.add(TankRain)
        pigfarm.run(farm)
        sys.exit()
                  
    minutes = args.minutes

    images = defaultdict(list)

    aminute = datetime.timedelta(minutes=1)

    timestamp = utcnow()

    iurls = dict(
        local  = dict(url=url + radar_template,
                      size=100),
        wide   = dict(url=url + radar_template,
                      size=250),
        parish = dict(url=url + parish_template,
                      size=0),
    )

    # make timestamp an even minute
    if timestamp.minute % 2:
        timestamp -= aminute

    end = timestamp - (minutes * aminute)
    while timestamp > end:

        try:
            for name, data in iurls.items():
                iurl = data['url'].format(date=timestamp,
                                         size=data['size'])
                image = requests.get(iurl)
                piurl = Path(iurl)
                print(iurl)

                if image.status_code == requests.codes.ALL_OK:
                    images[name].append(dict(image=image.content,
                                            time=timestamp,
                                            suffix=piurl.suffix))

        except Exception as e:
            raise e
        
        timestamp -= (2 * aminute)

    
    for name, items in images.items():
        for item in items:
            date = item['time']
            image = item['image']
            suffix = item['suffix']

            path = Path(target.format(
                date=date,
                suffix=suffix,
                name=name))

            print('Creating', path)
            path.parent.mkdir(exist_ok=True, parents=True)

            with path.open('wb') as outfile:
                outfile.write(image)


if __name__ == '__main__':
    # Radar
                    
    main() 
    

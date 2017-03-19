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

from karmapi import pigfarm, checksum


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

        self.add_event_map('r', self.reverse)
        self.add_event_map(' ', self.next_view)

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


    async def next_view(self):

        switch = dict(
            wide='local',
            local='parish',
            parish='wide')
        
        self.version = switch[self.version]
        
        self.load_images()

    async def reverse(self):

        self.inc *= -1

    async def start(self):
        """ FIXME: get yoser to run fetch """
        #farm.yosser.run(fetch, minutes=20, sleep=300)
        pass

    async def run(self):

        self.dark()
        while True:

            self.compute_data()
            self.axes.clear()
            self.axes.imshow(self.data)


            self.draw()

            await curio.sleep(self.sleep)



async def fetch_part(name, data, minutes=30, timewarp=None):

    timewarp = datetime.timedelta()

    #FIXME adjust for timewarp
    
    timestamp = utcnow()

    timestamp += timewarp
    
    aminute = datetime.timedelta(minutes=1)
    
    # make timestamp an even minute
    if timestamp.minute % 1:
        timestamp -= aminute

    end = timestamp - (minutes * aminute)
    bad = set()
    checks = set()
    while timestamp > end:

        path = Path(target.format(
            date=timestamp,
            suffix='.png',
            name=name))

        path = Path('~/karmapi').expanduser() / path

        if not path.exists() and str(path) not in bad:

            # FIXME get a timewarp from the target.  Parish is on GMT
            #if parish:
            #    timewarp += parish_timewarp 

            print('looking for', path)
            # need to fetch it
            iurl = data['url'].format(
                date=timestamp,
                size=data['size'])

            
            # fixme -- await an async http call
            image = requests.get(iurl)

            if image.status_code == requests.codes.ALL_OK:
                # Save the imabe
                # checksum the data
                check = hash(image.content)
                if check in checks:
                    print('dupe', path)
                else:
                    print('GOT', path)
                    path.parent.mkdir(exist_ok=True, parents=True)
                    path.open('wb').write(image.content)
            else:
                print('bad', path)
                bad.add(str(path))
            
        timestamp -= (2 * aminute)

        
async def fetch(minutes=30, sleep=300):
    """ Download images """
    iurls = dict(
        local  = dict(url=url + radar_template,
                      size=100),
        wide   = dict(url=url + radar_template,
                      size=250),
        parish = dict(url=url + parish_template,
                      size=0),
    )


    while True:
        for name, data in iurls.items():
            
            await fetch_part(name, data, minutes)
        await curio.sleep(300)
                

def main(args=None):
    """ Retrieve images currently available 

    There are usually six images available from the last half hour.
    """

    parser = argparse.ArgumentParser()

    parser.add_argument('--pig', action='store_true')
    parser.add_argument('--minutes', type=int, default=30)

    args = parser.parse_args()

    if args.pig:
        farm = pigfarm.PigFarm()
        farm.add(TankRain)

        from karmapi.mclock2 import GuidoClock
        farm.add(GuidoClock)

        pigfarm.run(farm)
        sys.exit()
    else:
        curio.run(fetch(args.minutes))

if __name__ == '__main__':
    # Radar
                    
    main() 
    

""" I + git

tank rain for git browsing

"""

import itertools
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
url = '.'

target = None


class TankRain(pigfarm.MagicCarpet):
    """ Widget to show tankrain images """

    def __init__(self, parent, path=None, version='local', date=None, *args):
        
        self.version = version
        self.path = path or '~/karmapi/tankrain'
        self.timewarp = 0
        self.date = date
        if self.date is None:
            self.date = utcnow()

        self.load_images()

        super().__init__(parent, axes=[111])

        self.add_event_map('r', self.reverse)
        self.add_event_map(' ', self.next_view)

        self.add_event_map('b', self.previous_day)
        self.add_event_map('v', self.next_day)

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
        date = self.date + datetime.timedelta(seconds=self.timewarp)
        path = Path(f'{self.path}/{date.year}/{date.month}/{date.day}/').expanduser()

        print(f'loading images for path: {path} v{self.version}v')

        jpegs = path.glob('{}*.[jp][np]g'.format(self.version))
        gifs = path.glob('{}*.gif'.format(self.version))
        
        for image in sorted(itertools.chain(jpegs, gifs)):
    
            if image.stat().st_size == 0:
                continue
            print(image)
            yield image


    async def next_view(self):

        switch = dict(
            wide='local',
            local='parish',
            parish='wide')

        # no versions, don't switch
        switch[''] = ''
        
        self.version = switch[self.version]
        
        self.load_images()

    async def previous_day(self):

        self.timewarp -= 24 * 3600

        self.load_images()

    async def next_day(self):

        self.timewarp += 24 * 3600
        self.load_images()

    async def reverse(self):

        self.inc *= -1

    async def start(self):
        """ FIXME: get yoser to run fetch """
        #farm.yosser.run(fetch, minutes=20, sleep=300)
        pass

    async def run(self):

        # use yosser?
        await pigfarm.aside(runfetch)

        self.dark()
        while True:

            #title = self.paths[self.ix]
            if self.paths:
                title = self.paths[self.ix]
            else:
                title = f'{self.ix} : {len(self.paths)} {self.path}'
            
            self.compute_data()
            self.axes.clear()
            print('TITLE:', title)
            try:
                self.axes.set_title(title)
                self.axes.imshow(self.data)
            except OSError:
                print('dodgy image:', self.paths[self.ix])


            self.draw()

            await curio.sleep(self.sleep)



async def fetch_part(name, data, minutes=30, timewarp=None, bad=None):

    timewarp = datetime.timedelta()

    #FIXME adjust for timewarp
    bad = bad or set()
    
    timestamp = utcnow()

    timestamp += timewarp
    
    aminute = datetime.timedelta(minutes=1)
    
    # make timestamp an even minute
    # if timestamp.minute % 2:
    #     timestamp -= aminute

    end = timestamp - (minutes * aminute)
    checks = set()

    while timestamp > end:
        timestamp -= aminute

        path = Path(target.format(
            date=timestamp,
            suffix='.png',
            name=name))

        path = Path('~/karmapi').expanduser() / path

        if path.exists():
            print('already got', timestamp, name)
            continue

        if str(path) in bad:
            print('skipping bad', timestamp, name)
            continue

        # FIXME get a timewarp from the target.  Parish is on GMT
        #if parish:
        #    timewarp += parish_timewarp 

        print('looking for', timestamp, name)
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
                print('dupe', timestamp, name)
            else:
                print('GOT', timestamp, name)
                path.parent.mkdir(exist_ok=True, parents=True)
                path.open('wb').write(image.content)
        else:
            bad.add(str(path))
            print('bad', path, len(bad))

            
        print()

async def runfetch():

    await fetch()

    
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
        bad = set()
        for name, data in iurls.items():
            
            await fetch_part(name, data, minutes, bad)

            # FIXME -- shrink bad from time to time
            
        await curio.sleep(300)


def main(args=None):
    """ Retrieve images currently available 

    There are usually six images available from the last half hour.
    """

    parser = argparse.ArgumentParser()

    parser.add_argument('--pig', action='store_false', default=True)
    parser.add_argument('--minutes', type=int, default=30)
    parser.add_argument('path', nargs='?', default='~/karmapi/tankrain')
    parser.add_argument('--version', default='')
    parser.add_argument('--date')
                            
    args = parser.parse_args()

    args.date = base.parse_date(args.date)

    if args.pig:
        farm = pigfarm.PigFarm()
        farm.add(
            TankRain,
            dict(path=args.path, version=args.version, date=args.date))

        from karmapi.mclock2 import GuidoClock
        farm.add(GuidoClock)

        pigfarm.run(farm)
        sys.exit()
    else:
        curio.run(fetch(args.minutes))

if __name__ == '__main__':
    # Radar
                    
    main() 
    

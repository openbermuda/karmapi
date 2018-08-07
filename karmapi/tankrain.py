""" Bermuda weather


Or at least that is how it started.

Download and view Bermuda Weather radar.

tankrain being heavy rains that fill the water tanks beneath Bermuda homes.

Now it has morphed into an image viewer.

Sort your image into folders by year month day

Tankrain will let you navigate.

It also works for viewing models and data.

Just store the images for each day.
"""
import itertools
import argparse
import random

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

target = 'tankrain/{date.year}/{date.month}/{date.day}/{name}_{date:%H%M}{suffix}'


class TankRain(pigfarm.MagicCarpet):
    """ Widget to show tankrain images """

    def __init__(self, parent, path=None, version='local', date=None,
                 save=None, *args):
        
        self.version = version
        self.paused = False
        self.path = path or '.'
        self.save_folder = save
        self.timewarp = 0
        self.cut = 0
        self.date = date
        if self.date is None:
            self.date = utcnow()

        self.title = 'k'

        self.load_images()

        super().__init__(parent, axes=[111])

        self.add_event_map('r', self.reverse)
        self.add_event_map(' ', self.pause)

        self.add_event_map('b', self.previous_day)
        self.add_event_map('v', self.next_day)

        self.add_event_map('l', self.fewer_images)
        self.add_event_map('m', self.more_images)
        self.add_event_map('X', self.switcheroo)
        self.add_event_map('S', self.save)
        self.add_event_map('T', self.toggle_title)

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

        n = len(self.paths)
        ix = ix + self.inc
        if ix >= n:
            ix = self.cut
        if ix < 0:
            ix = len(self.paths) - 1
            
        self.ix = ix
                            
        self.data = im


    def when(self):
        """ current date """
        date = self.date + datetime.timedelta(seconds=self.timewarp)

        return date

    def where(self, when=None, path=None):
        """ Path for date """
        date = when or self.when()

        path = path or self.path
        path = Path(f'{path}/{date.year}/{date.month}/{date.day}/').expanduser()

        return path


    def get_images(self, when=None, path=None):

        # FIXME -- create key bindings to select time
        date = when or self.when()
        path = self.where(date)

        print(f'loading images for path: {path} v{self.version}v')

        jpegs = path.glob('{}*.[jp][np]g'.format(self.version))
        gifs = path.glob('{}*.gif'.format(self.version))
        
        for image in sorted(itertools.chain(jpegs, gifs)):
    
            if image.stat().st_size == 0:
                continue
            print(image)
            yield image


    async def save(self):
        """ Save image somewhere else

        This one saves the current data, not the PIL file
        so can be used to make transforms along the way.
        """
        # save relative to cwd
        target = self.where(self.when(), self.save_folder or '.')


        target /= self.paths[self.ix].name
        # fixme -- where's the path
        print('saving to', target)
        target.parent.mkdir(parents=True, exist_ok=True)
        self.data.save(target)

    async def switcheroo(self):
        """ switcheroo
        
        Swap images with those for previous day 

        """
        current = self.when()
        previous = current - datetime.timedelta(days=1)

        cfolder = self.where(current)
        pfolder = self.where(previous)

        # Get the lists of image names before we start moving things around
        cimages = list(self.get_images(current))
        pimages = list(self.get_images(previous))
        print('switcheroo time')
        print(cimages)
        print(pimages)

        for image in cimages:
            image.rename(pfolder / image.name)

        for image in pimages:
            image.rename(cfolder / image.name)

        self.load_images()


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
        """ previous day """
        self.timewarp -= 24 * 3600
        self.set_for_day()

    async def next_day(self):
        """ next day """
        self.timewarp += 24 * 3600
        self.set_for_day()

    def set_for_day(self):
        self.paused = False
        self.cut = 0
        self.load_images()

    async def reverse(self):
        """ Rongo Rongo change direction """
        self.paused = False
        self.inc *= -1

    async def pause(self):
        """ pause the show """
        self.paused = not self.paused

    async def fewer_images(self):
        """ Skip some images """
        self.inc = int(self.inc * 2)
        self.cut = self.ix % abs(self.inc)


    async def more_images(self):
        """ Show more images """
        if abs(self.inc) > 1:
            self.inc = int(self.inc / 2)

        self.cut = self.ix % abs(self.inc)

    async def toggle_title(self):
        """ toggle titles """
        if self.title == 'k':
            self.title = 'gold'
        else:
            self.title = 'k'

    async def start(self):
        """ FIXME: get yosser to run? """
        #farm.yosser.run(fetch, minutes=20, sleep=300)
        
        pass

    async def run(self):

        # use yosser?  ironically awaiting yosser
        #await pigfarm.aside(runfetch)

        self.dark()
        while True:
            if self.paused:
                await curio.sleep(self.sleep)
                continue

            if self.paths:
                title = self.paths[self.ix]
            else:
                title = f'{self.ix} : {len(self.paths)} {self.path}'

            self.compute_data()
            self.axes.clear()
            print('TITLE:', title)
            try:
                #self.axes.set_title(title, color=self.title)
                self.axes.set_title(title, color=self.title or 'k')
                
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
    parser.add_argument('path', nargs='?', default='.')
    parser.add_argument('--version', default='')
    parser.add_argument('--save',
                        help='folder to save to')

    parser.add_argument('--date')
                            
    args = parser.parse_args()

    args.date = base.parse_date(args.date)

    if args.pig:
        farm = pigfarm.PigFarm()
        farm.add(
            TankRain,
            dict(path=args.path, version=args.version, date=args.date,
                 save=args.save))

        from karmapi.mclock2 import GuidoClock
        farm.add(GuidoClock)

        pigfarm.run(farm)
        sys.exit()
    else:
        curio.run(fetch(args.minutes))

if __name__ == '__main__':
    # Radar
                    
    main() 
    

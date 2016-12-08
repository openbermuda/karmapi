""" Bermuda weather
"""
import argparse

import datetime
utcnow = datetime.datetime.utcnow

from urllib.error import HTTPError

from pathlib import Path

from collections import defaultdict

from karmapi import show

from karmapi import pig

# Paths to data
url = 'http://weather.bm/images/'

radar_template = 'Radar/CurrentRadarAnimation_{size}km_sri/{date:%Y-%m-%d-%H%M}_{size}km_sri.png'
parish_template = 'Radar/RadarParish/{date:%Y-%m-%d-%H%M}_ParishRadar.png'

atlantic_chart = 'surfaceAnalysis/Latest/Atlantic.gif'
local_chart = 'surfaceAnalysis/Latest/Local.gif'

target = 'tankrain/{date:%Y}/{date:%m}/{date:%d}/{name}_{date:%H%M}{suffix}'

def meta():
    """ Generate pig gui description for tankrain """
    info = dict(
        title = "PIGS",
        info = dict(foo=27, bar='open'),
        parms = [{'label': 'path'}],
        tabs = [
            {'name': 'parish',
             'widgets': [[TankRain]]},
            {'name': 'local',
             'widgets': [[TankRain]]},
            {'name': 'wide',
             'widgets': [[TankRain]]},
            {'name': 'yosser'}]) 
    return info
    

class TankRain(pig.Video):
    """ Widget to show tankrain images """

    def __init__(self, *args):
        
        self.ix = 0
        self.paths = [x for x in self.images()]
        print(self.paths)
        
        super().__init__(0.1)


    def compute_data(self):

        from PIL import Image

        ix = self.ix

        if ix < len(self.paths):
            im = Image.open(self.paths[ix])
        else:
            im = [list(range(10)) for x in range(10)]
        
        ix = ix + 1
        if ix == len(self.paths):
            ix = 0
        self.ix = ix
                            
        self.data = im

    def images(self):
        path = Path('tankrain/2016/10/12')

        
        for image in path.glob('local*.png'):
            yield image
            



class ParishImage(TankRain):

    def compute_data(self):

        # for now, no idea
        super().compute_data()

        # pick a time?

        # base.load(path)

        # increment time

class LocalImage(ParishImage):
    pass

class WideImage(LocalImage):
    pass


def get_parser():

    parser = argparse.ArgumentParser()

    parser.add_argument('--pig', action='store_true')
    parser.add_argument('--minutes', type=int, default=30)

    return parser

def run_pig():

    app = pig.build(meta())

    pig.run(app)

def main(args=None):
    """ Retrieve images currently available 

    There are usually six images available from the last half hour.
    """

    parser = get_parser()
    args = parser.parse_args()

    if args.pig:
        run_pig()
                  
    minutes = args.minutes

    size = 250

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
                image = show.load(iurl)
                piurl = Path(iurl)
                print(iurl)
                images[name].append(dict(image=image,
                                         time=timestamp,
                                         suffix=piurl.suffix))
        except HTTPError as e:
            #print('missing:', timestamp)
            pass

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

            show.save(str(path), image)


if __name__ == '__main__':
    # Radar
                    
    main() 
    

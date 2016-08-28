""" Bermuda weather
"""
import argparse

import datetime
utcnow = datetime.datetime.utcnow

from urllib.error import HTTPError

from pathlib import Path

from collections import defaultdict

from karmapi import show

# Paths to data
url = 'http://weather.bm/images/'

radar_template = 'Radar/CurrentRadarAnimation_{size}km_sri/{date:%Y-%m-%d-%H%M}_{size}km_sri.png'
parish_template = 'Radar/RadarParish/{date:%Y-%m-%d-%H%M}_ParishRadar.png'

atlantic_chart = 'surfaceAnalysis/Latest/Atlantic.gif'
local_chart = 'surfaceAnalysis/Latest/Local.gif'

target = 'tankrain/{date:%Y}/{date:%m}/{date:%d}/{name}_{date:%H%M}{suffix}'

def get_parser():

    parser = argparse.ArgumentParser()

    parser.add_argument('--minutes', type=int, default=30)

    return parser

def main(args=None):
    """ Retrieve images currently available 

    There are usually six images available from the last half hour.
    """

    parser = get_parser()
    args = parser.parse_args()
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
    

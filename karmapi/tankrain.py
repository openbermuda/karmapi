""" Bermuda weather
"""
import datetime

from karmapi import show

# Paths to data
url = 'http://weather.bm/images/'

radar_template = 'Radar/CurrentRadarAnimation_{size}km_sri/{date:%Y-%m-%d-%H%M}_{size}km_sri.png'
parish_template = 'Radar/RadarParish/{date:%Y-%m-%d-%H%M}_ParishRadar.png'

atlantic_chart = 'surfaceAnalysis/Latest/Atlantic.gif'
local_chart = 'surfaceAnalysis/Latest/Local.gif'

def get_images(now, template):
    """ Retrieve images currently available 

    There are usually six images available from the last half hour.
    """
    pass


if __name__ == '__main__':
    # Radar
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

    end = timestamp - (30 * aminute)
    while timestamp > (end - (30 * aminute)):

        try:
            for name, data in iurls.items():
                iurl = data['url'].format(date=timestamp,
                                         size=data['size'])
                image = show.load(iurl)
                print(iurl)
                images[name].append(image)
        except:
            print('missing:', timestamp)
            pass
        timestamp -= (2 * aminute)

    print(len(images))
    

"""
Explorations in Ottawa weather data

Data thanks to environment Canada

http://climate.weather.gc.ca/radar/index_e.html

"""
import requests

URL = "http://climate.weather.gc.ca/radar/index_e.html"

URL = "http://climate.weather.gc.ca/radar/image_e.html?time=07-OCT-18+01.06.42.405345+PM\&site=XFT"

PARMS = dict(
    site='XFT',
    year=2018,
    month=10,
    day=7,
    hour=12,
    minute=50,
    duration=2,
    image_type='PRECIPET_RAIN_WEATHEROFFICE',
    image=1)

TURL = "http://climate.weather.gc.ca/radar/image_e.html?time=07-OCT-17+01.00.33.755554+PM&site=XFT"

ITIMES =  [
        '/radar/image_e.html?time=07-OCT-17+01.00.33.755554+PM&site=XFT'
        '/radar/image_e.html?time=07-OCT-17+01.10.31.151260+PM&site=XFT',
        '/radar/image_e.html?time=07-OCT-17+01.20.28.146381+PM&site=XFT',
        '/radar/image_e.html?time=07-OCT-17+01.30.41.084535+PM&site=XFT',
        '/radar/image_e.html?time=07-OCT-17+01.40.36.764073+PM&site=XFT',
        '/radar/image_e.html?time=07-OCT-17+01.50.31.739783+PM&site=XFT',
        '/radar/image_e.html?time=07-OCT-17+02.00.28.468690+PM&site=XFT',
        '/radar/image_e.html?time=07-OCT-17+02.10.42.567798+PM&site=XFT',
        '/radar/image_e.html?time=07-OCT-17+02.20.55.146242+PM&site=XFT',
        '/radar/image_e.html?time=07-OCT-17+02.30.42.623817+PM&site=XFT',
        '/radar/image_e.html?time=07-OCT-17+02.51.12.647761+PM&site=XFT',
        '/radar/image_e.html?time=07-OCT-17+02.50.57.567531+PM&site=XFT',
        '/radar/image_e.html?time=07-OCT-17+03.00.42.884564+PM&site=XFT',
      ]

def find_images(data):

    dump = False
    for row in data.split('\n'):
        if dump:
            print(row)
        if row.startswith('blobArray'):
            dump = True

if __name__ == '__main__':

    #print(help(requests.get))

    result = requests.get(URL, PARMS)

    print(result)
    print(type(result.content))
    print(len(result.content))
    find_images(result.content)

    1/0
    print(result.content.decode())

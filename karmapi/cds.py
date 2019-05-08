"""
Coppernicus data service interface
"""

import cdsapi

c = cdsapi.Client()

years = [
            '1979','1980','1981',
            '1982','1983','1984',
            '1985','1986','1987',
            '1988','1989','1990',
            '1991','1992','1993',
            '1994','1995','1996',
            '1997','1998','1999',
            '2000','2001','2002',
            '2003','2004','2005',
            '2006','2007','2008',
            '2009','2010','2011',
            '2012','2013','2014',
            '2015','2016','2017',
            '2018'
        ]


months = ['%02d' % x for x in range(1, 13)]

days = ['%02d' % x for x in range(1, 32)]

times = ['%02d:00' % x for x in range(0, 24)]

years = ['1979']
months = ['01']
days = ['01']

print(years)
print(months)
print(days)
print(times)

c.retrieve(
    'reanalysis-era5-single-levels',
    {
        'product_type':'reanalysis',
        'format':'grib',
        'variable':[
            '2m_temperature','total_precipitation'
        ],
        'year': years,
        'month': months,
        'day': days,
        'time':[
            '00:00','01:00','02:00',
            '03:00','04:00','05:00',
            '06:00','07:00','08:00',
            '09:00','10:00','11:00',
            '12:00','13:00','14:00',
            '15:00','16:00','17:00',
            '18:00','19:00','20:00',
            '21:00','22:00','23:00'
        ]
    },
    'download.grib')


# coding: utf-8

# In[27]:

get_ipython().magic('matplotlib inline')
import sys
import os
import numpy
import struct
sys.path.append(os.path.expanduser("~/jng/sunshine/noddy"))


# In[2]:

import weather
from datetime import date, timedelta


# In[3]:

ls -al ../*.gz


# In[4]:

ls -al


# In[5]:

data = weather.get_data(date(1979,1,1), open('tmax.csv'))


# In[6]:

def tonumpy(data):
    
    ndata = numpy.array([float(x) for x in data.split()])
    ndata = ndata.reshape(weather.longitudes(), weather.latitudes()).T
    return ndata


# In[7]:

from matplotlib import pyplot


# In[8]:

data = tonumpy(data)
pyplot.imshow(data)


# In[9]:

get_ipython().system('mkdir euro')


# In[10]:

# mmake some directories
delta = weather.DELTA
lon = weather.LONGITUDE_START
for ix in range(weather.longitudes()):
    folder = 'euro/{}'.format(lon)
    
    try:
        os.makedirs(folder) 
    except:
        pass
    
    lat = weather.LATITUDE_START
    for ix in range(weather.latitudes()):
    
        folder = 'euro/{}/{}'.format(lon, lat)
    
        try:
            os.makedirs(folder)
        except:
            pass
        
        lat -= delta
    lon += delta


# In[15]:

pyplot.plot(data[:,30])


# In[99]:

# open a file for each lon
lons = numpy.linspace(weather.LONGITUDE_START, 360.0, weather.longitudes())

lons = get_ipython().getoutput('ls euro')

outfiles = [open('euro/{}/tmax'.format(x), 'ab') for x in lons]


# In[55]:

def write_day(data, date, outfiles):

    packer = struct.Struct('{}f'.format(weather.latitudes()))

    for ix in range(weather.longitudes()):
    
        col = data[:, ix]
        pdata = packer.pack(*col)
    
        outfiles[ix].write(pdata)

    


# In[61]:

def process_days(start, end, infile, outfiles):
    
    day = start
    while day < end:
        if day.day == 1: print(day)
        data = tonumpy(weather.get_data(day, infile))
        
        write_day(data, date, outfiles)
        
        day += timedelta(days=1)


# In[100]:

infile = open('tmax.csv')
process_days(date(1989,1,1), date(2016,1,1), infile, outfiles)


# In[101]:

for out in outfiles: out.close()


# In[83]:

# get data for a lat lon
def lat_lon(lat, lon, value='tmax'):
    
    # read all data for lon
    infile = "euro/{lat}/{value}".format(**locals())
    
    data = open(infile, 'rb').read()
    
    print(len(data)/4)
    
    unpack = struct.Struct('{}f'.format(int(len(data)/4)))
    
    return unpack.unpack(data)


# In[102]:

data = lat_lon(0.0, 0.0)


# In[103]:

d = data[170::241]


# In[104]:

pyplot.plot(d)


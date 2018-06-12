"""
Hush: separates the signal from the noise.

For now this is about getting a signal: a stream of sound frames to analyse.

Things to do:

Look at pyaudio, does it already know about async?

This looks interesting:

https://github.com/lemonzi/VoCoMi

And this seems to have solved a lot of problems nicely:

https://github.com/lemonzi/VoCoMi/nuance.py

For now, goal is sonograms: pictures of the sound as it goes by.

This uses hmm and does feature extraction and more:

https://github.com/tyiannak/pyAudioAnalysis



Update: back after a long absense.
 

OK.  So I have some .wav files I want to process and use with the rest of the
karma that is here.

But there are a lot of pieces to juggle around here.

I want to use the tpot.

Here's the idea.

Take a poor quality recording of me playing the guitar and turn it into
something Carlos Santana might do while he's tying shoe laces.

So I'm more Carlisle Sultana than Carlos, so this might take a while.

Less ambitious goal?  Beware if it sounds easy ...  remember the black hole of
code.  Did I mention the black hole is actually made of spaghetti code?  

All the failed *next generation* projects for the last generation, this is just
one of the holes out there.

The cool thing is that due to modern version control a code base can easily
belong to multiple black holes simultaneously.   

Of course a lot of this stuff is actually out there in the wild, but that is a
whole other problem.

Did I mention I digress?

So the other goal is to be able to control tankrain with a guitar.

And the teapot might just help with that.  Guess the state, bind the state to
actions for tankrain.

Oh and update.  Laptop has a mic, so can do the recording with hush.

And now I am having dega code

its deja vu for you know you have an idea you want to pursue and remember
solving the problem before (the problem in this case being reading and writing
files).

But the problem here is files with a special sound format.  And then of course
you realise this is the place where you did it last time.

Time to see if any of it still works.

karma currie time to be exact.
"""
from datetime import datetime
import math

import curio

import struct

from collections import defaultdict

import time

from matplotlib import pyplot

try:
    import pyaudio
    FORMAT = pyaudio.paInt16
except:
    FORMAT = None

import wave
import numpy as np

from karmapi import base

CHUNK = 1024 * 4
#CHUNK = 256 * 1
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5


def bytestoshorts(data):

    n = len(data) / 2
    return struct.unpack('%dh' % n, data)


def get_stream():

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    return stream


def record(stream):

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    return frames


def decode(frame, channel=0, channels=2, samplesize=2):
    """ Decode frame and return data for given channel """
    bytes_per_record = channels * samplesize


    data = [int(x) for x in frame]

    low = [x + 128 for x in data[1::1]]
    high = [x * 256 for x in data[0::1]]

    fixed = []
    for x, y in zip(high, low):

        fixed.append(x + y)

    return fixed


def bytestreams(frame, channels=4):

    data = {}

    frame = [int(x) for x in frame]

    for channel in range(channels):

        data['c%d' % channel] = frame[channel::channels]

    return data

class Connect:
    """ Connect to a stream

    Provides a co-routine to allow aysnchronous putting of data frames into a queue.

    await get() and you can pop stuff off the queue
    """


    def __init__(self, mick = None, *args, **kwargs):
        """ Fixme: configure stream according to **kwargs """

        if mick is None:
            self.mick = get_stream()
        else:
            self.mick = mick

        self.queue = curio.UniversalQueue(maxsize=2)

        self.tt = base.Timer()

    def rate(self):

        return self.mick._rate

    def frame_size(self):

        return self.mick._frames_per_buffer

    async def start(self):
        """ Keep reading frames, add them to the queue """

        rate = 0
        start = datetime.now()
        while True:
            self.tt.time()

            self.tt.time('read')
            data, timestamp = self.read()

            if (timestamp - start).seconds > 0:
                print('framerate', rate)
                rate = 0
                start = timestamp

            rate += 1
            

            self.tt.time('decode')
            await self.queue.put((data, timestamp))
            self.tt.time('put')


    def read(self, chunk=CHUNK, decode=True):

        timestamp = datetime.now()
        data = self.mick.read(chunk)
        if decode:
            data = self.decode(data)

        return data, timestamp

    async def get(self):

        self.tt.time('junk2')
        result = await self.queue.get()
        self.tt.time('get')

        return result

    def decode(self, data):

        return bytestoshorts(data)


class Wave:
    """ Create a sine wave for sound """


    def __init__(self, mode = None, scale=50, *args, **kwargs):
        """ Fixme: configure stream according to **kwargs """

        self.queue = curio.UniversalQueue(maxsize=2)
        self.sleep = 0.01

        n = 2 * CHUNK

        data = self.sine_wave(n)

        if mode == 'square':
            data = self.sine_to_square(data)
            
        self.data = data

    def sine_to_square(self, data):
        maxval = (2 ** 15) - 1

        square = []
        for x in data:
            if x > 0:
                square.append(maxval)
            else:
                square.append(-maxval)
        return square

    
    def sine_wave(self, n):

        data = np.arange(n)
        data = np.sin(data * math.pi / 50.0) * (2**15 - 1)

        return data


    def rate(self):
        """ FIXME """
        return 44100

    def frame_size(self):
        """ FIXME -- make this work with CHUNK """
        return 1024

    async def start(self):
        """ Keep reading frames, add them to the queue """

        while True:
            timestamp = datetime.now()
            await self.queue.put((self.data, timestamp))
            await curio.sleep(self.sleep)

    async def get(self):

        data = await self.queue.get()

        return data


class FreqGen:

    def __init__(self):

        self.mick = Connect()


    async def start(self):

        await curio.spawn(self.mick.frames())

        rate = self.mick.rate()
        frames = self.mick.frame_size()


        while True:

            data, timestamp = await self.mick.get()

            data = self.mick.decode(data)
            sono = base.fft.fft(data[:int(len(data)/2)])


            power = abs(sono)

            xx = np.argmax(power)

            hertz = (xx / frames) * rate * 0.5

            print('{} {}'.format(timestamp, hertz))


def open_wave(name):

    wf = wave.open(name, 'rb')

    # monkey patch
    wf.read = wf.readframes

    return wf


async def write(connect, outfile):
    
    while True:
        
        data, timestamp = await connect.get()
        print('got data', timestamp)

        # FIXME -- use aiofiles?
        outfile.write(data)

        
async def arecord(outfile):

    connect = Connect()

    # set the connection to start collecting frames
    frames = await curio.spawn(connect.start(decode=False))

    writer = await curio.spawn(write(connect, outfile))

    await writer.join()
    

async def run():
    """ Run this thing under curio  

    FIXME -- make it do something useful
    """

    connect = Connect()

    # set the connection to start collecting frames
    frames = await curio.spawn(connect.frames())

    while True:

        data = await connect.get()


def main(args=None):

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--outfile', default='out.hush')
    parser.add_argument('--record', action='store_true')
    parser.add_argument('--infile')
    parser.add_argument('--nomick', action='store_true')
    
    args = parser.parse_args(args)

    if args.record:
        curio.run(arecord(open(args.outfile, 'wb')))
        return
    
    from karmapi import sonogram
    from karmapi import pigfarm


if __name__ == '__main__':

    main()

            

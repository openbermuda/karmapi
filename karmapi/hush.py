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

"""
from datetime import datetime
import math

import curio

from matplotlib import pyplot
import struct

import pyaudio
import wave
import numpy as np

from karmapi import base

CHUNK = 1024 * 4
FORMAT = pyaudio.paInt16
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

    def rate(self):

        return self.mick._rate

    def frame_size(self):

        return self.mick._frames_per_buffer

    async def start(self):
        """ Keep reading frames, add them to the queue """

        rate = 0
        start = datetime.now()
        while True:
            timestamp = datetime.now()

            if (timestamp - start).seconds > 0:
                rate = 0
                start = timestamp

            rate += 1

            data = self.mick.read(CHUNK)
            rate += 1
            await self.queue.put((self.decode(data), timestamp))


    async def read(self, chunk):

        return self.mick.read(chunk)

    async def get(self):

        return await self.queue.get()


    def decode(self, data):

        return bytestoshorts(data)


class Wave:
    """ Create a sine wave for sound """


    def __init__(self, mode = None, scale=50, *args, **kwargs):
        """ Fixme: configure stream according to **kwargs """

        self.queue = curio.UniversalQueue(maxsize=2)

        n = 2 * CHUNK

        if mode == 'square':
            frames = int(n / 32)
            plus = [3000] * 16
            minus = [-3000] * 16
            data = (plus + minus) * frames
        else:
            data = np.arange(n)
            data = np.sin(data * math.pi / 50.0) * (2**15 - 1)

        print('xxxxxxxxxxxxxxxxx', mode, len(data))

        self.data = data


    def rate(self):

        return 44100

    def frame_size(self):

        return 1024

    async def start(self):
        """ Keep reading frames, add them to the queue """

        while True:
            timestamp = datetime.now()
            await self.queue.put((self.data, timestamp))


    async def get(self):

        data = await self.queue.get()

        return data


async def run():
    """ Run this thing under curio  """

    connect = Connect()

    # set the connection to start collecting frames
    frames = await curio.spawn(connect.frames())

    while True:

        data = await connect.get()


def open_wave(name):

    wf = wave.open(name, 'rb')

    # monkey patch
    wf.read = wf.readframes

    return wf


def main():



    curio.run(run(), with_monitor=True)


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

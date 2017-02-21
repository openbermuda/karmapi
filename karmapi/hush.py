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
import curio

from matplotlib import pyplot
import struct

import pyaudio
import wave
import numpy as np

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"


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

        self.queue = curio.UniversalQueue(maxsize=20)

    async def frames(self):
        """ Keep reading frames, add them to the queue """

        while True:
            timestamp = datetime.now()
            data = await self.read(CHUNK)

            await self.queue.put((data, timestamp))


    async def read(self, chunk):

        return self.mick.read(chunk)

    async def get(self):

            
        data = await self.queue.get()

        return data

    def decode(self, data):
    
        return bytestoshorts(data)
        

async def run():
    """ Run this thing under curio  """
    
    connect = Connect()
    print(connect.mick)

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




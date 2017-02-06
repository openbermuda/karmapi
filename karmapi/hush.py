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
import curio

from matplotlib import pyplot
import pyaudio
import numpy as np

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

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


def decode(frame):

    data = [int(x) for x in frame]

    fixed = []
    for x in data:
        if x > 128:
            x -= 256
        fixed.append(x)
    
    return fixed

class Connect:
    """ Connect to a stream 

    Provides a co-routine to allow aysnchronous putting of data frames into a queue.

    await get() and you can pop stuff off the queue.
    """


    def __init__(self, *args, **kwargs):
        """ Fixme: configure stream according to **kwargs """

        self.mick = get_stream()

        self.queue = curio.UniversalQueue()

    async def frames(self):
        """ Keep reading frames, add them to the queue """

        while True:
            data = await self.read(CHUNK)

            await self.queue.put(data)


    async def read(self, chunk):

        return self.mick.read(chunk)

    async def get(self):

            
        data = await self.queue.get()

        return data

    def decode(self, data):

        return decode(data)
        
async def run():
    """ Run this thing under curio  """
    
    connect = Connect()
    print(connect.mick)

    # set the connection to start collecting frames
    frames = await curio.spawn(connect.frames())

    while True:

        data = await connect.get()

        print('got data:', len(data))
    
def main():

    

    curio.run(run(), with_monitor=True)




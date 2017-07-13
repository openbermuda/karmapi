"""
Sense Hat tools

Work in progress...

FIXME:  

  Save hat data in year/month/day folders.

      weather:  csv file of weather related readings
      compass:  compass readings
      gyro:     gyro readings
      acceleration:  data from accelerometer

  Add timestamp to each record. 

  make the hat a mike?

  have some sort of record executable that can be run (eg at boot) to start recording data

  Once we have the data recording in place can just use MagicCarpet to view it.

"""
import subprocess
import datetime
from datetime import timedelta

import csv
import time
from pathlib import Path

import curio
import pandas

from karmapi import pigfarm, base

try:
    import sense_hat
except:
    # see if sense hat emulator is around
    import sense_emu as sense_hat


def stats(hat):
    while True:
        yield "T: %4.1f" % hat.temp
        yield "H: %4.1f" % hat.humidity
        yield "P: %4.0f" % hat.pressure
        yield "TP: %4.0f" % hat.get_temperature_from_pressure()
        yield "TH: %4.0f" % hat.pressure
        yield "P: %4.0f" % hat.pressure

def get_stats(hat):
    """ Return weather, compass and gyro data"""
    data = next(get_weather(hat))

    compass = next(get_compass(hat))
    data.update(compass)

    gyro = next(get_gyro(hat))
    data.update(gyro)

    return data

def get_weather(hat):

    while True:
        data = dict(
            humidity = hat.humidity,
            pressure = hat.pressure,
            
            temperature = (
                hat.get_temperature_from_pressure() +
                hat.get_temperature_from_humidity()) / 2.0,

            cpu_temperature = get_cpu_temperature())


        data['timestamp'] = time.time()

        yield data


def temperature_guess(data):

    guess = data['temperature_from_pressure'] + data['temperature_from_humidity']
    guess = guess / 2.0

    cputemp = data['cpu_temperature']

    guess = guess - ((cputemp - guess) / 2)

    return guess


def pressure_to_altitude(pressure, sealevel=1013.250):
    """ Converts pressure to height above sea level

    sealevel: optional actual pressure at sea level
    """
    pressure = 100.0 * pressure
    sealevel = 100.0 * sealevel
    
    altitude = 44330.0 * (1.0 - pow(pressure / sealevel, (1.0/5.255)))

    return altitude

def get_gyro(hat):

    while True:
        data = hat.gyro

        data['timestamp'] = time.time()

        yield data


def get_acceleration(hat):

    while True:
        data = hat.accel
    
        data['timestamp'] = time.time()

        yield data

def get_compass(hat):

    while True:
        data = hat.compass_raw
        data['compass'] = hat.compass
        data['timestamp'] = time.time()
        yield data

def get_cpu_temperature():

    result = subprocess.Popen('vcgencmd measure_temp'.split(),
                              stdout=subprocess.PIPE)

    data = result.stdout.read()

    return float(data[5:-3])

def show_all_stats(hat, show=None):

    if show is None:
        show = hat.show_message

    while True:
        stats = get_stats(hat)

        for key, value in stats.items():
            show("%s: %04.1f\n" % (key, value))

            

    
class Monitor(pigfarm.MagicCarpet):

    async def load_data(self):
        """ Reload data 

        This should periodically reload data.

        Create a dictionary keys being group, values df
        """
        while True:
            # do some magic here

            self.process_data()
        

def get_outfile(path, name):
    """ Open output file """
    path = Path(path)

    now = datetime.datetime.now()

    path = path / f'{now.year}' / f'{now.month}' / f'{now.day}' / name

    path.parent.mkdir(exist_ok=True, parents=True)

    if path.exists():
        # hmm... open in append, but then don't need a header
        header = False

        outfile = path.open('a')

        return header, outfile


    header = True
    return header, path.open('w')

        

def get_writer(path, name, data, sleep):

    # FIXME? maybe should read existing (if it exists) to get header line
    header = next(data).keys()

    # open outfile
    need_header, outfile = get_outfile(path, name)
    
    writer = csv.DictWriter(outfile, fieldnames=header)

    if need_header:
        writer.writeheader()
    
    return writer, outfile

async def recorder(path, name, data, sleep=1):
    """ Record from a sensor 

    path: base folder to put stuff
    name: the name for the values
    data: an iterator over dictionaries
    """

    writer, outfile = get_writer(path, name, data, sleep)

    try:
        while True:
            print('writing', name)
            writer.writerow(next(data))
            outfile.flush()
            await curio.sleep(sleep)
    except curio.CancelledError:
        outfile.close()


async def record(path='.', sleep=1, tasks=None, names=None, hat=None):
    """ Record everything from the hat """

    if hat is None:
        hat = sense_hat.SenseHat()

    weather = get_weather
    compass = get_compass
    gyro = get_gyro
    accel = get_acceleration

    if tasks is None:
        tasks = [weather, compass, gyro, accel]

    if names is None:
        names = ['weather', 'compass', 'gyro', 'accel']

    # magic from curio
    while True:

        now = datetime.datetime.now()
        midnight = timedelta(hours = 23 - now.hour,
                             minutes = 59 - now.minute,
                             seconds = 59 - now.second)

        print(now)
        print(now + midnight)
        # seconds to midnight + 1
        midnight = midnight.seconds + 1
        
        async with curio.timeout_after(midnight):
            async with curio.TaskGroup(wait='any') as workers:

                for task, name in zip(tasks, names):

                    await workers.spawn(recorder(path, name, task(hat), sleep))


def drop_bad_rows(infile):
    """ Take an input file and filter out bad data 

    Also change pressure to altitude.
    """
    line = next(infile)
    fields = [x.strip() for x in line.split(',')]

    null = chr(0)
    
    result = []
    
    print(fields)
    nn = len(fields)
    
    for ix, row in enumerate(infile):

        # sometimes get nulls in data eg when pi not shutdown cleanly
        if null in row:
            continue
        
        values = row.split(',')
        values = [x.strip() for x in values]

        if len(values) != nn:
            print(ix, len(fields), len(values))
            continue

        result.append(dict(zip(fields, values)))

    return result

def xtimewarp_timestamps(data):
    """ Don't let data go backwards in time """

    lasttime = None
    timewarp = 0.0
    mintime = 0
    for ix, row in enumerate(data):
        timestamp = float(row['timestamp'])
        
        if lasttime and timestamp < lasttime:
            timewarp = lasttime - timestamp
            print(ix, timewarp)

        row['timestamp'] = str(timestamp + timewarp)

        lasttime = timestamp

    return data

def timewarp_timestamps(data):
    """ Don't let data go backwards in time """

    from collections import Counter
    lasttime = None
    timewarp = 0.0
    mintime = 0

    deltas = Counter()
    for ix, row in enumerate(data):
        timestamp = float(row['timestamp'])        

        deltas = Counter()

        if lasttime:
            delta = round(timestamp - lasttime)
            deltas[delta] += 1

            # print(deltas.most_common())
        
        if lasttime and timestamp < lasttime:
            timewarp = lasttime - timestamp
            print(ix, timewarp)

        elif timewarp:
            mc = deltas.most_common(1)[0][0]
            if delta > mc:
                timewarp -= delta - mc
                print(f'warping warp by {delta - mc}')

        row['timestamp'] = str(timestamp + timewarp)

        lasttime = timestamp

    return data

def clean(path):
    """ Clean files at path
    
    put clean files in clean subfolder.
    """
    (path / 'clean').mkdir(exist_ok=True, parents=True)
    
    for name in path.glob('*'):

        if name.is_dir(): continue
        
        with name.open() as dirty:
            data = drop_bad_rows(dirty)
            data = timewarp_timestamps(data)

        fields = data[0].keys()
        clean_name = path / 'clean' / name.name
        with clean_name.open('w') as cleaner:
            writer = csv.DictWriter(cleaner, fieldnames=fields)
            writer.writeheader()
            writer.writerows(data)

        df = base.load(clean_name)

        # change pressure to altitude if it exists
        if hasattr(df, 'pressure'):
            df['altitude'] = df.pressure.map(pressure_to_altitude)

            df = df.drop('pressure', axis=1)

            base.save(clean_name, df)

class HatShow:
    """ Show things on a Sense Hat """

    pass
    
def main():

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('--pig', action='store_true')

    parser.add_argument('--path', default='.')
    parser.add_argument('name', nargs='?', default='sensehat')

    parser.add_argument('--sleep', type=float, default=1)

    parser.add_argument('--clean', action='store_true')

    args = parser.parse_args()

    if args.clean:
        # clean the data at path / name
        path = Path(args.path) / args.name
        clean(path)
        return
    
    if not args.pig:
        curio.run(record(args.path, args.sleep))
        return

    farm = pigfarm.PigFarm()

    hat = sense_hat.SenseHat()
    
    farm.add(WeatherHat)
    farm.add(OrientHat)

    from karmapi.mclock2 import GuidoClock
    farm.add(GuidoClock)

    pigfarm.run(farm)
    
    
if __name__ == '__main__':

    main()

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

from karmapi import pigfarm

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
            temperature_from_pressure = hat.get_temperature_from_pressure(),
            temperature_from_humidity = hat.get_temperature_from_humidity(),
            cpu_temperature = get_cpu_temperature())


        data['timestamp'] = time.time()

        yield data


def temperature_guess(data):

    guess = data['temperature_from_pressure'] + data['temperature_from_humidity']
    guess = guess / 2.0

    cputemp = data['cpu_temperature']

    guess = guess - ((cputemp - guess) / 2)

    return guess


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

            

class WeatherHat(pigfarm.MagicCarpet):
    """  Sense Hat widget """
    fields = ['humidity', 'temperature_guess', 'pressure']

    def __init__(self, parent=None, *args, **kwargs):
        """ Set up the widget """
        super().__init__(*args, **kwargs)

        layout = pig.qtw.QHBoxLayout(parent)

        meta = [["karmapi.sense.Monitor"] for x in self.fields]

        self.interval = 1
        
        # build a Grid and add to self
        monitor = pig.Grid(self, meta)
        self.monitor = monitor
        layout.addWidget(monitor)

        for widget, field in zip(monitor.grid.values(), self.fields):
            setattr(widget, 'field', field)


    async def run(self):

        self.hat = sense_hat.SenseHat()
        self.data = []

        
        while True:
            #self.data.append(get_stats(self.hat))
            for x in range(10):
                self.data.append(get_stats(self.hat))
                await curio.sleep(0.1)

            print(len(self.data))

            self.update_plots()
            
    def update_plots(self):

        if len(self.data) == 0:
            print('no data')
            return
        
        df = pandas.DataFrame(self.data)

        # FIXME: allow control over time period to plot
        print(df.info())
        for widget in self.monitor.grid.values():
            widget.show(df)
    
class OrientHat(WeatherHat):

    fields = ['compass', 'pitch', 'roll', 'yaw']
    
class Monitor(pigfarm.MagicCarpet):

    def show(self, df):
        """ Plot field from df """
        self.toolbar.hide()
        self.axes.hold(True)

        self.axes.clear()
        self.axes.plot(df.timestamp, df[self.field], label=self.field)

        self.axes.set_ylabel(self.field)
        self.draw()

    def plot(self):
        pass

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

    while True:
        print('writing', name)
        writer.writerow(next(data))
        outfile.flush()
        await curio.sleep(sleep)



async def record(path='.', sleep=1):
    """ Record everything from the hat """
    hat = sense_hat.SenseHat()

    weather = get_weather
    compass = get_compass
    gyro = get_gyro
    accel = get_acceleration

    tasks = [weather, compass, gyro, accel]
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

            

def main():

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('--pig', action='store_true')
    parser.add_argument('--path', default='.')
    parser.add_argument('--sleep', type=float, default=1)

    args = parser.parse_args()
    
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

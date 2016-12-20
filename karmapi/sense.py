"""
Sense Hat tools


"""
import subprocess
import curio
import sense_hat
import pandas
import datetime

from karmapi import pig

def piggy():

    info = dict(
        title = "SENSE HAT",
        tabs = [
            {'name': 'weather',
             'widgets': [
                 ["karmapi.sense.Temperature"],
                 ["karmapi.sense.Humidity"],
                 ["karmapi.sense.Pressure"],
             ]},
            {'name': 'curio',
             'widgets': [
                 ['karmapi.widgets.Curio']]}])

    return info
                

def stats(hat):
    while True:
        yield "T: %4.1f" % hat.temp
        yield "H: %4.1f" % hat.humidity
        yield "P: %4.0f" % hat.pressure
        yield "TP: %4.0f" % hat.get_temperature_from_pressure()
        yield "TH: %4.0f" % hat.pressure
        yield "P: %4.0f" % hat.pressure

def get_stats(hat):

    data = dict(
        temp = hat.temp,
        humidity = hat.humidity,
        pressure = hat.pressure,
        temperature_from_pressure = hat.get_temperature_from_pressure(),
        temperature_from_humidity = hat.get_temperature_from_humidity(),
        compass = hat.compass,
        cpu_temperature = get_cpu_temperature(),
        )
    data.update(hat.orientation)

    guess = data['temperature_from_pressure'] + data['temperature_from_humidity']
    guess = guess / 2.0

    cputemp = data['cpu_temperature']

    guess = guess - ((cputemp - guess) / 2)

    data['temperature_guess'] = guess

    data['timestamp'] = datetime.datetime.now()

    return data

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


class Humidity(pig.Video):

    field = 'humidity'

    async def run(self):
        """ Loop forever updating with sense had data

        A little help sleeping from curio
        """
        self.axes.hold(True)
        interval = 1

        data = []
        queue = curio.Queue()
        await curio.spawn(self.read_hat(queue))

        #for x in range(5):
        #    stats = await queue.get()
        #    data.append(stats)

        df = pandas.DataFrame(data)
        #self.axes.plot(df.timestamp, df.humidity)
        #self.draw()
        
        while True:
            stats = await queue.get()
            
            data.append(stats)
            df = pandas.DataFrame(data)

            self.axes.clear()
            self.axes.plot(df.timestamp, df[self.field],
                           label=self.field)

            self.axes.set_title(self.field)

            self.draw()

    def plot(self):
        pass

    async def read_hat(self, data):
        """ Read sense hat data """
        hat = sense_hat.SenseHat()

        while True:
            stats = get_stats(hat)
            await data.put(stats)
            await curio.sleep(self.interval)


class Temperature(Humidity):

    field = 'temperature_guess'

class Pressure(Humidity):

    field = 'pressure'
    
if __name__ == '__main__':

    app = pig.build(piggy())

    pig.run(app)
    
        
    

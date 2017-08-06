"""
Talk to a pi enviro hat
"""
import sys
import time
import argparse

import envirophat

from envirophat import light, weather, motion, analog

import curio

from karmapi.sense import record

def get_weather(hat):

    while True:
        yield dict(
            timestamp=time.time(),
            temperature=hat.weather.temperature(),
            pressure=hat.weather.pressure() / 100.0)

def get_light(hat):

    while True:
        
        data = dict(
            timestamp = time.time(),
            light = hat.light.light() / 100.0)
        
        rgb = light.rgb()
        
        data.update(dict(
            red = rgb[0],
            green = rgb[1],
            blue = rgb[2]))

        yield data

def get_motion(hat):

    while True:
        data = dict(
            timestamp = time.time(),
            heading = hat.motion.heading())

        mag = hat.motion.magnetometer()
        data.update(dict(
            mx = mag[0],
            my = mag[1],
            mz = mag[2]))

        acc = hat.motion.accelerometer()
        data.update(dict(
            ax = acc[0],
            ay = acc[1],
            az = acc[0]))

        yield data     
            

def write(line):
    sys.stdout.write(line)
    sys.stdout.flush()

OUTPUT = """
Temp: {t}c
Pressure: {p}Pa
Light: {c}
RGB: {r}, {g}, {b} 
Heading: {h}
Magnetometer: {mx} {my} {mz}
Accelerometer: {ax}g {ay}g {az}g
Analog: 0: {a0}, 1: {a1}, 2: {a2}, 3: {a3}
"""

def lettherebelight(on=True):

    if on:
        envirophat.leds.on()
    else:
        envirophat.leds.off()

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('--record', action='store_true')
    parser.add_argument('--path', default='.')
    parser.add_argument('--sleep', type=float, default=1)
    parser.add_argument('--light', action='store_true')

    args = parser.parse_args()

    lettherebelight(args.light)

    if args.record:
        names = ['motion', 'light', 'weather']
        tasks = [get_motion, get_light, get_weather]

        curio.run(
            record(args.path, args.sleep,
                   tasks=tasks, names=names, hat=envirophat))
        return
    
    write("--- Enviro pHAT Monitoring ---")

    
    while True:
        rgb = light.rgb()
        analog_values = analog.read_all()
        mag_values = motion.magnetometer()
        acc_values = [round(x,2) for x in motion.accelerometer()]

        output = OUTPUT.format(
            t = round(weather.temperature(),2),
            p = round(weather.pressure(),2),
            c = light.light(),
            r = rgb[0],
            g = rgb[1],
            b = rgb[2],
            h = motion.heading(),
            a0 = analog_values[0],
            a1 = analog_values[1],
            a2 = analog_values[2],
            a3 = analog_values[3],
            mx = mag_values[0],
            my = mag_values[1],
            mz = mag_values[2],
            ax = acc_values[0],
            ay = acc_values[1],
            az = acc_values[2])
                    
        output = output.replace("\n","\n\033[K")
        write(output)
        lines = len(output.split("\n"))
        write("\033[{}A".format(lines - 1))

        time.sleep(1)

        

if __name__ == '__main__':

    main()
                    

#!/usr/bin/env python

from pathlib import Path

def battery(path=None):

    if path is None:
        path = '/sys/class/power_supply'

    path = Path(path)
    print(path)

    for bat in path.glob('B*'):
        
        x = float((bat / 'charge_now').read_text())
        y = float((bat / 'charge_full').read_text())

        yield bat, x / y



if __name__ == '__main__':

    
    for path, bat in battery():

        print(100.0 * bat)


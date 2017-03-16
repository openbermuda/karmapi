"""  Generate toy data """

import random

def distros(trials=10000, n=5, groups=None):

    groups = groups or ['value']

    data = {}
    for group in groups:

        gdata = {}
        data[group] = gdata
        for value in range(n):
            values = [random.randint(10**5, 10**8) for x in range(trials)]

            gdata[value] = values


    return data

    

"""  Generate toy data """

import random

def distros(trials=10000, n=5, groups=None):

    groups = groups or ['value']

    data = {}
    for group in groups:

        gdata = {}
        data[group] = gdata
        for value in range(n):
            a = random.random()
            b = random.random()
            values = [random.gauss(a * 10**7, b * 10**6) for x in range(trials)]

            gdata[value] = values


    return data

    

""" Add some nulls to a file """

import random

def add_nulls(outfile, n=None):

    n = n or random.randint(1, 10)

    nulls = chr(0) * n

    outfile.write(nulls)

        

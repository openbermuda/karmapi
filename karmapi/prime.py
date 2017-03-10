""" Fun with primes"""

import random
import math

from karmapi.piglet import Video

xx = """
                            10   0.500000     0.4343 A
                           100   0.260000     0.2171 A
                         1,000   0.169000     0.1448 A
                        10,000   0.123000     0.1086 A
                       100,000   0.095930     0.0869 A
                     1,000,000   0.078499     0.0724 A
                    10,000,000   0.066458     0.0620 A
                   100,000,000   0.053200     0.0543 B
                 1,000,000,000   0.047600     0.0483 B
                10,000,000,000   0.039400     0.0434 B
               100,000,000,000   0.036900     0.0395 B
             1,000,000,000,000   0.038700     0.0362 B
            10,000,000,000,000   0.028900     0.0334 B
           100,000,000,000,000   0.032000     0.0310 B
         1,000,000,000,000,000   1.000000     0.0290 C
        10,000,000,000,000,000   1.000000     0.0271 C
       100,000,000,000,000,000   1.000000     0.0255 C
     1,000,000,000,000,000,000   1.000000     0.0241 C
"""

class Prime(Video):


    def compute_data(self):

        pass


    def plot(self):

        print('plotting primes')

        x = []
        y = []
        for row in xx.split('\n'):
            
            row = row.replace(',', '')
            fields = row.split()

            if not fields: continue

            x.append(float(fields[0]))

            yy = float(fields[1])

            if yy == 1.0:
                yy = 0.0

            y.append(yy)

        self.axes.plot(y)

        print(x)
        print(y)

        #self.axes.plot(range(10))



PRIMES = [2, 3]

def isprime(n, verbose=None):

    end = n ** 0.5
    
    genprimes(end)

    for x in PRIMES:
        if x > end:
            break
        
        if 0 == n % x:
            if verbose: print(f'{x}')
            return False

    return True



def genprime():

    for p in PRIMES:
        yield p

    n = p + 2

    while True:

        if isprime(n):
            PRIMES.append(n)
            yield n

        n += 2

def genprimes(end):

    n = PRIMES[-1]

    while n <= end:
        
        if isprime(n):
            PRIMES.append(n)

        n += 2

    

if __name__ == '__main__':

    import time
    end = 10
    t = time.time()
    for p in genprime():

        if p >= end:
            t2 = time.time()
            count = len(PRIMES)
            #print(end, count, count / end, t2-t)
            print('{:30,} {:10.6f} {:10.4f} A'.format(end, count / end, 1 / math.log(end)))
            t = t2
            end *= 10

            if end > 50000000:
                break

    # now have primes up to 100000
    biggest = PRIMES[-1]
    finish = biggest * biggest
    while end < finish:

        count = 0
        samples = 10000
        for trial in range(samples):
            sample = random.randint(end, 10 * end)
            if isprime(sample):
                count += 1

        print('{:30,} {:10.6f} {:10.4f} B'.format(end, count / samples, 1 / math.log(end)))

        end *= 10

    while end < 1e19:

        print('{:30,} {:10.6f} {:10.4f} C'.format(end, 1.0, 1 / math.log(end)))
        end *= 10
            

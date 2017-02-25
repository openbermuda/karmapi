
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


                
            

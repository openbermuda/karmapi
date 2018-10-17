import math

from matplotlib import pyplot as pp

T = 1000
k = 10000

xx = [x * math.pi / k for x in range(T)]
shint = [math.sinh(x) for x in xx]
cosht = [math.cosh(x) for x in xx]

#print(xx[-100:])
#print(yy[-100:])

pp.plot(shint, cosht)

pp.show()

"""
Are gamma-ray bursts optical illusions?

Robert S MacKay, Colin Rourke

http://msp.warwick.ac.uk/~cpr/paradigm/GammaRayBursts.pdf

What is it like when a galaxy emerges into view at the edge of our visible
universe?

In what follows I am imagining a wider universe that has the similar uniform
structure.

It appears spirals are a natural thing to arise and perhaps we just see a
window on an expanding arm of a giant spiral of galaxies.

If we go with this, then from the perspective of the galaxy (the emitter of
light just coming into view from our world) nothing unusual is happening, it is
just cruising along, just like our galaxy.

What paths have the light waves have taken to get to us and how
long that journey was?

Note also the new addition to our inertial field, settling in.

Update
======

The emitter itself does not need to enter our visible universe.  All that is
required is a beam of light from that emitter that enters our visible universe,
and is heading in our direction.


"""

import math
import numpy as np

from matplotlib import pyplot as pp



T = 1000
k = 10000

xx = [x * math.pi / k for x in range(T)]
shint = np.array([math.sinh(x) for x in xx])
cosht = np.array([math.cosh(x) for x in xx])
print(shint.size)
#print(xx[-100:])
#print(yy[-100:])

pp.plot(list(shint), list(cosht))


# emitter
shinu = shint.copy()
coshu = cosht.copy()

alpha = 2
beta  = 1
gamma = -1
delta = 1
e0 = (alpha * shinu) + (beta * coshu)
e1 = (gamma * shinu) + (delta * coshu)

# 2.2

geo_test = - (e0 * shint) + (e1 * cosht)

pp.plot(geo_test)

pp.show()


# TODO plot t against u: receiver and emitter times respectively

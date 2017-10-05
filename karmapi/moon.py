

import datetime

NEW = datetime.datetime(1900, 1, 1, 5, 50)

NEXTNEW = datetime.datetime(1900, 1, 30, 5, 22)


delta = (NEXTNEW - NEW)

deltas = delta.days * 24 * 3600

print(delta.days)

deltas += delta.seconds

print(deltas)


latest = datetime.datetime(2017, 11, 18, 3, 43)

ldelta = latest - NEW


seconds = ldelta.days * 24 * 3600
seconds += ldelta.seconds

print(seconds, seconds / deltas)

current = NEW
for x in range(100):
    print(current)

    current += delta
    

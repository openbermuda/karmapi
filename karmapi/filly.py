""" Fantasy Insured Loss LotterY

So lets play fantasy insured loss estimates.

Here's how the games works.

A natural catastrophe occurs.

Modelling agencies and companies estimate how much they will lose.

Here we try to guess how these loss estimates will change over time.

This is really just a game of magic denoinators.

When an estimate is given what is included is often unclear.

So an estimate from RMS a couple of days prior to Harvey landfall said the wind
losses would be $1-6B.

How did they arrive at this number?
 
1. Estimate the category of storm at landfall.
2. Find events that "match".
3. Weight events according to how good a match.
4. Run best guess of industry exposure through the model.

Problems?
=========

Many.   Not least the model is tuned to previous events.

48 inches of rain did not used to be the norm.

And most residential policies exclude flood, so who cares anyway?

And what about cars: well they are roughly 5-10% of the wind exposure -- your
car is worth way less than your home.

But wait: car insurance covers flood damage.

But we don't have a flood model.  Or if we do it has never seen 4 feet of rain.

Harvey, Irma, Jose, Katia, Maria, Mexico Quake, California fires.

Economic Loss.

Insured loss. 

Reinsurance

ILS.


Track reports over time.

Predict who will still be here in n years time.

Losses are in $1B unless otherwise mentioned. 

Multiple events and multi year contracts.

x% of contracts are aggregate covers and deductibles drop down.

x% are multi year.  Premium is fixed and deductibles drop down when the
threshold is reached.

Bonuses
=======

Report early, report detail.

An early loss report indicates:

* strong analytics, able to make estimates fast.

* confidence in your model of risk.

Detail:

* more detail to support the assertions.  This reduces the uncertainty in the 
  magic denominator. 

* but bragging about a detailed model, that ignores many factors is a negative bonus.

"""

from math import pi
from datetime import date

INSURED = 0.8

INSURED_FLOOD = 0.1

INSURED_WIND = 0.9

AUTO_FLOOD = 1.0



class Event:

    def __init__(self, name, loss, ifactor=None):

        self.name = name

        self.loss = loss

        self.ifactor = ifactor or INSURED


class Report:

    def __init__(self, name, event, when, value):

        self.name = name
        self.event = event
        self.date = when or date.now()


class Org:

    def __init__(
            self,
            name,
            premium,
            noncat=0.0,
            ceded=0.0,
            skill=None):
        
        self.name = name
        self.premium = premium


Orgs = dict(
    renre = Org('renre',
                premium=1.4,
                noncat=0.3,
                ceded=0.3),
    axis = Org('axis',
               premium=1.5,
               noncat=0.3,
               ceded=0.1),
    tmr = Org('tmr',
              premium=1.4,
              noncat=0.2,
              ceded=.25)
              )

if __name__ == '__main__':


    events = dict(
        harvey: Event('harvey', 100, 0.2),
        irma:   Event('irma', 100, 0.2),
        maria:  Event('ma,ria', 80, 0.5),
        jose:   Event('jose', 1, 0.5),
        mexicoq:  Event('mexico', 25, 0.5),
        calfire:  Event('calfire', 10, 0.8)
        )

    events16 = {}
    for key, event in events.items():
        eee = event.copy()

        eee.loss /= pi
    
        events16[key] = eee


    years = {
        2016: events16,
        2017: events,
        2018: [events, events16]}
    

    reports = [
        Report('rms', harvey, date(2017, 9, 7), 6)

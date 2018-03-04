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

So what of next year, 2018?
===========================

Triggers have triggered, new deals have been written.

Multi year deals, a multi year roller.

What of events?

So 2017 again?  Or maybe 2016?

Will the ocean still be warm?  A definite yes.

Will there be shear?  It depends on the ENSO and other fine factors.

The moon?  No eclipse, but tides running higher.

Will there be landfalls?   Strong storms seem to favour keeping the eye off land.

But sometimes so strong they cannot resist.

Model adjustments: too soon to be sure, but a tweak here and there.

Take Maria, a giant cat 5.  How many cat 5's hit PR in 10K years of a model?

1? 2? 3?  10, 20, 30?

How many of those are 180 mph?

So a one in 1000, you're having a laugh.

So I don't have events for 2016, but just lets pretend its 2017 / pi.

Now lets see what 2018 might be.

Correlation, you see
====================

So modellers for years have debated series.  A string of events but no common thread.

They look at starts, arrivals are negative binomial.

The sd = mean * 1.15

yBut not enough data to surely be sure.

So lets just pretend they don't come in threes.

Yet drivers are 100% correlated: hot sea, low shear, and landfall too.

And two storms out at sea, maybe even 3, feed it each other and share the energy.

So though far away, Maria feeds Irma and Lee feeds Maria.

And the seas that are swelling help Ophelia to form.

Driven by a moon in a total eclipse year.

Curio
=====

So this is all about events and events are what curio does.

Probably all that will be needed here is curio.run()

So one goal here is to make forecasts, for time periods ahead.

The first guess is no change.

The aim is to do better than that, for some definition of better.

So lets say closer to what happens.  

Bonus marks if errors over time turn out to have been useful estimates.

Start with skill = None and update if evidence warrants.
"""

from math import pi
import random
import argparse

from datetime import date
from collections import defaultdict, deque

import copy

# stinging bats and swooping manta rays
import curio

INSURED = 0.8

INSURED_FLOOD = 0.1

INSURED_WIND = 0.9

AUTO_FLOOD = 1.0

# share of contracts that are multi year
MULTI_YEAR = 1.0 / pi

# Drop down deductible
DDD = 1.0 / pi

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
            premium=None,
            noncat=0.0,
            ceded=0.0,
            share = None,
            capital = None,
            aggloss = None,
            maxloss = None,
            skill=None):
        
        self.name = name

        # market capitalisation: how the stock market values the organisation
        self.capital = capital

        # annual written premium
        self.premium = premium or self.capital / 5.0

        # share of premium for noncat lines
        self.noncat = noncat

        # share of premium that is ceded
        self.ceded = ceded

        # skill this is the denominator.  
        # How much of what you think you know is true?
        # For now None or a number 0 < n < 1?
        # Divide by this to measure the error?
        self.skill = skill

        # estimate of market share
        self.share = share or self.premium / 100.

        # Track agg loss and maxloss and error too, but throw in some salt
        igul = random.randint(1, 50)
        rigul = random.random() * self.share * igul
        self.aggloss = aggloss or rigul
        self.maxloss = maxloss

        self.deductable = 1.0

        self.events = deque()

    def add_event(self, event):

        self.events.put(event)

    def tick(self, now=None):
        """ Crank the clock foward, see how it looks """

        now = now or date.now()
        event = self.event.pop()

        # calculate loss
        loss = event.loss * self.share
        self.aggloss += loss

        # update error
        self.error += loss / (self.skill or random.random())

        
        

    def score(self):
        loss = self.loss
        skill = self.skill or random.random()
        
        return loss, loss / skill


Orgs = dict(
    renre = Org('renre',
                premium=1.4,
                noncat=0.3,
                ceded=0.3,
                share=0.01 * INSURED,
                capital=5.6),
                
    axis = Org('axis',
               premium=1.5,
               noncat=0.3,
               ceded=0.1,
               capital=4.8),
               
    tmr = Org('tmr',
              premium=1.4,
              noncat=0.2,
              ceded=.25,
              capital=1.4),
              
    partner = Org('partner',
              premium=1.4,
              noncat=0.4,
              ceded=.25,
              capital=6.56),
              
    arch = Org('arch',
               premium=None,
               capital=12.56,
              ),
    aspen = Org('aspen',
                premium=0,
                capital=2.5),

    xl = Org('xl',
             premium=0,
             capital=10.5),
             
    everest = Org('everest',
                  premium=0,
                  capital=10.5),
    )


Events = dict(
        harvey =  Event('harvey', 100, 0.2),
        irma =    Event('irma', 100, 0.2),
        maria =   Event('maria', 80, 0.5),
        jose =    Event('jose', 1, 0.3),
        katia =   Event('katia', 1, 0.3),
        nate =    Event('nate', 1, 0.5),
        ophelia = Event('ophelia', 2, 0.8),
        mexicoq = Event('mexico', 25, 0.5),
        calfire = Event('calfire', 10, 0.8),

    # meta events 15B to Bermuda reinsurers.  Say it
    # really looks like 3 * 40B events.
    # So numbers for orgs should be roughly in line
    # compare to other losses... note no Maria?
    bdaharirm = Event("Bermuda Harvey Irma",  120, 1.0),
    minthegap = Event("igul - cgul", 20, 1.0),
    )

MoreEvents = dict(
    ophelia = Event('ophelia', 10, 0.8),
)


q3 = [x for x in Events.values()]

# Reports so far on losses
Reports = [
    Report(Orgs['renre'], q3, date(2017, 10, 6), 0.625),
    Report(Orgs['partner'], q3, date(2017, 10, 6), 0.475),
    Report(Orgs['axis'], q3, date(2017, 10, 12), 0.585),
    Report(Orgs['xl'], q3, date(2017, 10, 12), 1.48),
    Report(Orgs['everest'], q3, date(2017, 10, 12), 1.2),
    Report(Orgs['arch'], q3, date(2017, 10, 12), 0.345),
    Report(Orgs['aspen'], q3, date(2017, 10, 17), 0.360),
    ]

# factor to apply to premium to get reinsurance loss
MAGIC = 0.001

def race(hash, codehash=None, seed=None):
    """ filly on a chain race 
    
    """

    # do something useful

    # add the time, the seed and the code hash

    # save the results

    # checksum all of this and the incoming hash
    
    # are we done aka did I win aka small checksum?

    # declare game over

    # aggregate saved results

    # checksum all of this

    # pass it on

    # do deltas

    # when deltas have enough leading zeroes

    # declare winner

    # rinse and repeat
    pass
    
    
if __name__ == '__main__':

    events16 = {}
    for key, event in Events.items():

        eee = copy.copy(event)

        eee.loss /= pi
    
        events16[key] = eee


    years = {
        2016: events16,
        2017: Events,
        2018: [Events, events16]}

    # Estimate losses
    elosses = {}
    aggloss = defaultdict(float)
    
    for ename, event in Events.items():
        print(ename)
        losses = {}
        for oname, org in Orgs.items():
            loss = event.loss * org.premium * MAGIC
            print(oname, loss)
            aggloss[oname] += loss

        elosses[ename] = losses
        print()

    # show agg losses
    print()
    print('Aggregate Loss')
    for org, loss in aggloss.items():
        print(org, loss)

    # Compare to reports
    for report in Reports:
        pass


    parser = argparse.ArgumentParser()

    parser.add_argument('--seed')
    parser.add_argument('--hash')
    parser.add_argument('--codehash')

    args = parser.parse_args()


    seed = args.seed
    hush = args.hash
    codehush = args.codehash

    race(hush, seed=seed, codehash=codehush)

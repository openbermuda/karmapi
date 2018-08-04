""" World Cup

Over the years I've done a few world cup predict the scores things.

There's another one coming so here we go.

Eight groups of four.

And six games per group.

Will likely turn into a simulation of errors.

Prior? probabilities for games.. aim it to predict first and second in each
group for now as those will be the ones that get there.

Things to include maybe... factors for order games are played.

Oh and stuff like what will be going on at home by June 2018.

Russia are the hosts, and I understand have graciously offered to represent the
USA and Italy too, sorry you couldn't make the party.

Seek Irish, Scots or English for advice on how to survive when your team is not
there.

All times are UTC and subject to typos and other delights.

The story so far.

It's December 2017.  World Cup finals draw in Russia is out.

Italy and USA are already out.  Sweden eliminated Italy and the USA story is more complex. 

On the Mueller advent calendar Michael Flynn pleaded guilty on the 1st.

Picture wasn't clear on the 2nd.  3-4 maybe more faces?

Back to the world cup.

Group A.

rus sau egy urg


OK.. back from the fixture lists.

Order of games interesting and need to add places.  Fair bit of moving around
in some groups.  

Some teams get to play after seeing the other game in their group in first two
rounds of games.

As groups progress teams will be looking at what comes next, if they have a
couple of wins, or otherwise just how to get out of the group.

Seeding has placed the teams with higher FIFA rankings with potentially less
travel complications, but then there are the fans back home and time zone
considerations.

Now it is 2017 so there may be an obligatory block chain connection, but if so
it well be super low tech.

And simulations.   For now stuck deciding what to simulate.. oh and priors..

I think we may need some events here soon.

Back to the coding.  So rule 0: keep it under 1000 lines, bonus marks under
500.  World cup rules, so you decide how to count.

Subtracting docstrings there should be a lot less.  And with luck sphinx will
magically turn the code into ok docs.

rule 1: there is no rule one.  It's the world cup, so breaking all the coding
rules.  See also counting lines of code, world cup style.

Or rather just writing what seems easiest at the time.

There is a fair bit of going round in circles: check the commit log see git.

Ok.. back to the football.

The world cup mixes up 32 teams from around the world.  The final draw mixes
everything up and there are some fascinating match ups.

Simon Kuiper, football anthropologist?, wrote a fascinating book about matches
between countries, places that had been at war in the very recent past.  Many
of the games covered were at world cups or big football federation finals.

Others were just qualifying games.  

Sources:  Wikipedia and scriblings on beer mats.

Places coming along.

Rostov-on-Don.  Lots of twin towns, including Toronto.

Some interesting games there too.

545km to the south

Simulations
===========

Run the code and you get a draw for the last 16.

I am starting to simulate the first round games with 4 bottles in a pool.  It's
like Paul the octobpus, but not quite so scientific.  Or maybe it is?

eng tun bel and pan played already.  See Game's for results.


"""
import argparse
import curio

from .jsf import JeuxSansFrontieres
from .mexwave import MexicanWaves

# break with tradition and import *
# so if you can't fint it here, check wcYYYY
from .wc2018 import *

from karmapi import pigfarm


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--nopig', action='store_true')
    parser.add_argument('--back_image')
    parser.add_argument('--dump')
    parser.add_argument('--events')
    parser.add_argument('--warp', type=float, default=1.0,
                        help="warp speed")
    parser.add_argument('--outfile')
    args = parser.parse_args()            

    if args.nopig:
        sys.exit()

    farm = pigfarm.PigFarm()

    from karmapi.mclock2 import GuidoClock

    xdump = args.dump
    if xdump:
        xdump = open(args.dump, 'w')

    if args.outfile:
        args.outfile = open(args.outfile, 'w')

    if args.events:
        args.events = open(args.events)

        #parse_events(args.events, args.outfile)
        #sys.exit()

    jsf.timewarp *= args.warp    
    farm.add(GuidoClock)
    farm.add(MexicanWaves, dict(jsf=jsf,
                                venues=places,
                                back_image=args.back_image,
                                events=args.events,
                                dump=xdump))

    # add a random wc time warper?
    curio.run(farm.run(), with_monitor=True)



if __name__ == '__main__':

    main()

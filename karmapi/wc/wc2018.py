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
from .base import *


from .jsf import JeuxSansFrontieres
from .game import Game
from .group import Group
from .team import Team
from .place import Place


class Moscow(Place):
    """ Final """

    name = 'Moscow Luzhniki'
    lat = 55 + (45 / 60)
    lon = 37 + (37 / 60)

class Spartak(Place):
    """ Spartak Moscow  """

    name = 'Moscow Oktkrytiye'
    lat = 57 + (49 / 60)
    lon = 34 + (26 / 60)

    xlat = 55 + (49 / 60)
    xlon = 37 + (26 / 60)


class StPetersberg(Place):
    """ Place of many names """

    name = 'St Petersberg'
    lat = 59 + (58 / 60)
    lon = 30 + (14 / 60)

class Volgograd(Place):
    """ Down south """

    name = 'Volgograd'
    lat = 48 + (45 / 60)
    lon = 44 + (33 / 60)

class Novgorod(Place):
    """ Central """

    name = 'Nizhny Novgorod'
    lat = 56 + (20 / 60)
    lon = 43 + (57 / 60)
    
class Kaliningrad(Place):
    """ North West port """

    name = 'Kaliningrad'
    lat = 54 + (42 / 60)
    lon = 20 + (32 / 60)

class RostovOnDon(Place):
    """ Sheffield in Russia """
    name = "Rostov-on-Don"
    lat = 47 + (13 / 60)
    lon = 39 + (44 / 60)
    
class Kazan(Place):
    """  
    
    https://tools.wmflabs.org/geohack/geohack.php?

    pagename=Kazan_Arena&

    params=55_49_14.3_N_49_9_40.0_E_type:landmark """

    name = 'Kazan'
    lat = 55 + (49 / 60) + (14.3 / 3600)
    lon = 49 + (9 / 60) + (40.0 / 3600)

class Samara(Place):
    """  """

    name = 'Samara'
    lat = 53 + (17 / 60)
    lon = 10 + (14 / 60)

class Yekaterinburg(Place):
    """  """

    name = 'Central Stadium'
    lat = 56 + (50 / 60)
    lon = 60 + (34 / 60)

class Saransk(Place):
    """  """

    name = 'Mordovia Arena'
    lat = 54 + (11 / 60)
    lon = 45 + (12 / 60)

class Sochi(Place):
    """  """

    name = 'Fisht Olympic Stadium'
    lat = 43 + (24 / 60)
    lon = 39 + (57 / 60)


places = dict(
    
    moscow=Moscow(),
    spartak=Spartak(),
    stpetersberg=StPetersberg(),

    kaliningrad=Kaliningrad(),

    novgorod=Novgorod(),
    yekaterinburg=Yekaterinburg(),
    kazan=Kazan(),
    saransk=Saransk(),
    samara=Samara(),

    volgograd=Volgograd(),
    rostovondon=RostovOnDon(),
    sochi=Sochi(),
    )

# Group A
rus = Team('RUS')
sau = Team('SAU')
egy = Team('EGY')
urg = Team('URG')

# Group B
por = Team('POR')
spa = Team('SPA')
mor = Team('MOR')
ira = Team('IRA')

# group C
fra = Team('FRA')
aus = Team('AUS')
per = Team('PER')
den = Team('DEN')

# group D
arg = Team('ARG')
ice = Team('ICE')
cro = Team('CRO')
nig = Team('NIG')

# group E
bra = Team('BRA')
swi = Team('SWI')
crc = Team('CRC')
ser = Team('SER')

# group F
ger = Team('GER')
swe = Team('SWE')
mex = Team('MEX')
sko = Team('SKO')

# group G
bel = Team('BEL')
pan = Team('PAN')
tun = Team('TUN')
eng = Team('ENG')

# group H
pol = Team('POL')
sen = Team('SEN')
col = Team('COL')
jap = Team('JAP')

    
groups = dict(
    a=Group(teams = [rus, sau, egy, urg],
            games = [
                Game(rus, sau, datetime(2018, 6, 14, 15, 0),
                     where=places['moscow'],
                     ascore=5, bscore=0),

                Game(egy, urg, datetime(2018, 6, 15, 12, 0),
                     where=places['yekaterinburg'],
                     ascore=0, bscore=1),

                
                Game(rus, egy, datetime(2018, 6, 19, 18, 0),
                     where=places['stpetersberg'],
                     ascore=3, bscore=1),
                
                Game(urg, sau, datetime(2018, 6, 20, 15, 0),
                     where=places['rostovondon'],
                     ),
                

                Game(urg, rus, datetime(2018, 6, 25, 14, 0),
                     where=places['samara'],
                     ),
                Game(sau, egy, datetime(2018, 6, 25, 14, 0),
                     where=places['volgograd'],
                     ),
                ]),
                
    b=Group(teams = [por, spa, mor, ira],
            games = [
                Game(mor, ira, datetime(2018, 6, 15, 15, 0),
                     where=places['stpetersberg'],
                     ascore=0, bscore=1),
                     
                Game(por, spa, datetime(2018, 6, 15, 18, 0),
                     where=places['sochi'],
                     ascore=3, bscore=3),

                
                Game(por, mor, datetime(2018, 6, 20, 12, 0),
                     where=places['moscow'],
                     ),
                Game(ira, spa, datetime(2018, 6, 20, 18, 0),
                     where=places['kazan'],
                     ),
                
                Game(ira, por, datetime(2018, 6, 25, 18, 0),
                     where=places['saransk'],
                     ),
                Game(spa, mor, datetime(2018, 6, 25, 18, 0),
                     where=places['kaliningrad'],
                     ),
                ]),
                
    c=Group(teams = [fra, aus, per, den],

            games = [
                Game(fra, aus, datetime(2018, 6, 16, 10, 0),
                     where=places['kazan'],
                     ascore=2, bscore=1),
                     
                Game(per, den, datetime(2018, 6, 16, 14, 0),
                     where=places['saransk'],
                     ascore=0, bscore=1),

                
                Game(den, aus, datetime(2018, 6, 21, 12, 0),
                     where=places['samara'],
                     ),
                Game(fra, per, datetime(2018, 6, 21, 15, 0),
                     where=places['yekaterinburg'],
                     ),
                
                Game(den, fra, datetime(2018, 6, 26, 14, 0),
                     where=places['moscow'],
                     ),
                Game(aus, per, datetime(2018, 6, 26, 14, 0),
                     where=places['sochi'],
                     ),
                
                ]),
                
    d=Group(teams = [arg, ice, cro, nig],

            games = [
                Game(arg, ice, datetime(2018, 6, 16, 13, 0),
                     where=places['spartak'],
                     ascore=1, bscore=1),

                Game(cro, nig, datetime(2018, 6, 16, 19, 0),
                     where=places['kaliningrad'],
                     ascore=2, bscore=0),

                
                Game(arg, cro, datetime(2018, 6, 21, 18, 0),
                     where=places['novgorod'],
                     ),
                
                Game(nig, ice, datetime(2018, 6, 22, 15, 0),
                     where=places['volgograd'],
                    ),

                
                Game(nig, arg, datetime(2018, 6, 26, 18, 0),
                     where=places['stpetersberg'],
                     ),
                Game(ice, cro, datetime(2018, 6, 26, 18, 0),
                     where=places['rostovondon'],
                     ),
                ]),
                
    e=Group(teams = [bra, swi, crc, ser],

            games = [
                Game(crc, ser, datetime(2018, 6, 17, 12, 0),
                     where=places['samara'],
                     ascore=0, bscore=1),
                     
                Game(bra, swi, datetime(2018, 6, 17, 18, 0),
                     where=places['rostovondon'],
                     ascore=1, bscore=1),

                
                Game(bra, crc, datetime(2018, 6, 22, 12, 0),
                     where=places['stpetersberg'],
                     ),
                Game(ser, swi, datetime(2018, 6, 22, 18, 0),
                     where=places['kaliningrad'],
                     ),
                
                Game(ser, bra, datetime(2018, 6, 27, 18, 0),
                     where=places['spartak'],
                     ),
                Game(swi, crc, datetime(2018, 6, 27, 18, 0),
                     where=places['novgorod'],
                     ),
                ]),
                
    f=Group(teams = [ger, swe, mex, sko],

            games = [
                Game(ger, mex, datetime(2018, 6, 17, 15, 0),
                     where=places['moscow'],
                     ascore=0, bscore=1),

                Game(swe, sko, datetime(2018, 6, 18, 12, 0),
                     where=places['novgorod'],
                     ascore=1, bscore=0),

                
                Game(sko, mex, datetime(2018, 6, 23, 15, 0),
                     where=places['rostovondon'],
                     ),
                Game(ger, swe, datetime(2018, 6, 23, 18, 0),
                     where=places['sochi'],
                     ),
                
                Game(sko, ger, datetime(2018, 6, 27, 14, 0),
                     where=places['kazan'],
                     ),
                Game(mex, swe, datetime(2018, 6, 27, 14, 0),
                     where=places['yekaterinburg'],
                     ),
                ]),
                
    g=Group(teams = [bel, pan, tun, eng],

            games = [
                Game(bel, pan, datetime(2018, 6, 18, 15, 0),
                     where=places['sochi'],
                     ascore=3, bscore=0),
                     
                Game(tun, eng, datetime(2018, 6, 18, 18, 0),
                     where=places['volgograd'],
                     ascore=1, bscore=2),

                
                Game(bel, tun, datetime(2018, 6, 23, 12, 0),
                     where=places['spartak'],
                     ),
                
                Game(eng, pan, datetime(2018, 6, 24, 12, 0),
                     where=places['novgorod'],
                     ),
                
                Game(eng, bel, datetime(2018, 6, 28, 18, 0),
                     where=places['kaliningrad'],
                     ),
                Game(pan, tun, datetime(2018, 6, 28, 18, 0),
                     where=places['saransk'],
                     ),
                ]),
                
    h=Group(teams = [pol, sen, col, jap],

            games = [
                Game(col, jap, datetime(2018, 6, 19, 12, 0),
                     where=places['saransk'],
                     ascore=1, bscore=2),
                     
                Game(pol, sen, datetime(2018, 6, 19, 15, 0),
                     where=places['spartak'],
                     ascore=1, bscore=2),

                
                Game(jap, sen, datetime(2018, 6, 24, 15, 0),
                     where=places['yekaterinburg'],
                     ),
                Game(pol, col, datetime(2018, 6, 24, 18, 0),
                     where=places['kazan'],
                     ),
                
                Game(jap, pol, datetime(2018, 6, 28, 14, 0),
                     where=places['volgograd'],
                     ),
                Game(sen, col, datetime(2018, 6, 28, 14, 0),
                     where=places['samara'],
                     ),
                ]))


print()
print("It's a knock out!")
    
# Simulate a knockout draw + bugs
jsf_places = [
    places['sochi'],
    places['kazan'],
    places['samara'],
    places['rostovondon'],

    places['moscow'],
    places['novgorod'],
    places['stpetersberg'],
    places['spartak'],
    
    places['novgorod'],
    places['kazan'],
    places['samara'],
    places['sochi'],
    

    places['stpetersberg'],
    places['moscow'],
    
    places['stpetersberg'],
    
    places['moscow'],
    ]

jsf_dates = [
    datetime(2018, 6, 30, 18, 0),
    datetime(2018, 6, 30, 14, 0),
    datetime(2018, 7,  2, 14, 0),
    datetime(2018, 7,  2, 18, 0),

    datetime(2018, 7,  1, 14, 0),
    datetime(2018, 7,  1, 18, 0),
    datetime(2018, 7,  3, 14, 0),
    datetime(2018, 7,  3, 18, 0),
    
    datetime(2018, 7,  6, 14, 0),
    datetime(2018, 7,  6, 18, 0),
    datetime(2018, 7,  7, 14, 0),
    datetime(2018, 7,  7, 18, 0),
    
    datetime(2018, 7, 10, 18, 0),
    datetime(2018, 7, 11, 18, 0),
    
    datetime(2018, 7, 14, 14, 0),
    datetime(2018, 7, 15, 15, 0),
    ]

def name2team(name):
    """ Convert string to team object """
    return globals()[name]


jsf = JeuxSansFrontieres(
    groups,
    places=jsf_places,
    dates=jsf_dates,
    name2team=name2team)






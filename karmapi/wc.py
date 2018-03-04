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

import random
import argparse

from datetime import datetime, timedelta

# number of teams
n = 32

class Team:

    def __init__(self, name=None, win=None):
        """ Init the team with no name? """
        self.name= name
        self.points = 0
        self.yellow = 0
        self.red = 0
        self.goals = 0
        self.against = 0

        self.win = win or 1 / n

        
    def __str__(self):

        msg = f'{self.name} {self.points:3}'
        msg +=f'{self.goals - self.against:4} {self.goals:4} {self.against:4}'

        return msg

class Group:

    def __init__(self, teams=None, games=None):

        self.teams = teams
        self.games = games or []

    def winner(self):
        """ Pick a winner """
        return self.get_table()[0]

    def second(self):
        """ Pick a second """
        return self.get_table()[1]

    def __str__(self):

        return str(self.teams, self.games)

    def run(self):
        """ Run the group """
        for game in self.games:

            print()
            print (game)
            print()
            
            ascore = game.ascore
            bscore = game.bscore

            print(ascore, bscore)
            # if either score is None, call score
            if game.ascore == None or game.bscore == None:
                ascore, bscore = game.score()

            print(f'{ascore} {bscore}')
            print()

            a = game.a
            b = game.b
            
            a.goals += ascore
            b.goals += bscore

            a.against += bscore
            b.against += ascore

            if ascore > bscore:
                a.points += 3

            elif bscore > bscore:
                b.points += bscore

            else:
                a.points += 1
                b.points += 1

    def table(self):
        """ Show the group table """
        teams = self.get_table()
        
        for team in teams:
            print(team)

        
    def get_table(self):
        """ Return teams sorted per table """
        teams = list(self.teams)

        teams = sorted(teams, key=self.tablesort)

        return list(reversed(teams))

    def tablesort(self, key):
        """ Order teams """
        return key.points, key.goals - key.against, key.goals
        
            


class JeuxSansFrontieres:
    """  The knockout stage.

    Winners and seconds from group stage come through into a
    last 16 grid that looks something like this:

    wa rb
    wc rd   w  w    w  w   w  w   W r

    we rf   w  w
    wg rh

    wb ra   w  w    w  w   s s    T f
    wd rc   

    wf re   w  w
    wh rg

    with abcdefgh
     and badcfehg
    

    """
    def __init__(self, groups, places=None, dates=None):
        """ Set up knockout stage """
        key = sorted(groups.keys())

        key = list(key)
        print(key)

        key2 = ''
        for x in range(0, len(key), 2):
            key2 += key[x+1] + key[x]

        print(key2) 

        games = []

        for gps in key, key2:
            for x in range(0, len(key), 2):
            
                a = gps[x]
                b = gps[x+1]
                
                teama = groups[a].winner()
                teamb = groups[b].second()

                games.append([teama, teamb])

        dates = dates or [datetime.today()] * len(games)
        
        for game, date in zip(games, dates):
            game.append(date)
            
        places = places or (['???'] * len(games))
        for game, place in zip(games, places):
            game.append(place)

        self.games = []
        for teama, teamb, when, place in games:
            self.games.append(Game(teama, teamb, when, place))
        
        for game in self.games:
            print(game)

        

class Game:

    def __init__(self, a, b, when, where=None, ascore=None, bscore=None):

        self.a = a
        self.b = b
        self.when = when
        self.where = where
        
        self.ascore = ascore
        self.bscore = bscore

    def score(self):
        """ Make up a score """
        ascore = random.randint(0, random.randint(0, 5))
        bscore = random.randint(0, random.randint(0, 5))

        return self.ascore or ascore, self.bscore or bscore

    def __str__(self):

        return f'{self.a.name} {self.b.name} {self.when} {self.where}'


class Place:
    pass

class Moscow(Place):
    """ Final """

    name = 'Moscow Luzhniki'
    lat = 55 + (45 / 60)
    lon = 37 + (37 / 60)

class Spartak(Place):
    """ Spartak Moscow  """

    name = 'Moscow Oktkrytiye'
    lat = 55 + (49 / 60)
    lon = 37 + (26 / 60)


class StPetersberg(Place):
    """ Place of many names """

    name = 'St Petersberg'
    lat = None
    lon = None

class Volgograd(Place):
    """ Down south """

    name = 'Volgograd'
    lat = None
    lon = None

class Novgorod(Place):
    """ Central """

    name = 'Nizhny Novgorod'
    lat = None
    lon = None
    
class Kaliningrad(Place):
    """ North West port """

    name = 'Kaliningrad'
    lat = None
    lon = None

class RostovOnDon(Place):
    """ Sheffield in Russia """
    name = "Rostov-on-Don"
    lat = None
    lon = None
    
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
    lat = None
    lon = None

class Yekaterinburg(Place):
    """  """

    name = ''
    lat = None
    lon = None

class Saransk(Place):
    """  """

    name = ''
    lat = None
    lon = None

class Sochi(Place):
    """  """

    name = ''
    lat = None
    lon = None

    

places = [

    Moscow(),
    Spartak(),
    StPetersberg(),

    Kaliningrad(),

    Novgorod(),
    Yekaterinburg(),
    Kazan(),
    Saransk(),
    Samara(),

    Volgograd(),
    RostovOnDon(),
    Sochi(),
    
    ]
    

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
                     ascore=4, bscore=0),

                Game(egy, urg, datetime(2018, 6, 15, 12, 0),
                     ascore=1, bscore=2),

                
                Game(rus, egy, datetime(2018, 6, 19, 18, 0)),
                
                Game(urg, sau, datetime(2018, 6, 20, 15, 0)),
                

                Game(urg, rus, datetime(2018, 6, 19, 14, 0)),
                Game(sau, egy, datetime(2018, 6, 19, 14, 0)),
                ]),
                
    b=Group(teams = [por, spa, mor, ira],
            games = [
                Game(mor, ira, datetime(2018, 6, 15, 15, 0),
                     ascore=2, bscore=2),
                     
                Game(por, spa, datetime(2018, 6, 15, 18, 0),
                     ascore=3, bscore=2),

                
                Game(por, mor, datetime(2018, 6, 20, 12, 0)),
                Game(ira, spa, datetime(2018, 6, 20, 18, 0)),
                
                Game(ira, por, datetime(2018, 6, 25, 18, 0)),
                Game(spa, mor, datetime(2018, 6, 25, 18, 0)),
                ]),
                
    c=Group(teams = [fra, aus, per, den],

            games = [
                Game(fra, aus, datetime(2018, 6, 16, 10, 0),
                     ascore=1, bscore=2),
                     
                Game(per, den, datetime(2018, 6, 16, 14, 0),
                     ascore=2, bscore=2),

                
                Game(den, aus, datetime(2018, 6, 21, 12, 0)),
                Game(fra, per, datetime(2018, 6, 21, 15, 0)),
                
                Game(den, fra, datetime(2018, 6, 26, 14, 0)),
                Game(aus, per, datetime(2018, 6, 26, 14, 0)),
                ]),
                
    d=Group(teams = [arg, ice, cro, nig],

            games = [
                Game(arg, ice, datetime(2018, 6, 16, 13, 0),
                     ascore=3, bscore=2),

                Game(cro, nig, datetime(2018, 6, 16, 19, 0),
                     ascore=2, bscore=2),

                
                Game(arg, cro, datetime(2018, 6, 21, 18, 0)),
                
                Game(nig, ice, datetime(2018, 6, 22, 15, 0)),

                
                Game(nig, arg, datetime(2018, 6, 26, 18, 0)),
                Game(ice, cro, datetime(2018, 6, 26, 18, 0)),
                ]),
                
    e=Group(teams = [bra, swi, crc, ser],

            games = [
                Game(crc, ser, datetime(2018, 6, 17, 12, 0),
                     ascore=2, bscore=4),
                     
                Game(bra, swi, datetime(2018, 6, 17, 18, 0),
                     ascore=3, bscore=3),

                
                Game(bra, crc, datetime(2018, 6, 22, 12, 0)),
                Game(ser, swi, datetime(2018, 6, 22, 18, 0)),
                
                Game(ser, bra, datetime(2018, 6, 27, 18, 0)),
                Game(swi, crc, datetime(2018, 6, 27, 18, 0)),
                ]),
                
    f=Group(teams = [ger, swe, mex, sko],

            games = [
                Game(ger, mex, datetime(2018, 6, 17, 15, 0),
                     ascore=1, bscore=2),

                Game(swe, sko, datetime(2018, 6, 18, 12, 0),
                     ascore=3, bscore=2),

                
                Game(sko, mex, datetime(2018, 6, 23, 15, 0)),
                Game(ger, swe, datetime(2018, 6, 23, 18, 0)),
                
                Game(sko, ger, datetime(2018, 6, 27, 14, 0)),
                Game(mex, swe, datetime(2018, 6, 27, 14, 0)),
                ]),
                
    g=Group(teams = [bel, pan, tun, eng],

            games = [
                Game(bel, pan, datetime(2018, 6, 18, 15, 0),
                     ascore=3, bscore=1),
                     
                Game(tun, eng, datetime(2018, 6, 18, 18, 0),
                     ascore=0, bscore=0),

                
                Game(bel, tun, datetime(2018, 6, 23, 12, 0)),
                
                Game(eng, pan, datetime(2018, 6, 24, 12, 0)),
                
                Game(eng, bel, datetime(2018, 6, 28, 18, 0)),
                Game(pan, tun, datetime(2018, 6, 28, 18, 0)),
                ]),
                
    h=Group(teams = [pol, sen, col, jap],

            games = [
                Game(col, jap, datetime(2018, 6, 19, 12, 0),
                     ascore=2, bscore=1),
                     
                Game(pol, sen, datetime(2018, 6, 19, 15, 0),
                     ascore=3, bscore=2),

                
                Game(jap, sen, datetime(2018, 6, 24, 15, 0)),
                Game(pol, col, datetime(2018, 6, 24, 18, 0)),
                
                Game(jap, pol, datetime(2018, 6, 28, 14, 0)),
                Game(sen, col, datetime(2018, 6, 28, 14, 0)),
                ]))

# group winners and seconds
winners = {}
seconds = {}
for item in 'abcdefgh':

    group = groups[item]
    
    winners[group] = group.winner()
    seconds[group] = group.second()


# do something ?

# print out the games
for xx, group  in groups.items():
    
    print(xx)
    
    for game in group.games:
        print(game.a, game.b, game.when)

    print()
    group.run()
    print()

    group.table()


print()
print("It's a knock out!")
    
# Simulate a knockout draw + bugs
jsf = JeuxSansFrontieres(groups)

    

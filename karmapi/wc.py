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

from random import random, randint
import argparse
from collections import Counter, defaultdict
from datetime import datetime, timedelta
import sys

import curio

from karmapi import pigfarm


# number of teams
n = 32
squadsize = 23

class Team:

    def __init__(self, name=None, win=None):
        """ Init the team with no name? """
        self.name = name

        # default location: North Pole
        self.lat = 90
        self.lon =  0
        
        self.win = win or 1 / n

        self.reset()


    def reset(self):

        self.points = 0
        self.yellow = 0
        self.red = 0
        self.goals = 0
        self.against = 0

        # Keep track of games played/to be played?
        self.games = []

        self.load_squad()

    def load_squad(self):
        """ Numbers 1 to sqadsize """
        self.squad = defaultdict(int)

        for player in range(squadsize):
            self.squad[player] = Player(player + 1)
        
    def where(self, when):
        """ Where is the team? """

        last_game = None
        next_game = None
        for game in self.games:
            if game.when < when:
                last_game = game
            else:
                next_game = game
                break

        if last_game is None and next_game is None:
            # return a defualt?
            return self.lat, self.lon

        # if one is missing, use the other
        last_game = last_game or next_game
        next_game = next_game or last_game
        
        # Interpolate based on time
        self.lat, self.lon = warp(last_game, next_game, when)

        return self.lat, self.lon

    def __str__(self):
 
       return self.name


    def stats(self):

        return dict(
            points = self.points,
            goals = self.goals,
            against = self.against,
            goal_delta = self.goals - self.against,
            red = self.red,
            yellow = self.yellow)

    def statto(self):
        """ Return line of stats for the team """

        stats = self.stats()
        msg = "%s" % self.name
        msg += " {points:4d} {goal_delta:4d}".format(**stats)
        msg += " {goals:4d} {against:4d}".format(**stats)

        return msg

class Player:
    """ A player of class

    Tony Currie, Kyle Walker, Harry Maguire
    """

    def __init__(self, number):

        self.goals = []
        self.red = []
        self.yellow = []
        self.number = number

class Goal:

    def __init__(self, team, who=None, when=None, game=None, penalty=False):

        self.who = who
        self.when = when
        self.game = game
        self.penalty = penalty

class Penalty:
    """ Penalty in a shoot out 

    which: which penalty: 1, 2, 3 etc
    """
    def __init__(self, team, who=None, which=None, game=None, score=True):

        self.who = who
        self.when = when
        self.game = game
        self.penalty = penalty

class ShootOut:
    """ Class to run a penalty shoot out """
    pass
        
def warp(a, b, when):
    """ Interpolate between a and b based on time """
    
    delta_t = (b.when - a.when).total_seconds()

    if delta_t == 0:
        return a.where.lat, a.where.lon

    delta_w = (when - a.when).total_seconds()
    
    frac = delta_w / delta_t

    aa = a.where
    bb = b.where
    
    lat = aa.lat
    lon = aa.lon

    lat += frac * (bb.lat - aa.lat)
    lon += frac * (bb.lon - aa.lon)

    return lat, lon        


class Game:

    NUMBER = 1

    def __init__(self, a, b, when, where=None, ascore=None, bscore=None):

        self.a = a
        self.b = b
        self.when = when
        self.where = where
        
        self.ascore = ascore
        self.bscore = bscore
        self.minute = 0

        # flag if score was simulated
        self.simulated = (ascore is None) or (bscore is None)
        self.number = Game.NUMBER
        Game.NUMBER += 1


    def reset(self):
        """ Reset score if it was random """
        if self.simulated:
            self.ascore = self.bscore = None
            self.minute = 0

    def __str__(self):

        return (
            str(self.label) + ' '  +
            str(self.a.name) + ' v '  +
            str(self.b.name) + ' '  +
            str(self.when)  + ' '  +
            str(self.where))

    def __eq__(self, other):

        return self.number == other.number

    def __ne__(self, other):

        return self.number != other.number

    def __gt__(self, other):

        return (self.when, self.number) > (other.when, other.number)

    def __le__(self, other):

        return (self.when, self.number) <= (other.when, other.number)

    def __ge__(self, other):

        return (self.when, self.number) >= (other.when, other.number)

    async def kick_off(self):
        """ Game has kicked off """
        self.ascore = 0
        self.bscore = 0
        
        minutes = 45 + randint(0, 7)

        await self.half(minutes)

        await self.half_time()

        await self.second_half()

        await self.full_time()
        if self.is_group():
            # maybe a good time to check if group is finished?
            return self.ascore, self.bscore

    def is_group(self):

        return hasattr(self, 'group')
    
    async def half(self, minutes):
        """ Run a half """

        for minute in range(minutes):
            await self.run_minute()


    async def run_minute(self):
        
        yellow_per_minute = 1 / 30
        red_per_minute = 1 / 150
        goals_per_minute = 1 / 30

        # score a goal?
        if random() < goals_per_minute:
            # who scored
            if random() <= 0.5:
                self.ascore += 1
            else:
                self.bscore += 1
                
            await self.flash(" %dm" % self.minute, fill='green')
                
        if random() < yellow_per_minute:
            # yellow card?
            pass

        if random() < red_per_minute:
            # red card?
            pass

        self.minute += 1

        return self.ascore, self.bscore

    async def half_time(self):

        self.flash(fill='blue', tag='HT')

    async def second_half(self):
        minutes = 45 + randint(0, 7)
        await self.half(minutes)

    async def full_time(self):
        
        self.flash(fill='blue', tag='FT')

    async def extra_time(self):
        pass

    async def extra_half_time(self):
        pass

    async def extra_full_time(self):
        pass

    async def penalties(self):
        pass

    async def goal(self, team, who=None, when=None):
        pass

    async def yellow(self, team, who=None, when=None):
        pass

    async def red(self, team, who=None, when=None):
        pass

    async def sub(self, team, off=None, on=None, when=None):
        pass

    async def run(self, events):
        """ Run the game """
        self.events = events

        if self.ascore == None or self.bscore == None:
            await self.kick_off()

        a = self.a
        b = self.b
            
        a.goals += self.ascore
        b.goals += self.bscore

        a.against += self.bscore
        b.against += self.ascore

        if self.ascore > self.bscore:
            a.points += 3

        elif self.bscore > self.ascore:
            b.points += 3

        else:
            a.points += 1
            b.points += 1

        await self.flash(tag='FT')

    async def flash(self, tag='', fill='red'):

        a = self.a
        b = self.b
        ascore = self.ascore
        bscore = self.bscore
        
        msg = a.name + ' ' + str(ascore) + ' ' + str(bscore) + ' ' + b.name
        msg += ' ' + tag

        print('flash', msg)
        when = self.when + timedelta(minutes=self.minute)
        await self.events.put(dict(where=self.where, msg=msg, yoff=-90,
                                   when=when, fill=fill))


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

    def reset(self):
        """ reset for a new run """
        for game in self.games:
            game.reset()

        for team in self.teams:
            team.reset()

    def run(self):
        """ Run the group """
        for game in self.games:

            print()
            print (game)
            print()

            game.run()
            

    def table(self):
        """ Show the group table """
        teams = self.get_table()
        
        for team in teams:
            print(team)
            print(team.statto)

        
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
    

    So lets set it up so we can do:

    * simulate groups
    * do draw for knockout stage
    * get games for final stage

    """
    def __init__(self, groups, places=None, dates=None, now=None):
        self.groups = groups

        # places and dates for knockout stage
        self.places = places
        self.dates = dates

        self.now = now or datetime(2018, 6, 14)
        self.step = timedelta(hours=1)

        self.games = curio.PriorityQueue()
        self.events = curio.UniversalQueue()

    async def load_group_games(self):
        """ Put the group games into the game queue """
        for label, group in self.groups.items():
            group.name = label
            group.reset()
            for game in group.games:
                game.group = group
                game.label = label.upper()

                game.a.games.append(game)
                game.b.games.append(game)

                await self.games.put(game)

    def its_a_knockout(self):
        """ Set up knockout stage """

        groups = self.groups
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


    def run_groups(self):
        """ Run the group stage """
        # group winners and seconds
        winners = {}
        seconds = {}

        # print out the games while we are at it
        for xx, group  in groups.items():
            
            print(xx)
            
            for game in group.games:
                print(game.a, game.b, game.when)

            print()
            group.run()
            print()

            winners[xx] = group.winner()
            seconds[xx] = group.second()

            group.table()

    def generate_teams(self):
        """ Generate teams """
        for group in self.groups.values():
            for team in group.teams:
                yield team

    async def reset(self):
        """ Reset things to start again """
        await self.load_group_games()

    async def run(self):
        """ Run the games 

        run the group stage

        generate knockout bracket

        run knockout

        collect stats

        reset

        AND/OR:

        Generate events.
        """
        print('jsf: run start')
        print(self.now)
        print('load games')
        await self.reset()

        print('loop forever?')
        while not self.games.empty():

            game = await self.games.get()

            if game.when < self.now:
                print(self.now, game)

                # Run the game
                await game.run(self.events)
                # Do post processing depending on the type of Game

            else:
                await self.games.put(game)

            await curio.sleep(0)


class Place:

    def __str__(self):

        return self.name

    def __repr__(self):

        return str(self)

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
                     ascore=4, bscore=0),

                Game(egy, urg, datetime(2018, 6, 15, 12, 0),
                     where=places['yekaterinburg'],
                     ascore=1, bscore=2),

                
                Game(rus, egy, datetime(2018, 6, 19, 18, 0),
                     where=places['stpetersberg'],
                    ),
                
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
                     ascore=2, bscore=2),
                     
                Game(por, spa, datetime(2018, 6, 15, 18, 0),
                     where=places['sochi'],
                     ascore=3, bscore=2),

                
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
                     ascore=1, bscore=2),
                     
                Game(per, den, datetime(2018, 6, 16, 14, 0),
                     where=places['saransk'],
                     ascore=2, bscore=2),

                
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
                     ascore=3, bscore=2),

                Game(cro, nig, datetime(2018, 6, 16, 19, 0),
                     where=places['kaliningrad'],
                     ascore=2, bscore=2),

                
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
                     ascore=2, bscore=4),
                     
                Game(bra, swi, datetime(2018, 6, 17, 18, 0),
                     where=places['rostovondon'],
                     ascore=3, bscore=3),

                
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
                     ascore=1, bscore=2),

                Game(swe, sko, datetime(2018, 6, 18, 12, 0),
                     where=places['novgorod'],
                     ascore=3, bscore=2),

                
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
                     ascore=3, bscore=1),
                     
                Game(tun, eng, datetime(2018, 6, 18, 18, 0),
                     where=places['volgograd'],
                     ascore=0, bscore=0),

                
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
                     ascore=2, bscore=1),
                     
                Game(pol, sen, datetime(2018, 6, 19, 15, 0),
                     where=places['spartak'],
                     ascore=3, bscore=2),

                
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
    places['kazan'],
    places['sochi'],
    places['moscow'],
    places['novgorod'],

    places['samara'],
    places['rostovondon'],
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
    datetime(2018, 6, 30, 14, 0),
    datetime(2018, 6, 30, 18, 0),
    datetime(2018, 7,  1, 14, 0),
    datetime(2018, 7,  1, 18, 0),
    
    datetime(2018, 7,  2, 14, 0),
    datetime(2018, 7,  2, 18, 0),
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
jsf = JeuxSansFrontieres(groups, places=jsf_places, dates=jsf_dates)


# add a PI Gui?
class MexicanWaves(pigfarm.Yard):

    def __init__(self, parent, jsf=None, venues=None):
        """ Initialise the thing """

        super().__init__(parent)

        self.jsf = jsf

        self.messages = []

        self.when = datetime(2018, 6, 14)
        self.delta_t = 1.

        # teleprinter location
        self.teleprint_xxyy = .8, .025
        self.teleprints = []

        self.scan_venues(venues)

        self.add_event_map('r', self.reset)
        self.add_event_map('s', self.slower)
        self.add_event_map('w', self.faster)

    async def slower(self):
        """ Go slower """
        self.delta_t /= 2

    async def faster(self):
        """ Go faster """
        self.delta_t *= 2

    def scan_venues(self, venues):
        """ Set the lat lon bounds for the canvas """
        self.places = places = list(venues.values())

        minlat = min(x.lat for x in places)
        maxlat = max(x.lat for x in places)
        
        minlon = min(x.lon for x in places)
        maxlon = max(x.lon for x in places)

        height = maxlat - minlat
        width = maxlon - minlon

        wpad = width / 8
        hpad = height / 8

        # need to add padding to make grid
        self.xx = minlon - wpad
        self.yy = minlat - hpad

        self.xscale = width + (2 * wpad)
        self.yscale = height + (2 * hpad)


    def latlon2xy(self, place):
        """ Convert lat lon to yard coordinates """
        lat = place.lat
        lon = place.lon
        
        xx = int(((lon - self.xx) / self.xscale) * self.width)
        yy = self.height - int(((lat - self.yy) / self.yscale) * self.height)
 
        return xx, yy
        
        
    def step_balls(self):
        """ do something here """
        #print('mexican wave step_balls')
        for place in self.places:
            #print(place)
            #print(self.width, self.height, xx, yy)
            size = 5
            self.ball(place, fill='red', size=5)

            self.message(place.name, place, yoff=-20, fill='yellow')
            
        #print('done places')
        locations = defaultdict(list)
        
        for team in jsf.generate_teams():
            team.where(self.when)
            xx, yy = self.latlon2xy(team)

            locations[(xx, yy)].append(team)

        # Now draw the things
        for key in locations.keys():
            xx, yy = key
            yoff = 30
            for team in locations[key]:
                self.message(team.name, team, yoff=yoff, fill='green')

                yoff += 30

        self.show_score_flashes()

        self.show_tables()
                
        self.when += timedelta(hours=self.delta_t)

        
    def draw(self):
        pass

    async def reset(self):
        """ Reset timer """
        self.when = datetime(2018, 6, 14)

        self.jsf.reset()
        await self.jsf.load_group_games()

        self.messages = []

    async def score_flash(self):

        while True:
            info = await self.jsf.events.get()

            self.messages.append(info)

            self.teleprint(**info)


    def show_score_flashes(self):
        """ Show the score flashes """
        xx, yy = self.teleprint_xxyy

        for msg, fill in self.teleprints:
            
            self.message(msg=msg, fill=fill, xx=xx, yy=yy)
            xx, yy = xx, yy + .025

        # Now do messages
        keep = {}
        for info in reversed(self.messages):
            when = info['when']
            
            if self.when < when + timedelta(hours=48):
                pos = self.layout(**info)
                if pos in keep:
                    continue
                keep[pos] = info

                self.message(**info)

        self.messages = list(keep.values())


    def teleprint(self, msg=None, fill='orange', **kwargs):
        """ teleprinter messages """
        self.teleprints.append((msg, fill))

        if len(self.teleprints) > 10:
            del self.teleprints[0]

    def layout(self, where=None, xx=None, yy=None, **kwargs):
        """ layout for location """
        if xx is None or yy is None:
            xx, yy = self.latlon2xy(where)
        else:
            xx *= self.width
            yy *= self.height

        return xx, yy


    def message(self, msg=None, where=None, fill='red', size=5, xoff=0, yoff=0,
                xx=None, yy=None, **kwargs):
        """ Message from a place """

        xx, yy = self.layout(where, xx, yy)

        self.canvas.create_text((xx + xoff, yy + yoff), text=msg, fill=fill)


    def show_tables(self):
        
        position = [
            [.05, .1],
            [.15, .1],
            
            [.05, .25],
            [.15, .25],
            
            [.85,  .75],
            [.95,  .75],
            
            [.85, .9],
            [.95, .9],
            ]

        for label, group in self.jsf.groups.items():
            
            gindex = ord(label) - ord('a')

            xx, yy = position[gindex]
        
            for team in group.get_table()[::-1]:
                self.message(
                    msg=team.statto(),
                    xx=xx,
                    yy=yy,
                    fill='cyan')
                yy -= 0.025


    def ball(self, place, fill='red', size=5, xoff=0, yoff=0):
        """ Message from a place """

        xx, yy = self.latlon2xy(place)

        self.canvas.create_oval(
            xx+xoff-size,
            yy+yoff-size,
            xx+xoff+size, yy+yoff+size, fill='red')

    async def run(self):
        """ Run the waves """
        print('running mexican wave')

        print('spawning jsf')
        jsf = await curio.spawn(self.jsf.run)

        score_flashes = await curio.spawn(self.score_flash)

        self.set_background()
        
        while True:
            self.canvas.delete('all')

            self.draw()
            
            self.step_balls()

            self.jsf.now = self.when
            
            await curio.sleep(self.sleep)            


parser = argparse.ArgumentParser()
parser.add_argument('--nopig', action='store_true')
args = parser.parse_args()            

if args.nopig:
    sys.exit()
    
farm = pigfarm.PigFarm()

from karmapi.mclock2 import GuidoClock
    
farm.add(GuidoClock)
farm.add(MexicanWaves, dict(jsf=jsf, venues=places))

# add a random wc time warper?
curio.run(farm.run(), with_monitor=True)



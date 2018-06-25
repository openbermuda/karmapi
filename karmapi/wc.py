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
import csv
from collections import Counter, defaultdict, deque
from datetime import datetime, timedelta
import calendar
import sys

import curio

from karmapi import pigfarm, beanstalk


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
        self.home = False

        self.reset()


    def reset(self):

        self.points = 0
        self.played = 0
        self.yellow = 0
        self.red = 0
        self.goals = 0
        self.against = 0
        self.home = None

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

        if self.home is not None:
            self.lat, self.lon = self.home.lat, self.home.lon
            return self.lat, self.lon

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

    def go_home(self):

        self.home = NorthPole()

    def __str__(self):
 
       return self.name


    def stats(self):

        return dict(
            played = self.played,
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
        msg += " {played:4d}".format(**stats)
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

class GameEvent:
        
    def __init__(self, when=None, game=None, jsf=None):

        self.when = when
        self.game = game
        self.jsf = jsf
        self.start_evt = curio.Event()

    async def start(self, delay):

        # want to wait appropriate time, for now just 1
        try:
            await curio.timeout_after(delay, self.start_evt.wait)
        except curio.TaskTimeout:
            pass

        await self.run()

    async def run(self):

        print(self.when, self.game)


    def __str__(self):

        return 'GAMEEVENT ' + str(self.when)

        
class TeamEvent(GameEvent):
    """ An event that involves one team in the game """
    
    def __init__(self, team, who=None, when=None, game=None, og=False, **kwargs):

        super().__init__(when, game, **kwargs)

        self.team = team
        self.who = who
        self.og = og
        
class Goal(TeamEvent):

    async def run(self):

        print(self.team, self.when, self.who, self.game, self.og)
        # this sort of seems weird
        await self.game.goal(self.team, self.who, self.when)


class KickOff(GameEvent):

    async def run(self):

        print(self.when, self.game, 'KICK OFF')
        await self.game.kick_off(self.jsf)

class HalfTime(GameEvent):

    async def run(self):

        print(self.when, self.game, 'HALF TIME')
        await self.game.half_time()

class FullTime(GameEvent):

    async def run(self):

        print(self.when, self.game, 'FULL TIME')
        done = await self.game.full_time()

        if done:
            self.jsf.apres_match(self.game)
        else:
            print('NOT DONE???')

        


class Penalty(Goal):
    """ Penalty in a shoot out 

    which: which penalty: 1, 2, 3 etc
    """
    def __init__(self, team, which=None, score=True, **kwargs):

        super().__init__(team, **kwargs)
        
        self.which = which
        self.score = True
        self.penalty = True

    async def run(self):

        await self.game.penalty(self)


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
        self.label = ''

        # ignore ascore/bscore, let events do the work
        self.ascore = None
        self.bscore = None
        
        self.apen = []
        self.bpen = []
        
        self.minute = 0

        self.end_event = curio.Event()

        # flag if score was simulated - do this if game is in the future
        self.simulated = self.when > datetime.now()
        print('SIMULATED', self.simulated)
        self.number = Game.NUMBER
        Game.NUMBER += 1


    def __hash__(self):
        
        return id(self)

    def reset(self):
        """ Reset score if it was random """
        if self.simulated:
            self.ascore = self.bscore = 0
            
            self.apen = []
            self.bpen = []

            self.minute = 0

    def __str__(self):

        msg = ' '. join((
            str(self.label),
            str(self.a.name),
            'v',
            str(self.b.name),
            self.day_name(),
            str(self.when),
            str(self.where)))

        if self.ascore is not None:
            msg += ' ' + '-'.join((str(self.ascore), str(self.bscore)))

        return msg

    def day_name(self):

        return calendar.day_name[self.when.weekday()]

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

    async def kick_off(self, jsf):
        """ Game has kicked off """
        print('wtf ko', self)
        self.ascore = 0
        self.bscore = 0

        if not self.simulated:
            return

        print('SIMULATING', self)
        minutes = 45 + randint(0, 7)

        await self.half(minutes)

        await self.half_time()

        await self.second_half()

        done = await self.full_time()
        
        ko = not self.is_group()

        # knockout match, are we done?
        if ko and self.ascore == self.bscore:
            
            await self.extra_time()
            await self.extra_half_time()
            await self.extra_full_time()

            if self.ascore == self.bscore:
                await self.penalties()

        print('APRES!!!')
        jsf.apres_match(self)

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

        await self.flash(fill='blue', tag='HT')

    async def second_half(self):
        minutes = 45 + randint(0, 7)
        await self.half(minutes)

    async def full_time(self):

        done = False
        if self.is_group():
            done = True

        elif self.ascore != self.bscore:
            done = True

        if done:
            await self.end_event.set()
            
        await self.flash(fill='yellow', tag='FT')

        return done

    async def extra_time(self):
        minutes = 15 + randint(0, 3)
        await self.half(minutes)

    async def extra_half_time(self):
        pass

    async def extra_full_time(self):
        minutes = 15 + randint(0, 3)
        await self.half(minutes)

    async def penalties(self):
        """ Don't miss this """
        first, second = self.a, self.b

        if random() < 0.5:
            first, second = second, first

        total = 0
        done = False
        while not done:
            done = self.penalty(first)
            first, second = second, first

    def penalty(self, team):
        """ Take a penalty """
        which = len(self.apen) + len(self.bpen)
        
        if random() < 0.5:
            pen = Penalty(team, score=True, which=which, game=self,
                          when=self.when + timedelta(minutes=120 + which),
                          who = randint(1, 23))

            if team is self.a:
                self.apen.append(pen)
            else:
                self.bpen.append(pen)

        return self.all_over()

    def pens_score(self):
        """ score in penalties """
        apens = [x for x in self.apen if x.score]
        bpens = [x for x in self.bpen if x.score]

        return len(apens), len(bpens)
        

    def all_over(self):
        """ Are the pens done? """

        a, b = self.pens_score()
        
        if a == b:
            return False

        aa = len(self.apen)
        bb = len(self.bpen)
        
        which = aa + bb

        if which <= 10:
            aleft = 5 - aa
            bleft = 5 - bb

        else:
            aleft = bleft = 0

            if aa < bb:
                aleft = 1
            if bb < aa:
                bleft = 1

        if b > a + aleft:
            return True

        if a > b + bleft:
            return True

    async def goal(self, team, who=None, when=None):

        if self.ascore is None:
            print('wtf', self, who, when, team)

        print('zzzz', team, self.a.name, self.b.name, self.ascore, self.bscore)
            
        if team is self.a:
            self.ascore += 1
        else:
            self.bscore += 1

        minute = int((when - self.when).total_seconds() / 60)
        await self.flash(" %dm" % minute, fill='green')


    async def yellow(self, team, who=None, when=None):
        pass

    async def red(self, team, who=None, when=None):
        pass

    async def sub(self, team, off=None, on=None, when=None):
        pass

    def apres_match(self):
        
        a = self.a
        b = self.b

        a.goals += self.ascore
        b.goals += self.bscore

        a.against += self.bscore
        b.against += self.ascore

        if self.is_group():

            if self.ascore > self.bscore:
                a.points += 3

            elif self.bscore > self.ascore:
                b.points += 3

            else:
                a.points += 1
                b.points += 1

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

    def winner(self):
        """ Return winning team """
        if self.ascore > self.bscore:
            return self.a
        elif self.bscore > self.ascore:
            return self.b

        # penalties
        aa, bb = self.pens_score()
        if aa > bb:
            return self.a

        return self.b

    def loser(self):

        win = self.winner()
        if win == self.a:
            return self.b
        
        return self.a


class Group:

    def __init__(self, teams=None, games=None):

        self.teams = teams
        self.games = games or []
        self.played = 0

    def winner(self):
        """ Pick a winner """
        return self.get_table()[0]

    def second(self):
        """ Pick a second """
        return self.get_table()[1]

    def is_finished(self):

        size = len(self.teams)
        return self.played == (size * (size - 1)) / 2

    def __str__(self):

        return str(self.teams, self.games)

    def reset(self):
        """ reset for a new run """
        for game in self.games:
            game.reset()

        for team in self.teams:
            team.reset()

        self.played = 0


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
    def __init__(self, groups, places=None, dates=None,
                 when=None, game_events=None):
        self.groups = groups

        # places and dates for knockout stage
        self.places = places
        self.dates = dates

        self.when = when or datetime(2018, 6, 14)
        self.start = self.when

        self.start_time = datetime.now()

        # factor to warp time by
        self.timewarp = 120 / (30 * 24 * 60 * 60)
        self.sleep = 0.01

        self.knockout = []
        self.winners = {}
        self.seconds = {}

        self.events = curio.UniversalQueue()
        self.game_events = game_events

    def warp(self, when):
        """ convert when to a delay in seconds """ 
        start = self.start
        seconds = (when - start).total_seconds()

        # how far are we in?
        elapsed = (datetime.now() - self.start_time).total_seconds()

        print('WARP', when, seconds, elapsed)

        warp = (seconds * self.timewarp) - elapsed
        return warp

    def iwarp(self, ticks):
        """ convert tick time to a datetime  """
        return self.start + timedelta(seconds=ticks / self.timewarp)


    async def dispatch_events(self):
        """ Dispatch events to the appropriate game """

        if not self.game_events:
            return
        
        # build game lookup
        gl = {}
        for game in self.generate_games():
            game.events = self.events
            gl[(game.when.date(), game.a.name.lower(), game.b.name.lower())] = game

        knockout = []
        etasks = []
        for event in parse_events(self.game_events):
            when, ateam, bteam, what, extras = event

            key = when.date(), ateam, bteam

            game = gl.get(key)

            if not game:
                knockout.append(game)

            # turn team names into teams
            ateam = name2team(ateam)
            bteam = name2team(bteam)
            
            # got the game.  now create an appropriate event
            delay = self.warp(when)
            print('wtf', when, delay, what, self)
            if what == 'goal':
                team = name2team(extras[0])

                who = int(extras[1])
                og = False
                if who > 23:
                    og = True
                    who -= 100

                event = Goal(team, who, when, game, og, jsf=self)

                task = await curio.spawn(event.start, delay)
                etasks.append(task)

            elif what == 'ko':
                event = KickOff(when, game, jsf=self)
                task = await curio.spawn(event.start, delay)
                etasks.append(task)

            elif what == 'ft':

                event = FullTime(when, game, jsf=self)
                task = await curio.spawn(event.start, delay)
                etasks.append(task)

            else:
                # just print out the event info
                print('*****', when, ateam, bteam, what, extras)

        for task in etasks:
            await task.join()

        # fixme do something with knockout
        pass

    async def load_group_games(self):
        """ Put the group games into the game queue """

        kos = []
        
        for label, group in self.groups.items():
            group.name = label
            group.reset()
            for game in group.games:
                game.group = group
                game.label = label.upper()

                game.a.games.append(game)
                game.b.games.append(game)

                if game.simulated:
                    print('XXXXXXXX', game.when)
                    kos.append(KickOff(game.when, game, jsf=self))

        self.its_a_knockout()

        await self.dispatch_events()

        for game in self.knockout:
            game.events = self.events
            kos.append(KickOff(game.when, game, jsf=self))

        kotasks = []
        for ko in kos:
            task = await curio.spawn(ko.start, self.warp(ko.when))
            kotasks.append(task)

        for ko in kotasks:
            await ko.join()

    def its_a_knockout(self):
        """ Set up knockout stage """
        self.knockout = []
        Game.NUMBER = 49
        
        places = self.places or (['???'] * len(games))
        dates = self.dates or [datetime.today()] * len(games)

        for where, when in zip(places, dates):
            self.knockout.append(Game(None, None, when, where))

        groups = self.groups
        key = sorted(groups.keys())

        key = list(key)
        print(key)

        key2 = ''
        for x in range(0, len(key), 2):
            key2 += key[x+1] + key[x]

        print(key2) 

        games = []

        ix = 0
        for gps in key, key2:
            for x in range(0, len(key), 2):
            
                a = gps[x]
                b = gps[x+1]

                self.winners[a] = self.knockout[ix], 'a'
                self.seconds[b] = self.knockout[ix], 'b'
                ix += 1

        # now do knockout stage
        ko = self.knockout
        for ix, game in enumerate(ko[:8]):
            gix = 8 + int(ix / 2)
            if ix % 2 == 0:
                self.winners[game.number] = self.knockout[gix], 'a'
            else:
                self.winners[game.number] = self.knockout[gix], 'b'

        for ix, game in enumerate(ko[8:12]):
            gix = 12 + int(ix / 2)
            if ix % 2 == 0:
                self.winners[game.number] = self.knockout[gix], 'a'
            else:
                self.winners[game.number] = self.knockout[gix], 'b'

        for ix, game in enumerate(ko[12:14]):
            if ix % 2 == 0:
                self.winners[game.number] = self.knockout[15], 'a'
                self.seconds[game.number] = self.knockout[14], 'b'
            else:
                self.winners[game.number] = self.knockout[15], 'b'
                self.seconds[game.number] = self.knockout[14], 'a'


    def generate_teams(self):
        """ Generate teams """
        for group in self.groups.values():
            for team in group.teams:
                yield team

    def generate_games(self):
        """ Generate games """
        games = set()

        for team in self.generate_teams():
            for game in team.games:
                games.add(game)

        for game in sorted(games):
            yield game
        

    def apres_match(self, game):
        """ Deal with updating of knockout stage """

        game.apres_match()

        if game.number == 63:
            print('third place:', game.winner())
            return
        if game.number == 64:
            print('Winner:', game.winner())
            return

            
        if game.is_group():
            group = game.group
            group.played += 1

            game.a.played += 1
            game.b.played += 1
            
            key = game.label.lower()
            kgame, label = self.winners[key]
            wteam = group.winner()
            setattr(kgame, label, wteam)
            if group.is_finished():
                wteam.games.append(kgame)
                
            kgame, label = self.seconds[key]
            steam = group.second()
            setattr(kgame, label, group.second())
            if group.is_finished():
                steam.games.append(game)

                for team in group.teams:
                    if team not in (wteam, steam):
                        print('out', team)
                        team.go_home()

        else:
            kgame, label = self.winners[game.number]
            wteam = game.winner()
            setattr(kgame, label, game.winner())
            wteam.games.append(kgame)

            if game.number in self.seconds:
                kgame, label = self.seconds[game.number]
                lteam = game.loser()
                setattr(kgame, label, lteam)
                lteam.games.append(kgame)
            else:
                game.loser().go_home()
                

    async def reset(self):
        """ Reset things to start again """
        self.now = self.start
        Game.NUMBER -= len(self.knockout)

        self.knockout = []
        self.winners = {}
        self.seconds = {}

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
        await self.reset()

        if self.dump:
            for game in self.generate_games():
                dump(game, self.dump)

            self.dump.close()
            sys.exit(0)

        return



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

class NorthPole(Place):
    """  Where teams go when out? """

    name = 'North Pole'
    lat = 90
    lon = 0

    

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

    def __init__(self, parent, jsf=None, venues=None, gallery='.',
                 dump=None, events=None):
        """ Initialise the thing """

        super().__init__(parent)

        self.jsf = jsf
        self.jsf.dump = dump
        self.jsf.game_events = events

        self.messages = []

        self.start_time = datetime.now()
        self.delta_t = 1.

        # teleprinter location
        self.teleprint_xxyy = .8, .025
        self.teleprints = []

        self.scan_venues(venues)

        self.add_event_map('r', self.reset)
        self.add_event_map('S', self.slower)
        self.add_event_map('M', self.faster)
        self.add_event_map('m', self.toggle_show_games)
        self.add_event_map('g', self.toggle_show_groups)
        self.add_event_map('t', self.toggle_show_teams)
        self.add_event_map('j', self.previous_group)
        self.add_event_map('k', self.next_group)
        #self.add_event_map(' ', self.toggle_pause)
        
        self.game_view = False
        self.team_view = False
        self.group_view = False
        self.which_group = 0


    async def slower(self):
        """ Go through time more slowly """
        self.delta_t /= 2

    async def faster(self):
        """ Go through time more quickly  """
        self.delta_t *= 2

    async def toggle_show_games(self):
        """ Toggle matches view """
        self.game_view = not self.game_view

    async def toggle_show_teams(self):
        """ Toggle teams view """
        self.game_view = not self.team_view

    async def toggle_show_groups(self):
        """ Toggle groups view """
        self.group_view = not self.group_view

    async def next_group(self):
        """ Go to next group """
        self.which_group += 1

        if self.which_group == len(self.jsf.groups):
            self.which_group = 0

    async def previous_group(self):
        """ Go to previous group """
        self.which_group -= 1

        if self.which_group < 0:
            self.which_group += len(self.jsf.groups)
        

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
        
        
    async def step_balls(self):
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

            wtit = self.what_time_is_it()
            team.where(wtit)
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

        if self.game_view:
            self.show_games()

        if self.team_view:
            self.show_teams()

        if self.group_view:
            self.show_groups()

        if not self.group_view and not self.team_view and not self.game_view:
            self.show_tables()

            self.show_knockout()


    def what_time_is_it(self):

        elapsed = (datetime.now() - self.start_time).total_seconds()

        return self.jsf.iwarp(elapsed)

        
    def draw(self):

        import time
        self.beanstalk.create_time = time.time()
        #print(self.beanstalk.xx, self.beanstalk.yy)

        self.beanstalk.draw(self.canvas, self.width, self.height, 'red')

    async def reset(self):
        """ Reset timer """
        self.start_time = datetime.now()

        self.messages = []
        self.teleprints =[]

        await self.jsf.reset()
        #await self.jsf.load_group_games()


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
            
            if self.what_time_is_it() < when + timedelta(hours=48):
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
            [.10, .1],
            [.25, .1],
            
            [.10, .25],
            [.25, .25],
            
            [.75,  .75],
            [.90,  .75],
            
            [.75, .9],
            [.90, .9],
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

    def show_groups(self):

        xx = 0.6
        yy = 0.05

        which = chr(self.which_group + ord('a'))

        group = self.jsf.groups[which]

        for game in group.games:

            self.message(msg=str(game),
                         xx=xx, yy=yy, fill='magenta')

            yy += 0.025

    def show_teams(self):

        pass

                
    def show_games(self):

        xx = 0.2
        yy = 0.05
        
        for game in self.jsf.generate_games():
            print(game)

            self.message(msg=str(game),
                         xx=xx, yy=yy, fill='pink')

            yy += 0.025

    def show_knockout(self):

        if not self.jsf.knockout:
            return
        xx = .1
        yy = .6
        yinc = 0.025
        for ix, game in enumerate(self.jsf.knockout):
            aa = game.a or '   '
            bb = game.b or '   '

            ascore = game.ascore
            bscore = game.bscore
            if ascore is None: ascore = '-'
            if bscore is None: bscore = '-'
            
            self.message(msg="{} {} {}  {}".format(
                aa, ascore, bscore, bb),
                xx=xx, yy=yy, fill='green')
            
            yy += 0.05

            if ix in [7, 11, 13]:
                xx += .1
                yy = .6
                yinc *= 2

        final = self.jsf.knockout[-1]
        if final.ascore != None:
            xx += 0.1
            yy = 0.6
            for game in final.winner().games:
                print(game.where, game.when)
            self.message(msg="{}".format(
                final.winner().name),
                xx=xx, yy=yy,
                fill='gold')
            


    def ball(self, place, fill='red', size=5, xoff=0, yoff=0):
        """ Draw a filled circle at place """

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

        self.beanstalk = beanstalk.BeanStalk()
        self.beanstalk.xx = 0.5
        self.beanstalk.yy = 0.5
        self.beanstalk.x = ''
        
        while True:
            self.canvas.delete('all')

            image = self.find_image('1991')
            if image:
                #print(image)
                image = self.load_image(image)
                #print(image.size)
                image = image.resize((int(self.height), int(self.width)))
                #print(image.size, self.width, self.height)
                self.beanstalk.image = image

            self.draw()

            # step balls
            await self.step_balls()

            #self.jsf.now = self.when()

            # wait for event here.  We want to repaint in a minute game time
            await curio.sleep(self.sleep)            

def dump(game, out):

    now = datetime.now()
    print('dumping')
    when = game.when

    if when < now:
        return
    
    print(when.year, when.month, when.day, when.hour, sep=', ', end=', ', file=out)
    print(game.a, game.b, 0, 'ko', 0, 0, sep=', ', file=out)

    print(when.year, when.month, when.day, when.hour, sep=', ', end=', ', file=out)
    print(game.a, game.b, 45, 'ht', 0, 0, sep=', ', file=out)

    print(when.year, when.month, when.day, when.hour, sep=', ', end=', ', file=out)
    print(game.a, game.b, 90, 'ft', 0, 0, sep=', ', file=out)

def parse_events(events, out=None):

    if out:
        out = csv.writer(out)
    
    for row in csv.reader(events):

        if out:
            row = [x.strip() for x in row]
            out.writerow(row)
            continue

        if not row:
            continue

        if row[0].startswith('#'):
            continue
        
        year, month, day, hour = [int(x) for x in row[:4]]

        a, b = row[4], row[5]

        minute = int(row[6])
        what = row[7].strip().lower()
        extras = [x.strip().lower() for x in row[8:]]

        when = datetime(year, month, day, hour, 0)
        when += timedelta(minutes=minute)

        yield when, a.lower().strip(), b.lower().strip(), what, extras
        
    

def shuffle_events(events, out=None):
    
    if out:
        writer = csv.writer(out)
    else:
        writer = csv.writer(sys.stdout)
        
    for row in csv.reader(events):
        
        row = row[:4] + row[5:7] + row[4:5] + row[7:]
        row = [x.strip() for x in row]
        writer.writerow(row)

def name2team(name):
    """ Convert string to team object """
    return globals()[name]


parser = argparse.ArgumentParser()
parser.add_argument('--nopig', action='store_true')
parser.add_argument('--gallery')
parser.add_argument('--dump')
parser.add_argument('--events')
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
    
    
farm.add(GuidoClock)
farm.add(MexicanWaves, dict(jsf=jsf, venues=places, gallery=args.gallery,
                            events=args.events,
                            dump=xdump))

# add a random wc time warper?
curio.run(farm.run(), with_monitor=True)



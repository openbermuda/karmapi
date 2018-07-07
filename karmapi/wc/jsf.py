""" Jeus Sans Frontieres

"""
from datetime import datetime, timedelta

import curio

from .events import *
from .game import Game

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
                 when=None, game_events=None, name2team=None):
        self.groups = groups

        # places and dates for knockout stage
        self.places = places
        self.dates = dates
        self.name2team = name2team

        self.when = when or datetime(2018, 6, 14)
        self.start = self.when

        self.start_time = datetime.utcnow()

        # factor to warp time by
        self.timewarp = 1 / (30 * 24 * 60 * 60)
        self.sleep = 0.01

        self.knockout = []
        self.winners = {}
        self.seconds = {}

        self.events = curio.UniversalQueue()

        self.game_events = game_events or []

        self.tasks = []
            
    def warp(self, when):
        """ convert when to a delay in seconds """ 
        start = self.start
        seconds = (when - start).total_seconds()

        # how far are we in?
        elapsed = (datetime.utcnow() - self.start_time).total_seconds()

        warp = (seconds * self.timewarp) - elapsed
        return warp

    def iwarp(self, ticks):
        """ convert tick time to a datetime  """
        return self.start + timedelta(seconds=ticks / self.timewarp)


    def match_game(self, key):

        when, ateam, bteam = key

        # build game lookup
        gl = {}
        for game in self.generate_games():
            game.events = self.events

            aname = bname = '-'
            if game.a:
                aname = game.a.name.lower()
                bname = game.b.name.lower()

            gkey = (game.when, aname, bname)
            if gkey in gl:
                raise ValueError("Duplicate game key %s" % str(key))
            gl[gkey] = game

        # Now find the game for this key
        game = gl.get(key)

        if game is None:
            game = gl.get((key[0], '-','-'))

        return game

    
    async def dispatch_events(self):
        """ Dispatch events to the appropriate game """

        if not self.game_events:
            return
        
        knockout = []
        etasks = []
        for event in self.game_events:

            kotime, when, ateam, bteam, what, extras = event

            key = kotime, ateam, bteam

            game = self.match_game(key)

            if not game:
                knockout.append((key, event))
                continue

            # turn team names into teams
            ateam = self.name2team(ateam)
            bteam = self.name2team(bteam)
            
            # got the game.  now create an appropriate event
            if what == 'goal':
                team, who, og = self.whodunnit(extras)
                event = Goal(team, who, when, game, og, jsf=self)
                task = await curio.spawn(event.start)
                etasks.append(task)

            elif what == 'yellow':
                team, who, og = self.whodunnit(extras)
                event = Yellow(team, who, when, game, jsf=self)
                task = await curio.spawn(event.start)
                etasks.append(task)
                

            elif what == 'ko':
                event = KickOff(when, game, jsf=self)
                task = await curio.spawn(event.start)
                etasks.append(task)

            elif what == 'penalty':
                team, who, og = self.whodunnit(extras)

                score = int(extras[-1]) != 0
                
                event = Penalty(team, who, when, game, score, jsf=self)
                task = await curio.spawn(event.start)
                etasks.append(task)

            elif what == 'ft':

                event = FullTime(when, game, jsf=self)
                task = await curio.spawn(event.start)
                etasks.append(task)

            else:
                # just print out the event info
                print('*****', when, ateam, bteam, what, extras)

        self.tasks += etasks


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
                    kos.append(KickOff(game.when, game, jsf=self))

        self.its_a_knockout()

        await self.dispatch_events()

        for game in self.knockout:
            game.events = self.events
            if game.simulated:
                kos.append(KickOff(game.when, game, jsf=self))

        kotasks = []
        for ko in kos:
            task = await curio.spawn(ko.start)
            kotasks.append(task)

        self.tasks += kotasks


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

        key2 = ''
        for x in range(0, len(key), 2):
            key2 += key[x+1] + key[x]

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
                self.winners[game.number] = self.knockout[14], 'a'
                self.seconds[game.number] = self.knockout[15], 'b'
            else:
                self.winners[game.number] = self.knockout[14], 'b'
                self.seconds[game.number] = self.knockout[15], 'a'

            

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

        games.update(self.knockout)
        
        for game in sorted(games):
            yield game


    def apres_match(self, game):
        """ Deal with updating of knockout stage """

        game.apres_match()

        if game.number == 64:
            print('third place:', game.winner())
            return
        if game.number == 63:
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
            setattr(kgame, label, steam)
            if group.is_finished():
                steam.games.append(kgame)

                for team in group.teams:
                    if team not in (wteam, steam):
                        print('out', team)
                        team.go_home()

        else:
            kgame, label = self.winners[game.number]
            wteam = game.winner()

            setattr(kgame, label, wteam)
            print('knockout winner:', wteam, game, kgame)
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
        for task in self.tasks:
            await task.cancel()
            
        self.now = self.start
        self.start_time = datetime.utcnow()
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



    def whodunnit(self, extras):
    
        team = self.name2team(extras[0])

        who = int(extras[1])
        og = False
        if who > 23:
            og = True
            who -= 100

        return team, who, og

    
def dump(game, out):

    now = datetime.utcnow()
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


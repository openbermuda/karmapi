import curio

class GameEvent:
        
    def __init__(self, when=None, game=None, jsf=None):

        self.when = when
        self.game = game
        self.jsf = jsf
        self.start_evt = curio.Event()

    async def start(self):

        # want to wait appropriate time, for now just 1
        delay = self.jsf.warp(self.when)
        try:
            await curio.timeout_after(delay, self.start_evt.wait)
        except curio.TaskTimeout:
            pass

        await self.run()

    async def run(self):

        print('ruunning: ', self.when, self.game)


    def __str__(self):

        return 'GAMEEVENT ' + str(self.when)

class CheckPoint(GameEvent):

    async def run(self):

        print('check point: ', self.when, self.game)
        
        await self.jsf.check_point()

    def __str__(self):

        return 'CHECK POINT ' + str(self.when)
    

        
class TeamEvent(GameEvent):
    """ An event that involves one team in the game """
    
    def __init__(self, team, who=None, when=None, game=None, og=False, **kwargs):

        super().__init__(when, game, **kwargs)

        self.team = team
        self.who = who
        self.og = og
        
class Goal(TeamEvent):

    async def run(self):

        print('goal', self.team, self.when, self.who, self.game, self.og)
        # this sort of seems weird
        await self.game.goal(self.team, self.who, self.when)


class Yellow(TeamEvent):

    async def run(self):

        print('yellow', self.team, self.when, self.who, self.game, self.og)
        # this sort of seems weird
        await self.game.yellow(self.team, self.who, self.when)


class KickOff(GameEvent):

    async def run(self):

        print('ko', self.when, self.game, 'KICK OFF')
        await self.game.kick_off(self.jsf)

class HalfTime(GameEvent):

    async def run(self):

        print(self.when, self.game, 'HALF TIME')
        await self.game.half_time()

class FullTime(GameEvent):

    async def run(self):

        print(self.when, self.game, 'FULL TIME')
        await self.game.full_time()

        self.jsf.apres_match(self.game)
        


class Penalty(Goal):
    """ Penalty in a shoot out 

    which: which penalty: 1, 2, 3 etc
    """
    def __init__(self, team, who=None, when=None, game=None, score=False, **kwargs):

        super().__init__(team, who=who, when=when, game=game, **kwargs)

        print('PEN', self.when, team, score)
        
        self.score = score
        self.penalty = True

    async def run(self):

        await self.game.penalty(self)


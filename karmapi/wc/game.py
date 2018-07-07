import calendar
from datetime import datetime, timedelta
from random import random, randint

from .events import Penalty

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

        # flag if score was simulated - do this if game is in the future
        self.simulated = self.when > datetime.utcnow()
        if self.simulated:
            print('SIMULATED', self.simulated, self)

        # this has to go away..
        self.number = Game.NUMBER
        Game.NUMBER += 1


    def __hash__(self):
        
        return id(self)

    def reset(self):
        """ Reset score if it was random """
        self.ascore = self.bscore = 0
            
        self.apen = []
        self.bpen = []

        self.minute = 0

    def __str__(self):

        aname = bname = '---'
        if self.a:
            aname = self.a.name

        if self.b:
            bname= self.b.name
    
        msg = ' '. join((
            str(self.label),
            aname,
            'v',
            bname,
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
        self.reset()

        if not self.simulated:
            return

        print('SIMULATING', self)
            
        minutes = 45 + randint(0, 7)

        await self.half(minutes)

        await self.half_time()

        await self.second_half()

        await self.full_time()
        
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

        await self.flash(fill='yellow', tag='FT')

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
            done = self._penalty(first)
            first, second = second, first

    def _penalty(self, team):
        """ Simulate a penalty """
        which = len(self.apen) + len(self.bpen)

        score = False
        if random() < 0.8:
            score = True
            
        pen = Penalty(team, score=score, game=self,
                      when=self.when + timedelta(minutes=120 + which),
                          who = randint(1, 23))

        if team is self.a:
            self.apen.append(pen)
        else:
            self.bpen.append(pen)

        return self.all_over()

    async def penalty(self, pen):

        if pen.team is self.a:
            self.apen.append(pen)
        else:
            self.bpen.append(pen)

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

        if team is self.a:
            self.ascore += 1
        else:
            self.bscore += 1

        minute = int((when - self.when).total_seconds() / 60)
        await self.flash(" %dm" % minute, fill='green')

        
    async def yellow(self, team, who=None, when=None):
        
        if team is self.a:
            self.a.yellow += 1
        else:
            self.b.yellow += 1

        minute = int((when - self.when).total_seconds() / 60)
        await self.flash(" %dm" % minute, fill='purple', card='yellow')


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

    async def flash(self, tag='', fill='red', card=False):

        a = self.a
        b = self.b
        ascore = self.ascore
        bscore = self.bscore
        if self.apen:
            aa, bb = self.pens_score()
            ascore = "%d(%d)" % (self.ascore, aa)
            bscore = "%d(%d)" % (self.bscore, bb)
        
        msg = a.name + ' ' + str(ascore) + ' ' + str(bscore) + ' ' + b.name
        msg += ' ' + tag

        when = self.when + timedelta(minutes=self.minute)
        await self.events.put(dict(where=self.where, msg=msg, yoff=-90,
                                   when=when, fill=fill, card=card))

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

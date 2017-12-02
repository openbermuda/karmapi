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

"""

# number of teams
n = 32

class Team:

    def __init__(self, name=None, prob=None)
        """ Init the team with no name? """
        self.name= name

        self.prob = self.prob or 1 / n

class Group:

    def __init__(self, teams=None, games=None):

        self.teams = teams
        self.games = games

    def winner(self):
        """ Pick a winner """
        return self.teams[random.randint(0, n-1)]

    def second(self):
        """ Pick a second """
        return self.winner()


class Game:

    def __init__(self, a, b, when, where=None, ascore=None, bscore=None):

        self.a = a
        self.b = b
        self.when = when

        self.ascore = ascore or None
        self.bscore = bscore or None

    def score(self):
        """ Make up a score """
        ascore = random.randint(0, random.randint(0, 5))
        bscore = random.randint(0, random.randint(0, 5))

        return self.ascore or ascore, self.bscore or bscore
        

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
    a=Group('a', teams = [rus, sau, egy, urg]),
    b=Group('b', teams = [por, spa, mor, ira]),
    c=Group('c', teams = [fra, aus, per, den]),
    d=Group('d', teams = [arg, ice, cro, nig]),
    e=Group('e', teams = [bra, swi, crc, ser]),
    f=Group('f', teams = [ger, swe, mex, sko]),
    g=Group('g', teams = [bel, pan, tun, eng]),
    h=Group('h', teams = [pol, sen, col, jap]))
    
    

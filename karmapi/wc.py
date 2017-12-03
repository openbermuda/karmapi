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


"""
from datetime import datetime, timedelta
# number of teams
n = 32

class Team:

    def __init__(self, name=None, win=None):
        """ Init the team with no name? """
        self.name= name

        self.win = win or 1 / n

    def __str__(self):

        return self.name

class Group:

    def __init__(self, teams=None, games=None):

        self.teams = teams
        self.games = games or []

    def winner(self):
        """ Pick a winner """
        return self.teams[random.randint(0, n-1)]

    def second(self):
        """ Pick a second """
        return self.winner()

    def __str__(self):

        return str(self.teams, self.games)

class JeuxSansFrontieres:
    """  The knockout stage.

    Winners and seconds from group stage come through into a
    last 16 grid that looks something like this:

    w r
    w r   w  w    w  w   w  w   W

    w r   w  w
    w r

    w r   w  w    w  w
    w r   

    w r   w  w
    w r
    

    """

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
    a=Group(teams = [rus, sau, egy, urg],
            games = [
                Game(rus, sau, datetime(2018, 6, 14, 15, 0)),

                Game(egy, urg, datetime(2018, 6, 15, 12, 0)),

                
                Game(rus, egy, datetime(2018, 6, 19, 18, 0)),
                
                Game(urg, sau, datetime(2018, 6, 20, 15, 0)),
                

                Game(urg, rus, datetime(2018, 6, 19, 14, 0)),
                Game(sau, egy, datetime(2018, 6, 19, 14, 0)),
                ]),
                
    b=Group(teams = [por, spa, mor, ira],
            games = [
                Game(mor, ira, datetime(2018, 6, 15, 15, 0)),
                Game(por, spa, datetime(2018, 6, 15, 18, 0)),

                
                Game(por, mor, datetime(2018, 6, 20, 12, 0)),
                Game(ira, spa, datetime(2018, 6, 20, 18, 0)),
                
                Game(ira, por, datetime(2018, 6, 25, 18, 0)),
                Game(spa, mor, datetime(2018, 6, 25, 18, 0)),
                ]),
                
    c=Group(teams = [fra, aus, per, den],

            games = [
                Game(fra, aus, datetime(2018, 6, 16, 10, 0)),
                Game(per, den, datetime(2018, 6, 16, 14, 0)),

                
                Game(den, aus, datetime(2018, 6, 21, 12, 0)),
                Game(fra, per, datetime(2018, 6, 21, 15, 0)),
                
                Game(den, fra, datetime(2018, 6, 26, 14, 0)),
                Game(aus, per, datetime(2018, 6, 26, 14, 0)),
                ]),
                
    d=Group(teams = [arg, ice, cro, nig],

            games = [
                Game(arg, ice, datetime(2018, 6, 16, 13, 0)),

                Game(cro, nig, datetime(2018, 6, 16, 19, 0)),

                
                Game(arg, cro, datetime(2018, 6, 21, 18, 0)),
                
                Game(nig, ice, datetime(2018, 6, 22, 15, 0)),

                
                Game(nig, arg, datetime(2018, 6, 26, 18, 0)),
                Game(ice, cro, datetime(2018, 6, 26, 18, 0)),
                ]),
                
    e=Group(teams = [bra, swi, crc, ser],

            games = [
                Game(crc, ser, datetime(2018, 6, 17, 12, 0)),
                Game(bra, swi, datetime(2018, 6, 17, 18, 0)),

                
                Game(bra, crc, datetime(2018, 6, 22, 12, 0)),
                Game(ser, swi, datetime(2018, 6, 22, 18, 0)),
                
                Game(ser, bra, datetime(2018, 6, 27, 18, 0)),
                Game(swi, crc, datetime(2018, 6, 27, 18, 0)),
                ]),
                
    f=Group(teams = [ger, swe, mex, sko],

            games = [
                Game(ger, mex, datetime(2018, 6, 17, 15, 0)),

                Game(swe, sko, datetime(2018, 6, 18, 12, 0)),

                
                Game(sko, mex, datetime(2018, 6, 23, 15, 0)),
                Game(ger, swe, datetime(2018, 6, 23, 18, 0)),
                
                Game(sko, ger, datetime(2018, 6, 27, 14, 0)),
                Game(mex, swe, datetime(2018, 6, 27, 14, 0)),
                ]),
                
    g=Group(teams = [bel, pan, tun, eng],

            games = [
                Game(bel, pan, datetime(2018, 6, 18, 15, 0)),
                Game(tun, eng, datetime(2018, 6, 18, 18, 0)),

                
                Game(bel, tun, datetime(2018, 6, 23, 12, 0)),
                
                Game(eng, pan, datetime(2018, 6, 24, 12, 0)),
                
                Game(eng, bel, datetime(2018, 6, 28, 18, 0)),
                Game(pan, tun, datetime(2018, 6, 28, 18, 0)),
                ]),
                
    h=Group(teams = [pol, sen, col, jap],

            games = [
                Game(col, jap, datetime(2018, 6, 19, 12, 0)),
                Game(pol, sen, datetime(2018, 6, 19, 15, 0)),

                
                Game(jap, sen, datetime(2018, 6, 24, 15, 0)),
                Game(pol, col, datetime(2018, 6, 24, 18, 0)),
                
                Game(jap, pol, datetime(2018, 6, 28, 14, 0)),
                Game(sen, col, datetime(2018, 6, 28, 14, 0)),
                ]))

# group winners and seconds
winners = {}
seconds = {}
for group in 'abcdefgh':

    winners[group] = group.winner()
    seconds[group] = group.second()



    

# notes?
groups['a'].notes = [
j    """ Group A

    Russia
 
    Uruguay

    Egypt

    Saudi Arabia
    """
    ]

# do something ?

# print out the games
for xx, group  in groups.items():
    
    print(xx)
    
    for game in group.games:
        print(game.a, game.b, game.when)
        
    print()

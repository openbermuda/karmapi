from collections import defaultdict

from .place import Place


squadsize = 23
n = 32

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


class NorthPole(Place):
    """  Where teams go when out? """

    name = 'North Pole'
    lat = 90
    lon = 0

    
class Player:
    """ A player of class

    Tony Currie, Kyle Walker, Harry Maguire
    """

    def __init__(self, number):

        self.goals = []
        self.red = []
        self.yellow = []
        self.number = number


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


    

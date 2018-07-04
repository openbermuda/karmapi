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
        return key.points, key.goals - key.against, key.goals, -1 * key.yellow
        
            

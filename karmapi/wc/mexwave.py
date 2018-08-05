
from collections import defaultdict
from datetime import datetime, timedelta
import csv

import curio



from karmapi import pigfarm, beanstalk

# add a PI Gui?
class MexicanWaves(pigfarm.Yard):

    def __init__(self, parent, jsf=None, venues=None,
                 back_image=None,
                 dump=None, events=None):
        """ Initialise the thing """

        super().__init__(parent)

        self.jsf = jsf
        self.jsf.dump = dump
        self.back_image = back_image

        if events:
            events = list(parse_events(events))
        
        self.jsf.game_events = events

        self.messages = []

        self.start_time = datetime.utcnow()

        # teleprinter location
        self.teleprint_xxyy = .85, .425
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
        self.jsf.timewarp *= 2

    async def faster(self):
        """ Go through time more quickly  """
        self.jsf.timewarp /= 2

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

        for place in self.places:
            size = 5
            self.ball(place, fill='red', size=5)

            self.message(place.name, place, yoff=-20, fill='yellow')
            
        locations = defaultdict(list)
        
        for team in self.jsf.generate_teams():

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

        elapsed = (datetime.utcnow() - self.start_time).total_seconds()

        return self.jsf.iwarp(elapsed)

        
    def draw(self):

        import time
        self.beanstalk.create_time = time.time()

        self.beanstalk.draw(self.canvas, self.width, self.height, 'red')

    async def reset(self):
        """ Reset timer """
        self.start_time = datetime.utcnow()

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

        for msg, fill, card in self.teleprints:
            
            self.message(msg=msg, fill=fill, card=card, xx=xx, yy=yy)
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


    def teleprint(self, msg=None, fill='orange', card=None, **kwargs):
        """ teleprinter messages """
        self.teleprints.append((msg, fill, card))

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


    def message(self, msg=None, where=None, fill='red',
                card=False, 
                size=5, xoff=0, yoff=0,
                xx=None, yy=None, **kwargs):
        """ Message from a place """

        xx, yy = self.layout(where, xx, yy)

        self.canvas.create_text((xx + xoff, yy + yoff), text=msg, fill=fill)

        if card:
            #print("CARD", card, msg)
            x = xx + xoff - 150
            y = yy + yoff
            self.canvas.create_rectangle(x, y, x + 10, y + 10, fill=card)


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

            elif ascore == bscore:
                apen, bpen = game.pens_score()
                ascore += apen / 10
                bscore += bpen / 10
            
            self.message(msg="{} {} {}  {}".format(
                aa, ascore, bscore, bb),
                xx=xx, yy=yy, fill='green')

            px = xx - 0.01
            dx = -0.005
            
            for pens in game.apen, game.bpen:
                for pix, pen in enumerate(pens):
                    if pen.score:
                        rog = 'green'
                    else:
                        rog = 'red'

                    xp = px + (pix * dx)
                    self.ball(xx=xp, yy=yy + 0.025, fill=rog, size=3)
                    
                px = xx + 0.01
                dx *= -1
            
            yy += 0.05

            if ix in [7, 11, 13]:
                xx += .1
                yy = .6
                yinc *= 2

        final = self.jsf.knockout[-2]
        if final.ascore != None:
            xx += 0.1
            yy = 0.6
            self.message(msg="{}".format(
                final.winner().name),
                xx=xx, yy=yy,
                fill='gold')
            


    def ball(self, place=None, fill='red', size=5, xoff=0, yoff=0,
             xx=None, yy=None, **kwargs):
        """ Draw a filled circle at place """

        xx, yy = self.layout(place, xx, yy)

        self.canvas.create_oval(
            xx+xoff-size,
            yy+yoff-size,
            xx+xoff+size, yy+yoff+size, fill=fill)

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

            if self.back_image:
                image = self.find_image(self.back_image)
                if image:
                    image = self.load_image(image)

                    image = image.resize((int(self.height), int(self.width)))

                    self.beanstalk.image = image

            self.draw()

            # step balls
            await self.step_balls()

            #self.jsf.now = self.when()

            # wait for event here.  We want to repaint in a minute game time
            await curio.sleep(self.sleep)            


def parse_events(events, out=None):

    if out:
        out = csv.writer(out)
    
    for ix, row in enumerate(csv.reader(events)):

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

        kotime = datetime(year, month, day, hour, 0)
        when = kotime + timedelta(minutes=minute)

        yield kotime, when, a.lower().strip(), b.lower().strip(), what, extras
            

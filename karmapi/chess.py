"""
Queen Mary Chess
================

Normal chess rules except:

The goal is to make the chessboard a fascinating world for all that inhabit it.

Two players, working together to build trust.

Nobody gets hurt.

Unless perhaps two pawns are turned into six queens.

Build trust by exposing pieces. 

If a piece is exposed, move closer to have a better conversation.

The goal, is to communicate to each other through your moves.  

Perhaps, add a message to your move, to indicate the message you wish to send.

Scoring positions
=================

No king must be in check mate.   Zero value position.

Value pieces as follows:

Pawn:   1
Knight: 3
Bishop: 3
Rook:   5
Queen:  9

Base score for a position is the total value of the pieces on the board.

So, for example, promoting a pawn to a queen raises the base value by 8.

Complex Score
-------------

Base score plus:

1: for every way that something can be taken by the player whose turn it is.

1: for every way something can be taken by the person whose turn it is not.

(ie just 1 point for every possible way a piece can currently be taken).

For Queen, Bishop and Rook:

Add 6 - n, where n is the number of squares between the piece and the
piece it can take.

(ie the closer the two things are the higher the score.)

Pawn Promotion
--------------

Up to two pawns of each colour can be promoted to Riders

Up to two pawns of each colour can be promoted to Wizards

Up to two pawns of each colour can be promoted to Magic Castles

Pawns cannot be promoted to queens.

**Note these rules mean two chess sets are more than enough to play a game.**

Variations
..........

Up to two pawns can also become queens.

Alternate names
---------------

queen

rook, tent, magic castle 

bishop, wizard

knight, farmer, architect, rider

pawn, guide, nurse, helper, builder, messenger

River Dell
----------

Play with two boards, one rotated 180 degrees.  So each player is
playing both boards in effect.

Goal is to maximise *karma* over time. 

When a pawn is lost, three other pawns become passed.  They are on a
course to becoming wiards, riders or magic castles.

Off the board is River Dell.  It's where heros retire to tell their
tales and dream of lands far away.

Story
-----

One challenge is making sure you do not put your partner in check
mate.  If that happens it is game over, with a zero value game.

Players also have to be careful not to avoid giving each other no
choice but one has to put the other in check.

A stalemate arises when the same move, same position, has been
repeated three times.  Game over, tally up how well you did together.

If you play nicely, it might be possible to turn 12 pawns into 12 new
pieces, at a sacrifice of just four pawns, two for each side.


Six guides, pairs from the kingdoms
All dream of becoming a wizards
Four can have their dreams
Two may perish in the quest

Six messengers, pairs from the kingdoms
All dream of riding through the lands
Four can have their dreams
Two may perish in the quest.

Six builders, pairs in tents.
All dream of magic castles in the air
Four can have their dreams
Two must perish in the quest.

Together they can build a magic world
Eight castles in the sky
Eight riders of the land
Eight wizards shaping good

"""
from math import pi, e, sin, cos

from karmapi import pigfarm

from karmapi.mclock2 import GuidoClock

class RiverDell(pigfarm.PillBox):

    def __init__(self, parent):

        super().__init__(parent)

        self.lands = [Land()]


    async def start(self):

        for land in self.lands:
            land.plot(self)

    async def run(self):

        pass


class Nothing:

    def __init__(self):

        self.value = 0

    def colour(self, scale=pi*pi*e*e, flip=False):

        value = self.value
        rgb = 255, 0, 0

        if flip:
            rgb = rgb[::-1]

        return (int(c * value / scale) for c in rgb)
        

class Pawn(Nothing):

    def __init__(self):

        self.value = sin(pi/2)

class Rider(Pawn):

    def __init__(self):

        self.value = e

class Wizard(Pawn):

    def __init__(self):

        self.value = pi

class MagicCastle(Pawn):

    def __init__(self):

        self.value = sin(pi/4) * pi * e

class Queen(Pawn):

    def __init__(self):

        self.value = pi * e

class King(Pawn):

    def __init__(self):

        self.value = 0 + 1j

class Plot:
    def __init__(self):

        self.value = sin(pi/2)
        self.pawn = Nothing()

    def colour(self, scale=pi*pi*e*e):

        value = self.value
        
        rgb = 0, 255, 0

        return (int(c * value / scale) for c in rgb)
    
def value(world):

    value = 0
    for pawn in world:
        value += pawn.value

    return value

class Land:
    """ A magic land where it all happens """

    def __init__(self):

        self.grid = {}
        for x in range(8):
            for y in range(8):
                plot = Plot()

                plot.shade = (x + y) % 2
                self.grid[(x, y)] = plot

    def walk(self):
        """ Walk through the plots """
        for x in range(8):
            for y in range(8):
                plot = self.grid[(x, y)]
                yield x, y, plot


    def plot(self, image):
        """ Draw an image of the land 
        
        Use the plots as a background, the pawns in the foreground.

        With alpha blending the two.

        """

        land = []
        pawns = []
        for x, y, plot in self.walk():

            colour = plot.colour()
            land.append(colour)

            colour = plot.pawn.colour()
            pawns.append(colour)

        # draw the grids
        image.grid(land, alpha=0.5)
        image.grid(pawns, alpha=0.5)

    def piece_colour(self, value, scale=pi*pi*e*e):

        rgb = 255, 0, 0

        return (int(c * value / scale) for c in rgb)
    
    def shades(self):
        pass

    def values(self):

        data = []
        for x in range(8):
            row = []
            data.append(row)
            for y in range(8):
                plot = self.grid[(x, y)]

                value = plot.value

                if plot.pawn is not None:
                    value += plot.pawn.value
                    
                row.append(value)
                
        return data

    def score(self):

        pass

    
def main():

    farm = pigfarm.PigFarm()

    farm.add(GuidoClock)
    
    farm.add(RiverDell)

    pigfarm.run(farm)


    
if __name__ == '__main__':

    main()

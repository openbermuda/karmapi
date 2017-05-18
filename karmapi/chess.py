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

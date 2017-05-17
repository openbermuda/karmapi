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



"""

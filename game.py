
"""This includes some business logic for a chess board program.

Moves are here represented in the UCI move format. For example like:
"e2e4", "e7e5", "e1g1" (white short castling), "e7e8q" (for promotion),
"c5b6" (en passant).

Positions on the chess board are represented as for example "a1", "b5".

Pieces are represented as:

"P": white pawn   -  "p": black pawn
"N": white knight -  "n": black knight
"B": white biship -  "b": black bishop
"R": white rook   -  "r": black rook
"Q": white queen  -  "q": black queen
"K": white king   -  "k": black king
"""

import engine

class Game:

    def __init__(self, FEN_string):
        pass
        
        
    def board_value(square):
        """Return "k", "K", "p" etc f there is a piece on the square,
        and None if there is no piece. Square can be "a1", "b5" etc.
        """

    def legal_move(self, move):
        """Return"""
        
    def make_move(UCI_format_move):
        pass

def FEN_string(FEN_string, UCI_format_move):
    """Return a FEN string for the game state that result after making
    the given move to the given position."""

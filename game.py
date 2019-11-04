"""This includes some business logic for a chess board program.

Moves are here represented in the UCI move format. For example like:
"e2e4", "e7e5", "e1g1" (white short castling), "e7e8q" (for promotion),
"c5b6" (en passant).

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
        self.FEN_string = FEN_string
        self.legal_moves = engine.legal_moves_UCI(FEN_string)
        self.FEN_string_history = []

        # The board is represented as a list of rows.
        self.board = []


    def legal(self, UCI_format_move):
        """Return true iff the move is legal"""
        return UCI_format_move in self.legal_moves

    def make_move(self, UCI_format_move):
        pass

    def computer_move(self):
        """Return a move computed by the engine."""
        return computer_move_UCI(self.FEN_string)

    def check(self):
        return engine.check(self.FEN_string)

    def check_mate(self):
        return engine.check_mate(self.FEN_string)

    def stale_mate():
        return engine.stale_mate(self.FEN_string)

    def insufficient_material(self):
        """Return true if and only if the position is king vs king or
        king vs king and light piece."""
        FEN_fields = self.FEN_string.split(" ")
        board = FEN_fields[0]
        pieces = ""
        for c in board:
            if c in "pnbrqkPNBRQK":
                pieces += c
        if len(pieces) > 3:
            return False
        for c in "prqPRQ":
            if c in pieces:
                return False
        return True

    def draw_by_repetition(self):
        pass

    def draw_by_50_move_rule(self):
        pass

    def undo_move(self):
        """Move back in move history."""
        pass

    def redo_move(self):
        """Move forward in move history."""
        pass


def make_move(FEN_string, UCI_format_move):
    """Return a FEN string for the game state that result after making
    the given move to the given position."""




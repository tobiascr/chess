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
        self.FEN_string_history = []
        self.legal_moves = engine.legal_moves_UCI(FEN_string)
        self.board = Board(FEN_string)

    def __str__(self):
        """Make it possible to use the print the board by using the print command."""
        return self.board.__str__()

    def board_value(self, position):
        """Return values like "K", "k", "N" etc if there is a piece at the given
        position and None if there is none. The position is given as "a1", "b5" etc.
        """
        return self.board.value(position)

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


class Board:
    """Instances of this class describes how the pieces are placed on the board."""

    def __init__(self, FEN_string):
        # The board is represented as a list of rows, where each row is a list.
        # The entries in that list are None if there is no piece at the position
        # and for example "K", "k", "R" etc if there is. The position a1 correspond
        # to the first entry in the 8'th row.
        self.rows = [[None for i in range(8)] for i in range(8)]

        # Decode the FEN_string
        FEN_fields = FEN_string.split(" ")
        FEN_rows = FEN_fields[0].split("/")
        FEN_rows.reverse()
        for row in range(8):
            col = 0
            for char in FEN_rows[row]:
                if char in "12345678":
                    col += int(char)
                else:
                    self.rows[row][col] = char
                    col += 1

    def __str__(self):
        """Make it possible to use the print the board by using the print command."""
        def row(i):
            result = ""
            for value in self.rows[i]:
                if value == None:
                    result += " "
                else:
                    result += value
            return result
        return "   +" + "---+"*8 + "\n" + "\n".join([" " + str(8-i) +
               " | " + " | ".join(row(7-i)) + " |" + "\n   +" + "---+"*8
               for i in range(8)]) + "\n     a   b   c   d   e   f   g   h"

    def value(self, position):
        """Return values like "K", "k", "N" etc if there is a piece at the given
        position and None if there is none. The position is given as "a1", "b5" etc.
        """
        col = "abcdefgh".find(position[0]) 
        row = (int(position[1]) - 1)
        return self.rows[row][col]

    def make_move(self, UCI_format_move):
        pass




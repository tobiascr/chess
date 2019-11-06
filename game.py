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
    """It is intended that this class should function as an interface for the engine
    and everything else in this module.
    """
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
        return self.board.get_value(position)

    def legal(self, UCI_format_move):
        """Return true iff the move is legal"""
        return UCI_format_move in self.legal_moves

    def make_move(self, UCI_format_move):
        from_position = UCI_format_move[0:2]
        to_position = UCI_format_move[2:4]
        piece_moved = self.board.get_value(from_position)
        non_en_passant_capture = self.board.get_value(to_position) != None

        # Update the board.
        self.board.make_move(UCI_format_move)

        # Add the current FEN string to history.
        self.FEN_string_history.append(self.FEN_string)

        # Update the FEN string.
        FEN_fields = self.FEN_string.split(" ")
        self.FEN_string = self.board.FEN_string_first_part()

        if FEN_fields[1] == "w":
            self.FEN_string += " b "
            black_made_last_move = False
        else:
            self.FEN_string += " w "
            black_made_last_move = True

        castling_availability = FEN_fields[2]

        # If white castling.
        if UCI_format_move == "e1c1" or UCI_format_move == "e1g1":
            castling_availability = castling_availability.replace("K","")
            castling_availability = castling_availability.replace("Q","")
        # If black castling.
        elif UCI_format_move == "e8c8" or UCI_format_move == "e8g8":
            castling_availability = castling_availability.replace("k","")
            castling_availability = castling_availability.replace("q","")
        else:
            if "K" in castling_availability:
                if from_position == "e1" or from_position == "h1" or to_position == "h1":
                    castling_availability = castling_availability.replace("K","")
            if "Q" in castling_availability:
                if from_position == "e1" or from_position == "a1" or to_position == "a1":
                    castling_availability = castling_availability.replace("Q","")
            if "k" in castling_availability:
                if from_position == "e8" or from_position == "h8" or to_position == "h8":
                    castling_availability = castling_availability.replace("k","")
            if "q" in castling_availability:
                if from_position == "e8" or from_position == "a8" or to_position == "a8":
                    castling_availability = castling_availability.replace("q","")

        if castling_availability == "":
            castling_availability = "-"
        self.FEN_string += castling_availability + " "

        # En passant.
        en_passant_target_square = "-"
        if piece_moved == "P":
            if UCI_format_move[1] == "2" and UCI_format_move[3] == "4":
                print("hi")
                en_passant_target_square = UCI_format_move[0] + "3"
        if piece_moved == "p":
            if UCI_format_move[1] == "7" and UCI_format_move[3] == "5":
                en_passant_target_square = UCI_format_move[0] + "6"
        self.FEN_string += en_passant_target_square + " "

        # Half move clock. This is the number of halfmoves since the last
        # capture or pawn advance.
        if len(FEN_fields) <= 4:
            half_move_clock = 0
        else:
            half_move_clock = int(FEN_fields[4])

        if piece_moved == "P" or piece_moved == "p" or non_en_passant_capture:
            half_move_clock = 0
        else:
            half_move_clock += 1

        self.FEN_string += str(half_move_clock) + " "

        # Full move number.
        if len(FEN_fields) <= 5:
            full_move_number = 1
        else:
            full_move_number = int(FEN_fields[5])

        if black_made_last_move:
            full_move_number += 1

        self.FEN_string += str(full_move_number)


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

    def get_value(self, position):
        """Return values like "K", "k", "N" etc if there is a piece at the given
        position and None if there is none. The position is given as "a1", "b5" etc.
        """
        col = "abcdefgh".find(position[0]) 
        row = (int(position[1]) - 1)
        return self.rows[row][col]

    def set_value(self, position, value):
        """The position is given as "a1", "b5" etc. Value can be K", "n", None etc."""
        col = "abcdefgh".find(position[0]) 
        row = (int(position[1]) - 1)
        self.rows[row][col] = value

    def make_move(self, UCI_format_move):

        # Promotions
        if len(UCI_format_move) == 5:
            from_position = UCI_format_move[0:2]
            to_position = UCI_format_move[2:4]
            to_piece = UCI_format_move[4]
            # Convert to_piece to upper case if the player is white.
            if self.get_value(from_position) == "P":
                    to_piece = to_piece.upper()
            self.set_value(from_position, None)
            self.set_value(to_position, to_piece)
            return

        # Castlings
        if UCI_format_move == "e1c1":
            self.set_value("a1", None)
            self.set_value("b1", None)
            self.set_value("c1", "K")
            self.set_value("d1", "R")
            self.set_value("e1", None)
            return
        if UCI_format_move == "e1g1":
            self.set_value("e1", None)
            self.set_value("f1", "R")
            self.set_value("g1", "K")
            self.set_value("h1", None)
            return
        if UCI_format_move == "e8c8":
            self.set_value("a8", None)
            self.set_value("b8", None)
            self.set_value("c8", "k")
            self.set_value("d8", "r")
            self.set_value("e8", None)
            return
        if UCI_format_move == "e8g8":
            self.set_value("e8", None)
            self.set_value("f8", "r")
            self.set_value("g8", "k")
            self.set_value("h8", None)
            return

        # En passants
        from_position = UCI_format_move[0:2]
        piece = self.get_value(from_position)
        if piece == "P" or piece == "p":
            to_position = UCI_format_move[2:4]
            if from_position[0] != to_position[0]:
                if self.get_value(to_position) == None:
                    capture_position = to_position[0] + from_position[1]
                    self.set_value(from_position, None)
                    self.set_value(to_position, piece)
                    self.set_value(capture_position, None)
                    return

        # Ordinary moves
        from_position = UCI_format_move[0:2]
        to_position = UCI_format_move[2:4]
        piece = self.get_value(from_position)
        self.set_value(from_position, None)
        self.set_value(to_position, piece)

    def FEN_string_first_part(self):
        """Use the data in this class to produce the first part of a FEN string
        that describe the placement of the pieces."""
        def convert_to_FEN_row(row):
            FEN_row = ""
            empty_position_count = 0
            for value in row:
                if value == None:
                    empty_position_count += 1
                else:
                    if empty_position_count > 0:
                        FEN_row += str(empty_position_count)
                        empty_position_count = 0
                    FEN_row += value
            if empty_position_count > 0:
                FEN_row += str(empty_position_count)
            return FEN_row

        return "/".join([convert_to_FEN_row(self.rows[i]) for i in range(7,-1,-1)])







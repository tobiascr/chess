
"""Positions are represented as integers from 0 to 63. 0 represent a1,
1 represent b1, 8 represent a2 etc.
"""

import random


class Move:
    """Instances of Move describes changes to a game state. They can be used both for
    making the changes and for undoing them."""

    def __init__(self):
        self.change_list = []
        self.en_passant_target_square = None

    def __str__(self):
        """Make it possible to use the print command on objects of this class."""
        lines = []
        for change in self.change_list:
            line = convert_position_to_conventional_format(change[0]) + " "
            if change[1]:
                line += change[1].name + " "
            else:
                line += "- "
            if change[2]:
                line += change[2].name
            else:
                line += "-"
            lines.append(line)
        return ", ".join(lines)

    def add_change(self, position, value_before_change, value_after_change):
        """The values can be piece-objects or None."""
        self.change_list.append((position, value_before_change, value_after_change))


class King:

    def __init__(self, white):
        self.has_moved = False
        self.white = white
        if white:
            self.name = "K"
            self.value = 1000
        else:
            self.name = "k"
            self.value = -1000
        self.possible_moves_dict = {
                 0: [1, 8, 9],
                 1: [0, 2, 8, 9, 10],
                 2: [1, 3, 9, 10, 11],
                 3: [2, 4, 10, 11, 12],
                 4: [3, 5, 11, 12, 13],
                 5: [4, 6, 12, 13, 14],
                 6: [5, 7, 13, 14, 15],
                 7: [6, 14, 15],
                 8: [0, 1, 9, 16, 17],
                 9: [0, 1, 2, 8, 10, 16, 17, 18],
                 10: [1, 2, 3, 9, 11, 17, 18, 19],
                 11: [2, 3, 4, 10, 12, 18, 19, 20],
                 12: [3, 4, 5, 11, 13, 19, 20, 21],
                 13: [4, 5, 6, 12, 14, 20, 21, 22],
                 14: [5, 6, 7, 13, 15, 21, 22, 23],
                 15: [6, 7, 14, 22, 23],
                 16: [8, 9, 17, 24, 25],
                 17: [8, 9, 10, 16, 18, 24, 25, 26],
                 18: [9, 10, 11, 17, 19, 25, 26, 27],
                 19: [10, 11, 12, 18, 20, 26, 27, 28],
                 20: [11, 12, 13, 19, 21, 27, 28, 29],
                 21: [12, 13, 14, 20, 22, 28, 29, 30],
                 22: [13, 14, 15, 21, 23, 29, 30, 31],
                 23: [14, 15, 22, 30, 31],
                 24: [16, 17, 25, 32, 33],
                 25: [16, 17, 18, 24, 26, 32, 33, 34],
                 26: [17, 18, 19, 25, 27, 33, 34, 35],
                 27: [18, 19, 20, 26, 28, 34, 35, 36],
                 28: [19, 20, 21, 27, 29, 35, 36, 37],
                 29: [20, 21, 22, 28, 30, 36, 37, 38],
                 30: [21, 22, 23, 29, 31, 37, 38, 39],
                 31: [22, 23, 30, 38, 39],
                 32: [24, 25, 33, 40, 41],
                 33: [24, 25, 26, 32, 34, 40, 41, 42],
                 34: [25, 26, 27, 33, 35, 41, 42, 43],
                 35: [26, 27, 28, 34, 36, 42, 43, 44],
                 36: [27, 28, 29, 35, 37, 43, 44, 45],
                 37: [28, 29, 30, 36, 38, 44, 45, 46],
                 38: [29, 30, 31, 37, 39, 45, 46, 47],
                 39: [30, 31, 38, 46, 47],
                 40: [32, 33, 41, 48, 49],
                 41: [32, 33, 34, 40, 42, 48, 49, 50],
                 42: [33, 34, 35, 41, 43, 49, 50, 51],
                 43: [34, 35, 36, 42, 44, 50, 51, 52],
                 44: [35, 36, 37, 43, 45, 51, 52, 53],
                 45: [36, 37, 38, 44, 46, 52, 53, 54],
                 46: [37, 38, 39, 45, 47, 53, 54, 55],
                 47: [38, 39, 46, 54, 55],
                 48: [40, 41, 49, 56, 57],
                 49: [40, 41, 42, 48, 50, 56, 57, 58],
                 50: [41, 42, 43, 49, 51, 57, 58, 59],
                 51: [42, 43, 44, 50, 52, 58, 59, 60],
                 52: [43, 44, 45, 51, 53, 59, 60, 61],
                 53: [44, 45, 46, 52, 54, 60, 61, 62],
                 54: [45, 46, 47, 53, 55, 61, 62, 63],
                 55: [46, 47, 54, 62, 63],
                 56: [48, 49, 57],
                 57: [48, 49, 50, 56, 58],
                 58: [49, 50, 51, 57, 59],
                 59: [50, 51, 52, 58, 60],
                 60: [51, 52, 53, 59, 61],
                 61: [52, 53, 54, 60, 62],
                 62: [53, 54, 55, 61, 63],
                 63: [54, 55, 62]}

    def possible_moves(self, game_state, from_position):
        """Return all moves except from castlings that this king can make if it's
        located at from_position, including putting itself into check and capturing the
        opponents king.
        """
        move_list = []
        for to_position in self.possible_moves_dict[from_position]:
            piece = game_state.board[to_position]
            if piece:

                # If there is an opposite color piece on the target square.
                if piece.white != self.white:
                    move = Move()
                    move.add_change(from_position, self, None)
                    move.add_change(to_position, piece, self)
                    move_list.append(move)

            # If the is no piece on the target square.
            else:
                move = Move()
                move.add_change(from_position, self, None)
                move.add_change(to_position, None, self)
                move_list.append(move)

        return move_list


class Queen:

    def __init__(self, white):
        self.white = white
        if white:
            self.name = "Q"
            self.value = 9
        else:
            self.name = "q"
            self.value = -9

    def possible_moves(self, game_state, from_position):
        """Return all positions that this piece can move to if it's located at from_position."""
        return Rook.possible_moves(self, game_state, from_position) + Bishop.possible_moves(
               self, game_state, from_position)


class Rook:

    def __init__(self, white):
        self.has_moved = False
        self.white = white
        if white:
            self.name = "R"
            self.value = 5
        else:
            self.name = "r"
            self.value = -5

    def possible_moves(self, game_state, from_position):
        """Return all positions except for positions reached by castlings
        that this piece can move to if it's located at from_position."""
        move_list = []

        # Moves up.
        for to_position in range(from_position + 8, 64, 8):
            piece = game_state.board[to_position]
            if piece:
                # If capture.
                if piece.white != self.white:
                    move = Move()
                    move.add_change(from_position, self, None)
                    move.add_change(to_position, piece, self)
                    move_list.append(move)
                break
            else:
                move = Move()
                move.add_change(from_position, self, None)
                move.add_change(to_position, None, self)
                move_list.append(move)

        # Moves down.
        for to_position in range(from_position - 8, -1, -8):
            piece = game_state.board[to_position]
            if piece:
                # If capture.
                if piece.white != self.white:
                    move = Move()
                    move.add_change(from_position, self, None)
                    move.add_change(to_position, piece, self)
                    move_list.append(move)
                break
            else:
                move = Move()
                move.add_change(from_position, self, None)
                move.add_change(to_position, None, self)
                move_list.append(move)

        # Moves right.
        for to_position in range(from_position + 1, from_position - from_position % 8 + 8, 1):
            piece = game_state.board[to_position]
            if piece:
                # If capture.
                if piece.white != self.white:
                    move = Move()
                    move.add_change(from_position, self, None)
                    move.add_change(to_position, piece, self)
                    move_list.append(move)
                break
            else:
                move = Move()
                move.add_change(from_position, self, None)
                move.add_change(to_position, None, self)
                move_list.append(move)

        # Moves left.
        for to_position in range(from_position - 1, from_position - from_position % 8 - 1, -1):
            piece = game_state.board[to_position]
            if piece:
                # If capture.
                if piece.white != self.white:
                    move = Move()
                    move.add_change(from_position, self, None)
                    move.add_change(to_position, piece, self)
                    move_list.append(move)
                break
            else:
                move = Move()
                move.add_change(from_position, self, None)
                move.add_change(to_position, None, self)
                move_list.append(move)

        return move_list


class Bishop:

    def __init__(self, white):
        self.white = white
        if white:
            self.name = "B"
            self.value = 3
        else:
            self.name = "b"
            self.value = -3

    def possible_moves(self, game_state, from_position):
        """Return all positions that this piece can move to if it's located at from_position"""
        # Row and column for the position.
        [from_r, from_c] = [from_position // 8, from_position % 8]
        move_list = []

        # Moves up right.
        r = from_r + 1
        c = from_c + 1
        while r < 8 and c < 8:
            to_position = r * 8 + c
            piece = game_state.board[to_position]
            if piece:
                # If capture.
                if piece.white != self.white:
                    move = Move()
                    move.add_change(from_position, self, None)
                    move.add_change(to_position, piece, self)
                    move_list.append(move)
                break
            else:
                move = Move()
                move.add_change(from_position, self, None)
                move.add_change(to_position, None, self)
                move_list.append(move)
            c += 1
            r += 1

        # Moves up left.
        r = from_r + 1
        c = from_c - 1
        while r < 8 and c >= 0:
            to_position = r * 8 + c
            piece = game_state.board[to_position]
            if piece:
                # If capture.
                if piece.white != self.white:
                    move = Move()
                    move.add_change(from_position, self, None)
                    move.add_change(to_position, piece, self)
                    move_list.append(move)
                break
            else:
                move = Move()
                move.add_change(from_position, self, None)
                move.add_change(to_position, None, self)
                move_list.append(move)
            c -= 1
            r += 1

        # Moves down right.
        r = from_r - 1
        c = from_c + 1
        while r >= 0 and c < 8:
            to_position = r * 8 + c
            piece = game_state.board[to_position]
            if piece:
                # If capture.
                if piece.white != self.white:
                    move = Move()
                    move.add_change(from_position, self, None)
                    move.add_change(to_position, piece, self)
                    move_list.append(move)
                break
            else:
                move = Move()
                move.add_change(from_position, self, None)
                move.add_change(to_position, None, self)
                move_list.append(move)
            c += 1
            r -= 1

        # Moves down left.
        r = from_r - 1
        c = from_c - 1
        while r >= 0 and c >= 0:
            to_position = r * 8 + c
            piece = game_state.board[to_position]
            if piece:
                # If capture.
                if piece.white != self.white:
                    move = Move()
                    move.add_change(from_position, self, None)
                    move.add_change(to_position, piece, self)
                    move_list.append(move)
                break
            else:
                move = Move()
                move.add_change(from_position, self, None)
                move.add_change(to_position, None, self)
                move_list.append(move)
            c -= 1
            r -= 1

        return move_list


class Knight:

    def __init__(self, white):
        self.white = white
        if white:
            self.name = "N"
            self.value = 3
        else:
            self.name = "n"
            self.value = -3
        self.possible_moves_dict = { 
                 0: [17, 10],
                 1: [16, 18, 11],
                 2: [17, 19, 12, 8],
                 3: [18, 20, 13, 9],
                 4: [19, 21, 14, 10],
                 5: [20, 22, 15, 11],
                 6: [21, 23, 12],
                 7: [22, 13],
                 8: [25, 18, 2],
                 9: [24, 26, 19, 3],
                 10: [25, 27, 20, 4, 0, 16],
                 11: [26, 28, 21, 5, 1, 17],
                 12: [27, 29, 22, 6, 2, 18],
                 13: [28, 30, 23, 7, 3, 19],
                 14: [29, 31, 4, 20],
                 15: [30, 5, 21],
                 16: [33, 26, 10, 1],
                 17: [32, 34, 27, 11, 2, 0],
                 18: [33, 35, 28, 12, 3, 1, 8, 24],
                 19: [34, 36, 29, 13, 4, 2, 9, 25],
                 20: [35, 37, 30, 14, 5, 3, 10, 26],
                 21: [36, 38, 31, 15, 6, 4, 11, 27],
                 22: [37, 39, 7, 5, 12, 28],
                 23: [38, 6, 13, 29],
                 24: [41, 34, 18, 9],
                 25: [40, 42, 35, 19, 10, 8],
                 26: [41, 43, 36, 20, 11, 9, 16, 32],
                 27: [42, 44, 37, 21, 12, 10, 17, 33],
                 28: [43, 45, 38, 22, 13, 11, 18, 34],
                 29: [44, 46, 39, 23, 14, 12, 19, 35],
                 30: [45, 47, 15, 13, 20, 36],
                 31: [46, 14, 21, 37],
                 32: [49, 42, 26, 17],
                 33: [48, 50, 43, 27, 18, 16],
                 34: [49, 51, 44, 28, 19, 17, 24, 40],
                 35: [50, 52, 45, 29, 20, 18, 25, 41],
                 36: [51, 53, 46, 30, 21, 19, 26, 42],
                 37: [52, 54, 47, 31, 22, 20, 27, 43],
                 38: [53, 55, 23, 21, 28, 44],
                 39: [54, 22, 29, 45],
                 40: [57, 50, 34, 25],
                 41: [56, 58, 51, 35, 26, 24],
                 42: [57, 59, 52, 36, 27, 25, 32, 48],
                 43: [58, 60, 53, 37, 28, 26, 33, 49],
                 44: [59, 61, 54, 38, 29, 27, 34, 50],
                 45: [60, 62, 55, 39, 30, 28, 35, 51],
                 46: [61, 63, 31, 29, 36, 52],
                 47: [62, 30, 37, 53],
                 48: [58, 42, 33],
                 49: [59, 43, 34, 32],
                 50: [60, 44, 35, 33, 40, 56],
                 51: [61, 45, 36, 34, 41, 57],
                 52: [62, 46, 37, 35, 42, 58],
                 53: [63, 47, 38, 36, 43, 59],
                 54: [39, 37, 44, 60],
                 55: [38, 45, 61],
                 56: [50, 41],
                 57: [51, 42, 40],
                 58: [52, 43, 41, 48],
                 59: [53, 44, 42, 49],
                 60: [54, 45, 43, 50],
                 61: [55, 46, 44, 51],
                 62: [47, 45, 52],
                 63: [46, 53]}

    def possible_moves(self, game_state, from_position):
        """Return all positions that this piece can move to if it's located at from_position."""
        move_list = []
        for to_position in self.possible_moves_dict[from_position]:
            piece = game_state.board[to_position]
            if piece:

                # If there is an opposite color piece on the target square.
                if piece.white != self.white:
                    move = Move()
                    move.add_change(from_position, self, None)
                    move.add_change(to_position, piece, self)
                    move_list.append(move)

            # If the is no piece on the target square.
            else:
                move = Move()
                move.add_change(from_position, self, None)
                move.add_change(to_position, None, self)
                move_list.append(move)

        return move_list


class Pawn:

    def __init__(self, white): 
        self.white = white
        if white:
            self.name = "P"
            self.value = 1
        else:
            self.name = "p"
            self.value = -1

        # The position can later be changed to the last rank position of the particular
        # pawn.
        self.queen_to_promote = Queen(white)

    def possible_moves(self, game_state, from_position):
        """Return all positions that this piece can move to if it's located at from_position."""
        move_list = []
        [from_row, from_col] = [from_position // 8, from_position % 8]

        if self.white:
            if from_row == 1:
                # Non capture moves one step.
                if game_state.board[from_position + 8] == None:
                    move = Move()
                    move.add_change(from_position, self, None)
                    move.add_change(from_position + 8, None, self)
                    move_list.append(move)

                    # Non capture move two steps.
                    if game_state.board[from_position + 16] == None:
                        move = Move()
                        move.add_change(from_position, self, None)
                        move.add_change(from_position + 16, None, self)
                        # This move triggers en passant possibility.
                        move.en_passant_target_square = from_position + 8
                        move_list.append(move)

            if from_row < 6:
                # Queenside capture.
                if from_col > 0:
                    to_position = from_position + 7
                    piece = game_state.board[to_position]
                    if piece:
                        if piece.white != self.white:
                            move = Move()
                            move.add_change(from_position, self, None)
                            move.add_change(to_position, piece, self)
                            move_list.append(move)
                    # En passant.
                    if from_row == 4:
                        if to_position == game_state.en_passant_target_square:
                            move = Move()
                            move.add_change(from_position, self, None)
                            move.add_change(to_position, None, self)
                            move.add_change(from_position - 1, 
                                            game_state.board[from_position - 1], None)
                            move_list.append(move)

                # Kingside capture.
                if from_col < 7:
                    to_position = from_position + 9
                    piece = game_state.board[to_position]
                    if piece:
                        if piece.white != self.white:
                            move = Move()
                            move.add_change(from_position, self, None)
                            move.add_change(to_position, piece, self)
                            move_list.append(move)
                    # En passant.
                    if from_row == 4:
                        if to_position == game_state.en_passant_target_square:
                            move = Move()
                            move.add_change(from_position, self, None)
                            move.add_change(to_position, None, self)
                            move.add_change(from_position + 1,
                                            game_state.board[from_position + 1], None)
                            move_list.append(move)

            if 1 < from_row < 6:
                # Non capture move.
                if game_state.board[from_position + 8] == None:
                    move = Move()
                    move.add_change(from_position, self, None)
                    move.add_change(from_position + 8, None, self)
                    move_list.append(move)

            if from_row == 6:
                # Promotion.
                if game_state.board[from_position + 8] == None:
                    move = Move()
                    move.add_change(from_position, self, None)
                    move.add_change(from_position + 8, None, self.queen_to_promote)
                    move_list.append(move)

                # Queenside promotion capture.
                if from_col > 0:
                    to_position = from_position + 7
                    piece = game_state.board[to_position]
                    if piece:
                        if piece.white != self.white:
                            move = Move()
                            move.add_change(from_position, self, None)
                            move.add_change(to_position, piece, self.queen_to_promote)
                            move_list.append(move)

                # Kingside promotion capture.
                if from_col < 7:
                    to_position = from_position + 9
                    piece = game_state.board[to_position]
                    if piece:
                        if piece.white != self.white:
                            move = Move()
                            move.add_change(from_position, self, None)
                            move.add_change(to_position, piece, self.queen_to_promote)
                            move_list.append(move)
        else:
            if from_row == 6:
                # Non capture moves one step.
                if game_state.board[from_position - 8] == None:
                    move = Move()
                    move.add_change(from_position, self, None)
                    move.add_change(from_position - 8, None, self)
                    move_list.append(move)

                    # Non capture move two steps.
                    if game_state.board[from_position - 16] == None:
                        move = Move()
                        move.add_change(from_position, self, None)
                        move.add_change(from_position - 16, None, self)
                        # This move triggers en passant possibility.
                        move.en_passant_target_square = from_position - 8
                        move_list.append(move)

            if from_row > 1:
                # Queenside capture.
                if from_col > 0:
                    to_position = from_position - 9
                    piece = game_state.board[to_position]
                    if piece:
                        if piece.white != self.white:
                            move = Move()
                            move.add_change(from_position, self, None)
                            move.add_change(to_position, piece, self)
                            move_list.append(move)
                    # En passant.
                    if from_row == 3:
                        if to_position == game_state.en_passant_target_square:
                            move = Move()
                            move.add_change(from_position, self, None)
                            move.add_change(to_position, None, self)
                            move.add_change(from_position - 1, 
                                            game_state.board[from_position - 1], None)
                            move_list.append(move)

                # Kingside capture.
                if from_col < 7:
                    to_position = from_position - 7
                    piece = game_state.board[to_position]
                    if piece:
                        if piece.white != self.white:
                            move = Move()
                            move.add_change(from_position, self, None)
                            move.add_change(to_position, piece, self)
                            move_list.append(move)
                    # En passant.
                    if from_row == 3:
                        if to_position == game_state.en_passant_target_square:
                            move = Move()
                            move.add_change(from_position, self, None)
                            move.add_change(to_position, None, self)
                            move.add_change(from_position + 1,
                                            game_state.board[from_position + 1], None)
                            move_list.append(move)

            if 1 < from_row < 6:
                # Non capture move.
                if game_state.board[from_position - 8] == None:
                    move = Move()
                    move.add_change(from_position, self, None)
                    move.add_change(from_position - 8, None, self)
                    move_list.append(move)

            if from_row == 1:
                # Promotion.
                if game_state.board[from_position - 8] == None:
                    move = Move()
                    move.add_change(from_position, self, None)
                    move.add_change(from_position - 8, None, self.queen_to_promote)
                    move_list.append(move)

                # Queenside promotion capture.
                if from_col > 0:
                    to_position = from_position - 9
                    piece = game_state.board[to_position]
                    if piece:
                        if piece.white != self.white:
                            move = Move()
                            move.add_change(from_position, self, None)
                            move.add_change(to_position, piece, self.queen_to_promote)
                            move_list.append(move)

                # Kingside promotion capture.
                if from_col < 7:
                    to_position = from_position - 7
                    piece = game_state.board[to_position]
                    if piece:
                        if piece.white != self.white:
                            move = Move()
                            move.add_change(from_position, self, None)
                            move.add_change(to_position, piece, self.queen_to_promote)
                            move_list.append(move)
        return move_list


class GameState:

    def __init__(self, fen_string):

        # The pieces are stored in the board dictionary at keys that corresponds
        # to their position. Positions with no pieces have the value None.
        self.board = {p:None for p in range(64)}

        # Decode the FEN string.
        fen_fields = fen_string.split(" ")
        rows = fen_fields[0].split("/")
        rows.reverse()
        for row in range(8):
            i = 0
            position = row * 8
            for char in rows[row]:
                if char == "K":
                    self.board[position] = King(True)
                if char == "k":
                    self.board[position] = King(False)
                if char == "Q":
                    self.board[position] = Queen(True)
                if char == "q":
                    self.board[position] = Queen(False)
                if char == "R":
                    self.board[position] = Rook(True)
                if char == "r":
                    self.board[position] = Rook(False)
                if char == "B":
                    self.board[position] = Bishop(True)
                if char == "b":
                    self.board[position] = Bishop(False)
                if char == "N":
                    self.board[position] = Knight(True)
                if char == "n":
                    self.board[position] = Knight(False)
                if char == "P":
                    self.board[position] = Pawn(True)
                if char == "p":
                    self.board[position] = Pawn(False)
                if char in "12345678":
                    position += int(char)
                else:
                    position += 1

        self.white_to_play = fen_fields[1] == "w"

        # Information of whether the kings and rooks have been moved are
        # stored in this variable.
        self.castling_possibilities = fen_fields[2]

        if fen_fields[3] != "-":
            self.en_passant_target_square = convert_position_to_engine_format(fen_fields[3])
        else:
            self.en_passant_target_square = None
        self.en_passant_target_square_history = []

        self.value = 0
        for p in range(64):
            if self.board[p]: # If there is a piece at position p.
                self.value += self.board[p].value

    def __str__(self):
        """Make it possible to use the print command on objects of this class."""
        rows = [[" " for _ in range(8)] for _ in range(8)]
        for p in range(64):
            if self.board[p]:
                rows[p // 8][p % 8] = self.board[p].name
        return "   +" + "---+"*8 + "\n" + "\n".join([" " + str(8-i) +
               " | " + " | ".join(rows[7-i]) + " |" + "\n   +" + "---+"*8
               for i in range(8)]) + "\n     a   b   c   d   e   f   g   h"

    def possible_moves(self):
        """Return a list of Move-objects corresponding to all possible moves
        in this position, except for castlings."""
        move_list = []
        for position in range(64):
            piece = self.board[position]
            # If there is a piece.
            if piece:
                # If the piece have the right color.
                if piece.white == self.white_to_play:
                    move_list += piece.possible_moves(game_state, position)
        return move_list

    def make_move(self, move):
        """Make a change to the game_state described by the Move instance move.
        The value of the game state is also updated.
        """
        for tripple in move.change_list:
            self.board[tripple[0]] = tripple[2]
            if tripple[1]:
                self.value -= tripple[1].value
            if tripple[2]:
                self.value += tripple[2].value
        self.en_passant_target_square_history.append(self.en_passant_target_square)
        self.en_passant_target_square = move.en_passant_target_square
        self.white_to_play = not self.white_to_play

    def undo_move(self, move):
        """Make a change to the game_state that undo the move described by the
        Move instance move. The value of the game state is also updated.
        """
        for tripple in move.change_list:
            self.board[tripple[0]] = tripple[1]
            if tripple[1]:
                self.value += tripple[1].value
            if tripple[2]:
                self.value -= tripple[2].value
        self.en_passant_target_square = self.en_passant_target_square_history.pop()
        self.white_to_play = not self.white_to_play


def minimax_value(game_state, depth):
    """This function uses the minimax algorithm to analyze a game state.
    White is the maximizing player and black the minimizing."""

    # If max depth is reached or if king is captured.
    if depth == 0 or abs(game_state.value) > 500:
        return game_state.value

    # Test child nodes.
    moves = game_state.possible_moves()
    value_list = []

    # If no moves were found.
    if moves == []:
        return 0

    for move in moves:
        game_state.make_move(move)
        value_list.append(minimax_value(game_state, depth-1))
        game_state.undo_move(move)

    # If maximizing player.
    if game_state.white_to_play:
        return max(value_list)

    # If minimizing player.
    else:
        return min(value_list)

def make_random_move(game_state):
    """Make a random move to the game state. Then print out the board and the move."""
    moves = game_state.possible_moves()
    if moves:
        move = random.choice(moves)
        game_state.make_move(move)
        print(game_state)
        print("Computer move:")
        print(move)
    else:
        print("No piece to move.")

def convert_position_to_engine_format(position):
    """Convert conventional position format to engine format.
    position can be for example "a1". For example "a1" is converted to 0.
    """
    return "abcdefgh".find(position[0]) + (int(position[1]) - 1) * 8

def convert_position_to_conventional_format(position):
    """Convert engine position format to conventional format.
    position can be an integer from 0 to 63. For example 0 is converted to "a1".
    """
    [r, c] = [position // 8 + 1, position % 8]
    return "abcdefgh"[c] + str(r)

def make_move_from_text_input(game_state):
    """Ask the user for a move and make that move. The move can be expressed in the UCI long
    algebraic notation. Return true if a move is given. Return False if the input
    is q."""
    while True:
        player_input = input("Your move: ")
        if player_input == "q":
            return False
        from_position = convert_position_to_engine_format(player_input[0:2])
        to_position = convert_position_to_engine_format(player_input[2:4])
        piece = game_state.board[from_position]
        # Check if the move is legal.
        if piece: # If there is a piece at the from position.
            if piece.white == game_state.white_to_play: # If the piece have the right color.
                if to_position in piece.possible_moves(game_state, from_position):
                    piece = game_state.board[from_position]
                    game_state.make_move(from_position, to_position)
                    print()
                    return True
        print("The move is not possible.\n")

if __name__ == '__main__':

    def print_board(game_state):
        print(game_state)
        print()

    game_state = GameState("1q1q1k2/4q3/8/8/8/8/8/2K2QQQ w - -")

    # Standard starting position.
    game_state = GameState("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -")
    #print(game_state)
    #print()

    game_state = GameState("r1bqk2r/ppp1bppp/2np1n2/4p3/2B1P3/P1N2N2/1PPP1PPP/R1BQK2R w KQkq -")
    #print(game_state)
    #print()

    # Empty position.
    game_state = GameState("8/8/8/8/8/8/8/8 w - -")
    #print(game_state)
    #print()

#    game_state = GameState("7r/r7/2K2k2/NNn1R3/8/8/8/R7 w - -")

#    print()
#    print("Type q to quit.")
#    print()
#    print_board(game_state)
#    while True:
#        print("Position value: ", game_state.value)
#        if not make_move_from_text_input(game_state):
#            break
#        make_random_move(game_state)

    #game_state = GameState("8/8/8/3k4/8/3K4/8/8 w - -")
    #game_state = GameState("8/6n1/8/3k4/8/3K4/8/N7 w - -")
    #game_state = GameState("n7/6n1/8/3k4/8/3K4/8/NN6 w - -")
    #game_state = GameState("2n4r/R3n3/4k1r1/8/1N6/8/8/RK2N3 w - -")
    #game_state = GameState("rk3n2/8/8/8/8/8/8/2KRR1N1 w - -")
    #game_state = GameState("4r1rn/R2n2kn/5r2/2R5/8/1K6/2NN4/RRR5 w - -")
    #game_state = GameState("3k3r/8/3N4/2K5/8/8/8/8 w - -") # Fork
    #game_state = GameState("3k3r/5N2/8/2K5/8/8/8/8 b - -") # Fork
    #game_state = GameState("3r4/8/8/3k4/8/8/1KR5/8 w - -")    
    #game_state = GameState("2k5/8/4p3/6p1/8/8/PP2P1P1/3K4 w - -") # Pawns and kings
    #game_state = GameState("2k5/8/4p3/6p1/1P6/P3P1P1/8/3K4 w - -") # Pawns and kings
    #game_state = GameState("1k3q2/2r3n1/8/8/8/3N1B2/1N6/1K3Q2 w - -")
    #game_state = GameState("1k3q2/8/8/8/8/8/8/1K6 w - -")
    #game_state = GameState("1k4r1/8/8/8/8/b7/B7/1K6 w - -")
    #game_state = GameState("3k4/R7/8/8/8/8/1K5R/8 w - -") # Mate in 1.
    #game_state = GameState("1k6/8/8/8/8/8/6p1/1K3Q2 b - -")
    #game_state = GameState("8/8/8/3pP3/8/8/8/1K5k w - d6 0 2")
    #game_state = GameState("1k6/8/8/8/3pP3/8/8/1K6 b - e3 0 1")
    #game_state = GameState("k1K5/4p3/5Q2/8/8/8/8/8 b - -")
    #game_state = GameState("1k6/8/8/3pP3/8/8/8/1K6 w - d6 0 2") # En passant possible
    #game_state = GameState("1k6/8/8/4Pp2/8/8/8/1K6 w - f6 0 2") # En passant possible.
    #game_state = GameState("1k6/8/8/8/4Pp2/8/8/1K6 b - e3 0 1") # En passant possible.
    #game_state = GameState("8/8/8/3r1k2/2R5/8/2K1P3/8 w - -")
    #game_state = GameState("r7/1P6/8/8/8/7k/8/3K4 w - -")
    #game_state = GameState("6r1/5P2/8/8/8/7k/8/3K4 w - -")
    #game_state = GameState("2k5/4r3/5P2/8/8/8/8/3K4 w - -")
    #game_state = GameState("2k5/8/8/1r6/P7/8/8/3K4 w - -")
    #game_state = GameState("2k5/8/4p3/1r3Bp1/P4n2/4P2q/2P3P1/3K4 w - -")
    game_state = GameState("1k6/3PP3/2P2PP1/8/2p2p2/3p4/4p1p1/1K6 w - -")
    game_state = GameState("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -")
    #game_state = GameState("")
    #game_state = GameState("")
    #game_state = GameState("")
    #game_state = GameState("")
    #game_state = GameState("")
    #game_state = GameState("")
    #game_state = GameState("")
    #game_state = GameState("")
    #game_state = GameState("")
    #game_state = GameState("")
    #game_state = GameState("")
    #game_state = GameState("")
    #game_state = GameState("")
    #game_state = GameState("")
    #game_state = GameState("")
    #game_state = GameState("")
    #game_state = GameState("")
    #game_state = GameState("")
    #game_state = GameState("")
    #game_state = GameState("")
    #game_state = GameState("")
    #game_state = GameState("")
    #game_state = GameState("")
    #game_state = GameState("")
    #game_state = GameState("")
    #game_state = GameState("")
    #game_state = GameState("")
    #game_state = GameState("")
    #game_state = GameState("")
    #game_state = GameState("")
    #game_state = GameState("")
    #game_state = GameState("")
    #game_state = GameState("")
    #game_state = GameState("")
    #game_state = GameState("")
    #game_state = GameState("")
    #game_state = GameState("")
    #game_state = GameState("")
    #game_state = GameState("")
    #game_state = GameState("")
    #game_state = GameState("")
    #game_state = GameState("")
    #game_state = GameState("")
    #game_state = GameState("")

    print(minimax_value(game_state, 2))

    print(game_state)
    for n in range(100):
        make_random_move(game_state)
        print("Position value: ", game_state.value)

#    for n in range(100):
#        moves = game_state.possible_moves()
#        move = random.choice(moves)
#        game_state.make_move(move)
#        print(game_state)
#        print(move)





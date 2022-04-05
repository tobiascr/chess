"""Positions are represented as integers from 0 to 63. 0 represent a1,
1 represent b1, 8 represent a2 etc.
"""

import random

def computer_move_UCI(FEN_string):
    """Return a move that is computed by the engine. The move is returned in the UCI format.
    """
    game_state = GameState(FEN_string)
    move = computer_move(game_state)
    return move.UCI_move_format_string()


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
            line = convert_position_to_conventional_format(change[0]) + ": "
            if change[1]:
                line += change[1].name + " -> "
            else:
                line += "None -> "
            if change[2]:
                line += change[2].name
            else:
                line += "None"
            lines.append(line)
        return ", ".join(lines)

    def add_change(self, position, value_before_change, value_after_change):
        """The values can be piece-objects or None."""
        self.change_list.append((position, value_before_change, value_after_change))

    def UCI_move_format_string(self):
        """Return the move in the UCI move format. For example like:
        "e2e4", "e7e5", "e1g1" (white short castling), "e7e8q" (for promotion),
        "c5b6" (en passant).
        """
        if len(self.change_list) == 2:
            # The position where the move starts is not empty before the change.
            if self.change_list[0][1] != None:
                from_triple = self.change_list[0]
                to_triple = self.change_list[1]
            else:
                from_triple = self.change_list[1]
                to_triple = self.change_list[0]

            from_position = convert_position_to_conventional_format(from_triple[0])
            to_position = convert_position_to_conventional_format(to_triple[0])
            from_piece = from_triple[1].name
            to_piece = to_triple[2].name

            # If promotion.
            if from_piece != to_piece:
                if to_piece == "Q" or to_piece == "q":
                    return from_position + to_position + "q"
                if to_piece == "R" or to_piece == "r":
                    return from_position + to_position + "r"
                if to_piece == "B" or to_piece == "b":
                    return from_position + to_position + "b"
                if to_piece == "N" or to_piece == "n":
                    return from_position + to_position + "n"
            else:
                return from_position + to_position

        # En passants.
        if len(self.change_list) == 3:
            positions = [convert_position_to_conventional_format(p) 
                         for (p, vb, va) in self.change_list]
            # The from position has a unique file.
            files = [p[0] for p in positions]
            for p in positions:
                if files.count(p[0]) == 1:
                    from_position = p
                    break

            # The to position has a unique row.
            rows = [p[1] for p in positions]
            for p in positions:
                if rows.count(p[1]) == 1:
                    to_position = p
                    break

            return from_position + to_position

        # Castlings
        if len(self.change_list) == 4:
            positions = [p for (p, vb, va) in self.change_list]
            if 0 in positions:
                return "e1c1"
            if 7 in positions:
                return "e1g1"
            if 56 in positions:
                return "e8c8"
            if 63 in positions:
                return "e8g8"


class King:

    def __init__(self, white):
        self.has_moved = False
        self.white = white
        if white:
            self.name = "K"
            self.value = 10000
        else:
            self.name = "k"
            self.value = -10000
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
        capture_move_list = []
        non_capture_move_list = []
        for to_position in self.possible_moves_dict[from_position]:
            piece = game_state.board[to_position]
            if piece:

                # If there is an opposite color piece on the target square.
                if piece.white != self.white:
                    move = Move()
                    move.add_change(from_position, self, None)
                    move.add_change(to_position, piece, self)
                    capture_move_list.append(move)

            # If the is no piece on the target square.
            else:
                move = Move()
                move.add_change(from_position, self, None)
                move.add_change(to_position, None, self)
                non_capture_move_list.append(move)

        return (capture_move_list, non_capture_move_list)


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
        """Return all moves that this piece can make if it's located at from_position."""
        return (Rook.possible_moves(self, game_state, from_position)[0] +
                Bishop.possible_moves(self, game_state, from_position)[0],
                Rook.possible_moves(self, game_state, from_position)[1] +
                Bishop.possible_moves(self, game_state, from_position)[1])


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
        """Return all moves except for castlings that this piece can make if it's
        located at from_position."""
        capture_move_list = []
        non_capture_move_list = []

        # Moves up.
        for to_position in range(from_position + 8, 64, 8):
            piece = game_state.board[to_position]
            if piece:
                # If capture.
                if piece.white != self.white:
                    move = Move()
                    move.add_change(from_position, self, None)
                    move.add_change(to_position, piece, self)
                    capture_move_list.append(move)
                break
            else:
                move = Move()
                move.add_change(from_position, self, None)
                move.add_change(to_position, None, self)
                non_capture_move_list.append(move)

        # Moves down.
        for to_position in range(from_position - 8, -1, -8):
            piece = game_state.board[to_position]
            if piece:
                # If capture.
                if piece.white != self.white:
                    move = Move()
                    move.add_change(from_position, self, None)
                    move.add_change(to_position, piece, self)
                    capture_move_list.append(move)
                break
            else:
                move = Move()
                move.add_change(from_position, self, None)
                move.add_change(to_position, None, self)
                non_capture_move_list.append(move)

        # Moves right.
        for to_position in range(from_position + 1, from_position - from_position % 8 + 8, 1):
            piece = game_state.board[to_position]
            if piece:
                # If capture.
                if piece.white != self.white:
                    move = Move()
                    move.add_change(from_position, self, None)
                    move.add_change(to_position, piece, self)
                    capture_move_list.append(move)
                break
            else:
                move = Move()
                move.add_change(from_position, self, None)
                move.add_change(to_position, None, self)
                non_capture_move_list.append(move)

        # Moves left.
        for to_position in range(from_position - 1, from_position - from_position % 8 - 1, -1):
            piece = game_state.board[to_position]
            if piece:
                # If capture.
                if piece.white != self.white:
                    move = Move()
                    move.add_change(from_position, self, None)
                    move.add_change(to_position, piece, self)
                    capture_move_list.append(move)
                break
            else:
                move = Move()
                move.add_change(from_position, self, None)
                move.add_change(to_position, None, self)
                non_capture_move_list.append(move)

        return (capture_move_list, non_capture_move_list)


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
        """Return all moves this piece can make if it's located at from_position"""
        # Row and column for the position.
        [from_r, from_c] = [from_position // 8, from_position % 8]
        capture_move_list = []
        non_capture_move_list = []

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
                    capture_move_list.append(move)
                break
            else:
                move = Move()
                move.add_change(from_position, self, None)
                move.add_change(to_position, None, self)
                non_capture_move_list.append(move)
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
                    capture_move_list.append(move)
                break
            else:
                move = Move()
                move.add_change(from_position, self, None)
                move.add_change(to_position, None, self)
                non_capture_move_list.append(move)
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
                    capture_move_list.append(move)
                break
            else:
                move = Move()
                move.add_change(from_position, self, None)
                move.add_change(to_position, None, self)
                non_capture_move_list.append(move)
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
                    capture_move_list.append(move)
                break
            else:
                move = Move()
                move.add_change(from_position, self, None)
                move.add_change(to_position, None, self)
                non_capture_move_list.append(move)
            c -= 1
            r -= 1

        return (capture_move_list, non_capture_move_list)


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
        """Return all moves this piece can make if it's located at from_position."""
        capture_move_list = []
        non_capture_move_list = []
        for to_position in self.possible_moves_dict[from_position]:
            piece = game_state.board[to_position]
            if piece:

                # If there is an opposite color piece on the target square.
                if piece.white != self.white:
                    move = Move()
                    move.add_change(from_position, self, None)
                    move.add_change(to_position, piece, self)
                    capture_move_list.append(move)

            # If the is no piece on the target square.
            else:
                move = Move()
                move.add_change(from_position, self, None)
                move.add_change(to_position, None, self)
                non_capture_move_list.append(move)

        return (capture_move_list, non_capture_move_list)


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
        """Return all moves this piece can make if it's located at from_position
        with the exception of promotion to other pieces than queens."""
        capture_move_list = []
        non_capture_move_list = []
        [from_row, from_col] = [from_position // 8, from_position % 8]

        if self.white:
            if from_row == 1:
                # Non capture moves one step.
                if game_state.board[from_position + 8] == None:
                    move = Move()
                    move.add_change(from_position, self, None)
                    move.add_change(from_position + 8, None, self)
                    non_capture_move_list.append(move)

                    # Non capture move two steps.
                    if game_state.board[from_position + 16] == None:
                        move = Move()
                        move.add_change(from_position, self, None)
                        move.add_change(from_position + 16, None, self)
                        # This move triggers en passant possibility.
                        move.en_passant_target_square = from_position + 8
                        non_capture_move_list.append(move)

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
                            capture_move_list.append(move)
                    # En passant.
                    if from_row == 4:
                        if to_position == game_state.en_passant_target_square:
                            move = Move()
                            move.add_change(from_position, self, None)
                            move.add_change(to_position, None, self)
                            move.add_change(from_position - 1, 
                                            game_state.board[from_position - 1], None)
                            capture_move_list.append(move)

                # Kingside capture.
                if from_col < 7:
                    to_position = from_position + 9
                    piece = game_state.board[to_position]
                    if piece:
                        if piece.white != self.white:
                            move = Move()
                            move.add_change(from_position, self, None)
                            move.add_change(to_position, piece, self)
                            capture_move_list.append(move)
                    # En passant.
                    if from_row == 4:
                        if to_position == game_state.en_passant_target_square:
                            move = Move()
                            move.add_change(from_position, self, None)
                            move.add_change(to_position, None, self)
                            move.add_change(from_position + 1,
                                            game_state.board[from_position + 1], None)
                            capture_move_list.append(move)

            if 1 < from_row < 6:
                # Non capture move.
                if game_state.board[from_position + 8] == None:
                    move = Move()
                    move.add_change(from_position, self, None)
                    move.add_change(from_position + 8, None, self)
                    non_capture_move_list.append(move)

            if from_row == 6:
                # Promotion.
                if game_state.board[from_position + 8] == None:
                    move = Move()
                    move.add_change(from_position, self, None)
                    move.add_change(from_position + 8, None, self.queen_to_promote)
                    non_capture_move_list.append(move)

                # Queenside promotion capture.
                if from_col > 0:
                    to_position = from_position + 7
                    piece = game_state.board[to_position]
                    if piece:
                        if piece.white != self.white:
                            move = Move()
                            move.add_change(from_position, self, None)
                            move.add_change(to_position, piece, self.queen_to_promote)
                            capture_move_list.append(move)

                # Kingside promotion capture.
                if from_col < 7:
                    to_position = from_position + 9
                    piece = game_state.board[to_position]
                    if piece:
                        if piece.white != self.white:
                            move = Move()
                            move.add_change(from_position, self, None)
                            move.add_change(to_position, piece, self.queen_to_promote)
                            capture_move_list.append(move)
        else:
            if from_row == 6:
                # Non capture moves one step.
                if game_state.board[from_position - 8] == None:
                    move = Move()
                    move.add_change(from_position, self, None)
                    move.add_change(from_position - 8, None, self)
                    non_capture_move_list.append(move)

                    # Non capture move two steps.
                    if game_state.board[from_position - 16] == None:
                        move = Move()
                        move.add_change(from_position, self, None)
                        move.add_change(from_position - 16, None, self)
                        # This move triggers en passant possibility.
                        move.en_passant_target_square = from_position - 8
                        non_capture_move_list.append(move)

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
                            capture_move_list.append(move)
                    # En passant.
                    if from_row == 3:
                        if to_position == game_state.en_passant_target_square:
                            move = Move()
                            move.add_change(from_position, self, None)
                            move.add_change(to_position, None, self)
                            move.add_change(from_position - 1, 
                                            game_state.board[from_position - 1], None)
                            capture_move_list.append(move)

                # Kingside capture.
                if from_col < 7:
                    to_position = from_position - 7
                    piece = game_state.board[to_position]
                    if piece:
                        if piece.white != self.white:
                            move = Move()
                            move.add_change(from_position, self, None)
                            move.add_change(to_position, piece, self)
                            capture_move_list.append(move)
                    # En passant.
                    if from_row == 3:
                        if to_position == game_state.en_passant_target_square:
                            move = Move()
                            move.add_change(from_position, self, None)
                            move.add_change(to_position, None, self)
                            move.add_change(from_position + 1,
                                            game_state.board[from_position + 1], None)
                            capture_move_list.append(move)

            if 1 < from_row < 6:
                # Non capture move.
                if game_state.board[from_position - 8] == None:
                    move = Move()
                    move.add_change(from_position, self, None)
                    move.add_change(from_position - 8, None, self)
                    non_capture_move_list.append(move)

            if from_row == 1:
                # Promotion.
                if game_state.board[from_position - 8] == None:
                    move = Move()
                    move.add_change(from_position, self, None)
                    move.add_change(from_position - 8, None, self.queen_to_promote)
                    non_capture_move_list.append(move)

                # Queenside promotion capture.
                if from_col > 0:
                    to_position = from_position - 9
                    piece = game_state.board[to_position]
                    if piece:
                        if piece.white != self.white:
                            move = Move()
                            move.add_change(from_position, self, None)
                            move.add_change(to_position, piece, self.queen_to_promote)
                            capture_move_list.append(move)

                # Kingside promotion capture.
                if from_col < 7:
                    to_position = from_position - 7
                    piece = game_state.board[to_position]
                    if piece:
                        if piece.white != self.white:
                            move = Move()
                            move.add_change(from_position, self, None)
                            move.add_change(to_position, piece, self.queen_to_promote)
                            capture_move_list.append(move)
        return (capture_move_list, non_capture_move_list)


class GameState:

    def __init__(self, FEN_string):

        # The pieces are stored in the board list at indexes that corresponds
        # to their position. Positions with no pieces have the value None.
        self.board = [None]*64

        # Decode the FEN string.
        FEN_fields = FEN_string.split(" ")
        rows = FEN_fields[0].split("/")
        rows.reverse()
        for row in range(8):
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

        self.white_to_play = FEN_fields[1] == "w"

        # Information of whether the kings and rooks have been moved are
        # stored in this variable.
        self.castling_possibilities = FEN_fields[2]

        if FEN_fields[3] != "-":
            self.en_passant_target_square = convert_position_to_engine_format(FEN_fields[3])
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

    def pseudo_legal_moves_no_castlings(self):
        """Return a list of Move-objects corresponding to all possible pseudo-legal moves
        in this position, except for castlings and promotion to other pieces than
        queens. The moves are sorted in such a way that the capture moves are preceding
        the non capture moves."""
        capture_move_list = []
        non_capture_move_list = []
        for position in range(64):
            piece = self.board[position]
            # If there is a piece.
            if piece:
                # If the piece have the right color.
                if piece.white == self.white_to_play:
                    (c_move_list, non_c_move_list) = piece.possible_moves(self, position)
                    capture_move_list += c_move_list
                    non_capture_move_list += non_c_move_list

        # The capture moves are sorted so that moves where the captured
        # piece have a higher absolute value than the capturing piece are
        # prioritized.
        def value_difference(capture_move):
            if len(capture_move.change_list) > 2:
                return 0
            for triple in capture_move.change_list:
                if triple[2] != None:
                    return abs(triple[1].value) - abs(triple[2].value)

        capture_move_list.sort(key=value_difference, reverse=True)

        return capture_move_list + non_capture_move_list


    def legal_moves_no_castlings(self):
        """Return a list of Move-objects corresponding to all possible legal moves
        in this position, except for castlings and promotion to other pieces than
        queens."""
        move_list = []
        moves = self.pseudo_legal_moves_no_castlings()
        for move in moves:
            self.make_move(move)
            if abs(minimax(self, 1)) < 500:
                move_list.append(move)
            self.undo_move(move)
        return move_list

    def castlings(self):
        """Return a list of Move-objects corresponding to all possible castlings
        in this position. It is assumed that no moves have been made to the game state
        for while using this method."""
        move_list = []
        if self.castling_kingside_possible():
            if self.white_to_play:
                king = self.board[4]
                rook = self.board[7]
                move = Move()
                move.add_change(4, king, None)
                move.add_change(5, None, rook)
                move.add_change(6, None, king)
                move.add_change(7, rook, None)
                move_list.append(move)
            else:
                king = self.board[60]
                rook = self.board[63]
                move = Move()
                move.add_change(60, king, None)
                move.add_change(61, None, rook)
                move.add_change(62, None, king)
                move.add_change(63, rook, None)
                move_list.append(move)
        if self.castling_queenside_possible():
            if self.white_to_play:
                king = self.board[4]
                rook = self.board[0]
                move = Move()
                move.add_change(4, king, None)
                move.add_change(3, None, rook)
                move.add_change(2, None, king)
                move.add_change(0, rook, None)
                move_list.append(move)
            else:
                king = self.board[60]
                rook = self.board[56]
                move = Move()
                move.add_change(60, king, None)
                move.add_change(59, None, rook)
                move.add_change(58, None, king)
                move.add_change(56, rook, None)
                move_list.append(move)
        return move_list

    def make_move(self, move):
        """Make a change to the game_state described by the Move instance move.
        The value of the game state is also updated.
        """
        for triple in move.change_list:
            self.board[triple[0]] = triple[2]
            if triple[1]:
                self.value -= triple[1].value
            if triple[2]:
                self.value += triple[2].value
        self.en_passant_target_square_history.append(self.en_passant_target_square)
        self.en_passant_target_square = move.en_passant_target_square
        self.white_to_play = not self.white_to_play

    def undo_move(self, move):
        """Make a change to the game_state that undo the move described by the
        Move instance move. The value of the game state is also updated.
        """
        for triple in move.change_list:
            self.board[triple[0]] = triple[1]
            if triple[1]:
                self.value += triple[1].value
            if triple[2]:
                self.value -= triple[2].value
        self.en_passant_target_square = self.en_passant_target_square_history.pop()
        self.white_to_play = not self.white_to_play

    def check(self):
        """Return True if the king of the player in turn is in check and
        False if not.
        """
        nullmove = Move()
        self.make_move(nullmove)
        result = abs(minimax(self, 1)) > 500
        self.undo_move(nullmove)
        return result

    def castling_kingside_possible(self):
        """Return True if the player in turn can make kingside castling
        and False if not. This function is assumed to only be used if no moves
        have been made to the game_state object, since castling rights may not
        valid then.
        """
        if self.check():
            return False
        if self.white_to_play:
            if "K" in self.castling_possibilities:
                if self.board[5] == self.board[6] == None:

                    king = self.board[4]
                    move = Move()
                    move.add_change(4, king, None)
                    move.add_change(5, None, king)
                    self.make_move(move)
                    if abs(minimax(self, 1)) > 500:
                        self.undo_move(move)
                        return False
                    self.undo_move(move)

                    move = Move()
                    move.add_change(4, king, None)
                    move.add_change(6, None, king)
                    self.make_move(move)
                    if abs(minimax(self, 1)) > 500:
                        self.undo_move(move)
                        return False
                    self.undo_move(move)

                    return True
        else:
            if "k" in self.castling_possibilities:

                if self.board[61] == self.board[62] == None:

                    king = self.board[60]
                    move = Move()
                    move.add_change(60, king, None)
                    move.add_change(61, None, king)
                    self.make_move(move)
                    if abs(minimax(self, 1)) > 500:
                        self.undo_move(move)
                        return False
                    self.undo_move(move)

                    move = Move()
                    move.add_change(60, king, None)
                    move.add_change(62, None, king)
                    self.make_move(move)
                    if abs(minimax(self, 1)) > 500:
                        self.undo_move(move)
                        return False
                    self.undo_move(move)

                    return True
        return False

    def castling_queenside_possible(self):
        """Return True if the player in turn can make queenside castling
        and False if not. This function is assumed to only be used if no moves
        have been made to the game_state object, since castling rights may not
        valid then."""
        if self.check():
            return False
        if self.white_to_play:
            if "Q" in self.castling_possibilities:
                if self.board[1] == self.board[2] == self.board[3] == None:

                    king = self.board[4]
                    move = Move()
                    move.add_change(4, king, None)
                    move.add_change(3, None, king)
                    self.make_move(move)
                    if abs(minimax(self, 1)) > 500:
                        self.undo_move(move)
                        return False
                    self.undo_move(move)

                    move = Move()
                    move.add_change(4, king, None)
                    move.add_change(2, None, king)
                    self.make_move(move)
                    if abs(minimax(self, 1)) > 500:
                        self.undo_move(move)
                        return False
                    self.undo_move(move)

                    return True
        else:
            if "q" in self.castling_possibilities:

                if self.board[57] == self.board[58] == self.board[59] == None:

                    king = self.board[60]
                    move = Move()
                    move.add_change(60, king, None)
                    move.add_change(59, None, king)
                    self.make_move(move)
                    if abs(minimax(self, 1)) > 500:
                        self.undo_move(move)
                        return False
                    self.undo_move(move)

                    move = Move()
                    move.add_change(60, king, None)
                    move.add_change(58, None, king)
                    self.make_move(move)
                    if abs(minimax(self, 1)) > 500:
                        self.undo_move(move)
                        return False
                    self.undo_move(move)

                    return True
        return False


def minimax(game_state, depth):
    """This function uses the minimax algorithm to analyze a game state.
    White is the maximizing player and black the minimizing.
    """
    # If max depth is reached or if king is captured.
    if depth == 0 or abs(game_state.value) > 500:
        return game_state.value

    # Test child nodes.
    moves = game_state.pseudo_legal_moves_no_castlings()
    value_list = []

    # If no moves were found.
    if moves == []:
        return 0

    for move in moves:
        game_state.make_move(move)
        value_list.append(minimax(game_state, depth-1))
        game_state.undo_move(move)

    # If maximizing player.
    if game_state.white_to_play:
        return max(value_list)

    # If minimizing player.
    else:
        return min(value_list)

def negamax(game_state, depth, alpha, beta):
    """Compute a value of game_state. The value is seen from the perspective of the
    player in turn. A favorable position for that player is given a positive value.
    """

    #global node_counter
    #node_counter += 1

    # If max depth is reached or if king is captured.
    if depth == 0 or abs(game_state.value) > 500:
        if game_state.white_to_play:
            return game_state.value
        else:
            return -game_state.value

    # Test child nodes.
    moves = game_state.pseudo_legal_moves_no_castlings()
    value_list = []

    # If no moves were found.
    if moves == []:
        return 0

    # Else, return a value based on child node values.
    best_value = -1000000
    for move in moves:
        game_state.make_move(move)
        new_value = -negamax(game_state, depth-1, -beta, -alpha)
        game_state.undo_move(move)
        best_value = max(best_value, new_value)
        alpha = max(alpha, new_value)
        if beta <= alpha:
            break
    return best_value

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

def computer_move(game_state):
    """Return a move that is computed with the minimax algorithm.
    This function is assumed to only be used if no moves
    have been made to the game_state object, since castling rights may not
    valid then."""

    global node_counter
    node_counter = 0

    moves = game_state.legal_moves_no_castlings() + game_state.castlings()

    number_of_pieces = 0
    for s in range(64):
        if game_state.board[s] != None:
            number_of_pieces += 1

    if number_of_pieces > 15:
        depth = 3
    else:
        depth = 4

    best_move = None

    # The move order is randomized in order to make opening move
    # selection more natural.
    random.shuffle(moves)

    if moves == []:
        return None

    alpha = -1000000
    beta = 1000000
    for move in moves:
        game_state.make_move(move)
        value = -negamax(game_state, depth, -beta, -alpha)
        if value > alpha:
            best_move = move
            alpha = value
        game_state.undo_move(move)

    #print(node_counter)

    return best_move

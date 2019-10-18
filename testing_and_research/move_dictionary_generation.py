
import pprint

# In this program I try to generate dictionaries of possible moves
# for various positions of pieces.

def possible_king_moves(position):
    # Row and column for the position.
    [r, c] = [position // 8, position % 8]

    # Moves that inlude outside of board positions.
    moves = [(r-1, c-1), (r-1, c), (r-1, c+1), (r, c-1), (r, c+1),
             (r+1, c-1), (r+1, c), (r+1, c+1)]

    # Moves where outside of board positions are pruned off.
    moves_on_board = []
    for (r, c) in moves:
        if 0 <= r <= 7 and 0 <= c <= 7:
            moves_on_board.append((r, c))

    return [8*r+c for (r, c) in moves_on_board]

def possible_knight_moves(position):
    # Row and column for the position.
    [r, c] = [position // 8, position % 8]

    # Moves that inlude outside of board positions.
    moves = [(r+2, c-1), (r+2, c+1), (r+1, c+2), (r-1, c+2),
             (r-2, c+1), (r-2, c-1), (r-1, c-2), (r+1, c-2)]

    # Moves where outside of board positions are pruned off.
    moves_on_board = []
    for (r, c) in moves:
        if 0 <= r <= 7 and 0 <= c <= 7:
            moves_on_board.append((r, c))

    return [8*r+c for (r, c) in moves_on_board]


pp = pprint.PrettyPrinter(indent=17)

move_dict_king = {p:possible_king_moves(p) for p in range(64)}
pp.pprint(move_dict_king)

print()

move_dict_knight = {p:possible_knight_moves(p) for p in range(64)}
pp.pprint(move_dict_knight)

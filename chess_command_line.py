
from game import Game

def print_board(game, board_orientation):
    """board_orientation can be "w" or "b"."""
    if board_orientation == "w":
        print_board_normal_orientation(game)
    if board_orientation == "b":
        print_board_upside_down(game)

def print_board_normal_orientation(game):
    rows = []
    for n in range(8, 0, -1):
        row = ""
        for file in "abcdefgh":
            value = game.board_value(file+str(n))
            if value == None:
                row += " "
            else:
                row += value
        rows.append(row)

    print("   +" + "---+"*8 + "\n" + "\n".join([" " + str(8-i) +
               " | " + " | ".join(rows[i]) + " |" + "\n   +" + "---+"*8
               for i in range(8)]) + "\n     a   b   c   d   e   f   g   h")

def print_board_upside_down(game):
    rows = []
    for n in range(1, 9):
        row = ""
        for file in "hgfedcba":
            value = game.board_value(file+str(n))
            if value == None:
                row += " "
            else:
                row += value
        rows.append(row)

    print("   +" + "---+"*8 + "\n" + "\n".join([" " + str(i+1) +
               " | " + " | ".join(rows[i]) + " |" + "\n   +" + "---+"*8
               for i in range(8)]) + "\n     h   g   f   e   d   c   b   a")

def play_game(board_orientation):
    """board_orientation can be "w" or "b"."""
    print_board(game, board_orientation)
    print()
    while True:

        while True:
            player_input = input("Your move: ")
            if player_input == "q":
                break
            else:
                if not game.legal(player_input):
                    print("Not a legal move.")
                else:
                    game.make_move(player_input)
                    break

        if player_input == "q":
            break

        if game.check_mate():
            print_board(game, board_orientation)
            print("You win! Check mate.")
            break
        if game.stale_mate():
            print_board(game, board_orientation)
            print("Stale mate")
            break
        if game.insufficient_material():
            print_board(game, board_orientation)
            print("Draw by insufficient material.")
            break
        if game.threefold_repetition():
            print_board(game, board_orientation)
            print("Draw by threefold repetition.")
            break
        if game.possible_draw_by_50_move_rule():
            print_board(game, board_orientation)
            print("Draw by the 50 move rule.")
            break

        move = game.computer_move()
        game.make_move(move)
        print_board(game, board_orientation)
        print("Computer move:", move)

        if game.check_mate():
            print("Computer win! Check mate.")
            break
        if game.stale_mate():
            print("Stale mate")
            break
        if game.insufficient_material():
            print("Draw by insufficient material.")
            break
        if game.threefold_repetition():
            print("Draw by threefold repetition.")
            break
        if game.possible_draw_by_50_move_rule():
            print("Draw by the 50 move rule.")
            break

print("Pieces are denoted as follows:")
print()
print("P: white pawn   -  p: black pawn")
print("N: white knight -  n: black knight")
print("B: white biship -  b: black bishop")
print("R: white rook   -  r: black rook")
print("Q: white queen  -  q: black queen")
print("K: white king   -  k: black king")
print()
print("You can make moves by typing for example:")
print("e2e4, e7e5, e1g1 (white short castling), e7e8q (for promotion),")
print("c5b6 (en passant).")
print()
print("Type q to quit.")
print()
print("1) Play white")
print("2) Play black")
print()

game = Game("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -")

while True:
    player_input = input("Your choice: ")
    if player_input == "1":
        play_game("w")
        break
    if player_input == "2":
        move = game.computer_move()
        game.make_move(move)
        play_game("b")
        break
    if player_input == "q":
        break

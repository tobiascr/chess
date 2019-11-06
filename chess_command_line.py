
from game import Game

def play_game():
    print(game)
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
            print(game)
            print("You win! Check mate.")
            break
        if game.stale_mate():
            print(game)
            print("Stale mate")
            break
        if game.insufficient_material():
            print(game)
            print("Draw by insufficient material.")
            break
        if game.threefold_repetition():
            print(game)
            print("Draw by threefold repetition.")
            break
        if game.possible_draw_by_50_move_rule():
            print(game)
            print("Draw by the 50 move rule.")
            break

        move = game.computer_move()
        game.make_move(move)
        print(game)
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

game = Game("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -")

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

while True:
    player_input = input("Your choice: ")
    if player_input == "1":
        play_game()
        break
    if player_input == "2":
        move = game.computer_move()
        game.make_move(move)
        play_game()
        break
    if player_input == "q":
        break

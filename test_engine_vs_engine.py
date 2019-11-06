
from game import Game

# The engine plays against itself.
#game = Game("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -")
#game = Game("3n4/8/8/7K/8/8/2k4B/8 w - -")
#game = Game("k7/1pp5/1p6/8/8/8/8/Q5K1 b - -")
#game = Game("k7/1pp5/1pq5/8/8/8/8/Q5K1 b - -")
game = Game("8/kpp5/1p4r1/8/Q7/6r1/8/7K b - -")

print(game)
while(True):
    move = game.computer_move()
    game.make_move(move)
    print(game)
    print("FEN:", game.FEN_string)
    print("Last move:", move)
    if game.check_mate():
        print("Check mate")
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

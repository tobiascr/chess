
from game import Game

import engine as engine1
import test_engine as engine2

# An engine plays against another engine.

number_of_games = int(input("Number of games: "))

engine1_wins = 0
engine2_wins = 0
draws = 0
engine1_name = "engine.py"
engine2_name = "test_engine.py"

for n in range(1, number_of_games + 1):
    game = Game("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -")
    engine1_to_play = (n % 2) == 1
    print(game)
    while(True):
        if engine1_to_play:
            move = engine1.computer_move_UCI(game.FEN_string)
        else:
            move = engine2.computer_move_UCI(game.FEN_string)
        engine1_to_play = not engine1_to_play
        game.make_move(move)
        print(game)
        print("game ", n)

        def print_info():
            print(engine1_name + " wins:", engine1_wins)
            print(engine2_name + " wins:", engine2_wins)
            print("draws:", draws)

        print("FEN:", game.FEN_string)
        print("Last move:", move)
        if game.check_mate():
            print("Check mate")
            if engine1_to_play:
                engine2_wins += 1
                print(engine2_name + " win")
            else:
                engine1_wins += 1
                print(engine1_name + " win")
            print_info()
            break
        if game.stale_mate():
            draws += 1
            print("Stale mate")
            print_info()
            break
        if game.insufficient_material():
            draws += 1
            print("Draw by insufficient material.")
            print_info()
            break
        if game.threefold_repetition():
            draws += 1
            print("Draw by threefold repetition.")
            print_info()
            break
        if game.possible_draw_by_50_move_rule():
            draws += 1
            print("Draw by the 50 move rule.")
            print_info()
            break
        print_info()



from game import Game
import time
import engine as engine1
import test_engine as engine2

# An engine plays against another engine.

number_of_games = int(input("Number of games: "))

engine1_wins = 0
engine2_wins = 0
draws = 0
engine1_time = 0
engine2_time = 0
engine1_max_move_time = 0
engine2_max_move_time = 0
engine1_number_of_moves = 0
engine2_number_of_moves = 0
engine1_name = "engine.py"
engine2_name = "test_engine.py"

for n in range(1, number_of_games + 1):
    game = Game("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -")

    engine1_to_play = (n % 2) == 1
    print(game)
    while(True):
        start_time = time.perf_counter()
        if engine1_to_play:
            move = engine1.computer_move_UCI(game.FEN_string)
            engine1_number_of_moves += 1
            move_time = time.perf_counter() - start_time
            engine1_time += move_time
            engine1_max_move_time = max(move_time, engine1_max_move_time)
        else:
            move = engine2.computer_move_UCI(game.FEN_string)
            engine2_number_of_moves += 1
            move_time = time.perf_counter() - start_time
            engine2_time += move_time
            engine2_max_move_time = max(move_time, engine2_max_move_time)
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

print(engine1_name + " time used for all games:", engine1_time, "s")
print(engine2_name + " time used for all games:", engine2_time, "s")
print(engine1_name + " max move time:", engine1_max_move_time, "s")
print(engine2_name + " max move time:", engine2_max_move_time, "s")
print(engine1_name + " average move time:", engine1_time/engine1_number_of_moves, "s")
print(engine2_name + " average move time:", engine2_time/engine2_number_of_moves, "s")



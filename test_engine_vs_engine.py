
import engine as chess

# The engine play against itself.
game_state = chess.GameState("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -")
print(game_state)
for n in range(200):
    move = chess.computer_move(game_state)
    game_state.make_move(move)
    print(game_state)
    print(move)
    print("Position value: ", game_state.value)
    if game_state.check_mate():
        if game_state.white_to_play:
            print("Black win")
        else:
            print("White win")
        print("Check mate")
        break
    if game_state.stale_mate():
        print("Stale mate")
        break

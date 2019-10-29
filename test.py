
import chess

#game_state = chess.GameState("8/1Q1K4/R7/8/8/k7/8/4b3 b - -") # Check
#game_state = chess.GameState("8/1Q1K4/R7/8/8/k7/8/8 b - -") # Check mate
#game_state = chess.GameState("K7/P2n4/1n6/8/8/k4b2/8/8 w - -") # Check mate
#game_state = chess.GameState("K7/P2n4/b7/8/8/k7/8/8 w - -") # Stale mate
game_state = chess.GameState("K7/P7/5N2/8/8/4k3/R7/3R1R2 b - -") # Stale mate

#game_state = chess.GameState("")
#game_state = chess.GameState("")
#game_state = chess.GameState("")
#game_state = chess.GameState("")
#game_state = chess.GameState("")
#game_state = chess.GameState("")
#game_state = chess.GameState("")
#game_state = chess.GameState("")
#game_state = chess.GameState("")
#game_state = chess.GameState("")
#game_state = chess.GameState("")
#game_state = chess.GameState("")
#game_state = chess.GameState("")
#game_state = chess.GameState("")
#game_state = chess.GameState("")
#game_state = chess.GameState("")
#game_state = chess.GameState("")
#game_state = chess.GameState("")
#game_state = chess.GameState("")
#game_state = chess.GameState("")
#game_state = chess.GameState("")
#game_state = chess.GameState("")
#game_state = chess.GameState("")
#game_state = chess.GameState("")
#game_state = chess.GameState("")
#game_state = chess.GameState("")

print(game_state)
print("Check:", game_state.check())
print("Check mate:", game_state.check_mate())
print("Stale mate:", game_state.stale_mate())

if not game_state.check_mate() and not game_state.stale_mate():
    moves = game_state.legal_moves_no_castlings()
    print("Possible moves:")
    for move in moves:
        print(move)
    move = chess.computer_move(game_state)
    game_state.make_move(move)
    print(game_state)
    print(move)

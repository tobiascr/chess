
import engine as chess

#game_state = chess.GameState("8/1Q1K4/R7/8/8/k7/8/4b3 b - -") # Check
#game_state = chess.GameState("8/1Q1K4/R7/8/8/k7/8/8 b - -") # Check mate
#game_state = chess.GameState("K7/P2n4/1n6/8/8/k4b2/8/8 w - -") # Check mate
#game_state = chess.GameState("K7/P2n4/b7/8/8/k7/8/8 w - -") # Stale mate
#game_state = chess.GameState("K7/P7/5N2/8/8/4k3/R7/3R1R2 b - -") # Stale mate

 # Castling tests
#game_state = chess.GameState("3k4/3p4/1q6/8/8/8/8/4K2R w K -")
#game_state = chess.GameState("3k4/3p4/8/8/8/4n3/8/4K2R w K -")
#game_state = chess.GameState("3k4/2np4/8/8/8/8/8/4K2R w K -")
#game_state = chess.GameState("3k4/2np4/8/8/8/8/8/4K1BR w K -") 
#game_state = chess.GameState("3k4/2np4/6B1/8/8/8/8/4K2R w - -")
#game_state = chess.GameState("3k4/8/8/8/8/2b5/8/4K2R w K -")
#game_state = chess.GameState("4k2r/2N5/8/8/2b5/8/8/4K2R b Kk -")
#game_state = chess.GameState("4k2r/7N/8/8/2b5/8/8/4K2R b Kk -")
#game_state = chess.GameState("4k2r/8/8/6N1/2b5/8/8/4K2R b Kk -")
#game_state = chess.GameState("2q1k2r/8/8/6N1/8/1b6/8/R3K3 w Q -")
#game_state = chess.GameState("r3k3/7q/2N5/8/8/1b6/8/R3K3 b q -")
#game_state = chess.GameState("r3k3/7q/1N6/8/8/1b6/8/R3K3 b q -")
#game_state = chess.GameState("r3k3/8/8/8/6R1/8/8/4K3 b q -")
#game_state = chess.GameState("rnbqkb1r/ppp2ppp/3p1n2/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq -")
#game_state = chess.GameState("1k6/8/8/8/8/8/8/R3K2R w KQ -")
#game_state = chess.GameState("r3k2r/8/8/8/8/8/8/4K3 b kq -")
#game_state = chess.GameState("r3k2r/8/6N1/8/8/8/8/4K3 b kq -")
#game_state = chess.GameState("8/8/8/8/4n3/2n4k/7P/4K2R w K -")
#game_state = chess.GameState("8/8/8/8/4n3/k5n1/P7/R3K3 w Q -")
#game_state = chess.GameState("8/8/8/8/8/k7/P7/R3K3 w Q -")
#game_state = chess.GameState("8/6b1/8/8/8/k7/P7/R3K3 w Q -")
#game_state = chess.GameState("r3k3/p5b1/K7/8/8/8/P6B/R6Q b q -")
game_state = chess.GameState("4k2r/7p/7K/8/8/8/1B6/8 b k -")
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
print("Kingside castling possible:", game_state.castling_kingside_possible())
print("Queenside castling possible:", game_state.castling_queenside_possible())

if not game_state.check_mate() and not game_state.stale_mate():
    moves = game_state.legal_moves_no_castlings() + game_state.castlings()
    print("Possible moves:")
    for move in moves:
        print(move)
    move = chess.computer_move(game_state)
    game_state.make_move(move)
    print(game_state)
    print(move)

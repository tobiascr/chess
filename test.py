
import engine

#FEN_string = "8/1Q1K4/R7/8/8/k7/8/4b3 b - -" # Check
#FEN_string = "8/1Q1K4/R7/8/8/k7/8/8 b - -" # Check mate
#FEN_string = "K7/P2n4/1n6/8/8/k4b2/8/8 w - -" # Check mate
#FEN_string = "K7/P2n4/b7/8/8/k7/8/8 w - -" # Stale mate
#FEN_string = "K7/P7/5N2/8/8/4k3/R7/3R1R2 b - -" # Stale mate

# Castling tests
#FEN_string = "3k4/3p4/1q6/8/8/8/8/4K2R w K -"
#game_state = engine.GameState("3k4/3p4/8/8/8/4n3/8/4K2R w K -")
#game_state = engine.GameState("3k4/2np4/8/8/8/8/8/4K2R w K -")
#game_state = engine.GameState("3k4/2np4/8/8/8/8/8/4K1BR w K -") 
#game_state = engine.GameState("3k4/2np4/6B1/8/8/8/8/4K2R w - -")
#game_state = engine.GameState("3k4/8/8/8/8/2b5/8/4K2R w K -")
#game_state = engine.GameState("4k2r/2N5/8/8/2b5/8/8/4K2R b Kk -")
#game_state = engine.GameState("4k2r/7N/8/8/2b5/8/8/4K2R b Kk -")
#game_state = engine.GameState("4k2r/8/8/6N1/2b5/8/8/4K2R b Kk -")
#game_state = engine.GameState("2q1k2r/8/8/6N1/8/1b6/8/R3K3 w Q -")
#game_state = engine.GameState("r3k3/7q/2N5/8/8/1b6/8/R3K3 b q -")
#game_state = engine.GameState("r3k3/7q/1N6/8/8/1b6/8/R3K3 b q -")
#game_state = engine.GameState("r3k3/8/8/8/6R1/8/8/4K3 b q -")
#game_state = engine.GameState("rnbqkb1r/ppp2ppp/3p1n2/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq -")
#game_state = engine.GameState("1k6/8/8/8/8/8/8/R3K2R w KQ -")
#game_state = engine.GameState("r3k2r/8/8/8/8/8/8/4K3 b kq -")
#game_state = engine.GameState("r3k2r/8/6N1/8/8/8/8/4K3 b kq -")
#game_state = engine.GameState("8/8/8/8/4n3/2n4k/7P/4K2R w K -")
#game_state = engine.GameState("8/8/8/8/4n3/k5n1/P7/R3K3 w Q -")
#game_state = engine.GameState("8/8/8/8/8/k7/P7/R3K3 w Q -")
#game_state = engine.GameState("8/6b1/8/8/8/k7/P7/R3K3 w Q -")
#game_state = engine.GameState("r3k3/p5b1/K7/8/8/8/P6B/R6Q b q -")
#game_state = engine.GameState("4k2r/7p/7K/8/8/8/1B6/8 b k -")
#game_state = engine.GameState("")
#game_state = engine.GameState("")
#game_state = engine.GameState("")
#game_state = engine.GameState("")
#game_state = engine.GameState("")
#game_state = engine.GameState("")

# En passant
#game_state = engine.GameState("8/8/8/2Pp3k/8/8/3K4/8 w - d6 0 2")
#game_state = engine.GameState("7Q/1k6/8/2q5/4Pp2/8/K7/8 b - e3 0 1")
#game_state = engine.GameState("")

# Captures
FEN_string = "8/2k3r1/8/8/8/8/2K3R1/8 w - -"

#Other tests
#game_state = engine.GameState("8/4P3/8/8/7k/8/3r4/2K5 w - -")
#game_state = engine.GameState("8/4P3/8/8/3R3k/8/3r4/2K5 w - -")
#game_state = engine.GameState("8/4P3/8/7k/3R4/8/3K2p1/8 b - -")
#game_state = engine.GameState("")
#game_state = engine.GameState("")
#game_state = engine.GameState("")
#game_state = engine.GameState("")


game_state = engine.GameState(FEN_string)
print(game_state)
print("Check:", game_state.check(), engine.check(FEN_string))
print("Check mate:", game_state.check_mate(), engine.check_mate(FEN_string))
print("Stale mate:", game_state.stale_mate(), engine.stale_mate(FEN_string))
print("Kingside castling possible:", game_state.castling_kingside_possible())
print("Queenside castling possible:", game_state.castling_queenside_possible())
print("Possible moves:", engine.legal_moves_UCI(FEN_string))

move = engine.computer_move_UCI(FEN_string)
print("Best move found by the engine:", move)



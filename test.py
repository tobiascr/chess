
import engine
import game as game_module

def print_board(game):
    print(game.board_value("g2"))

#FEN_string = "8/1Q1K4/R7/8/8/k7/8/4b3 b - -" # Check
#FEN_string = "8/1Q1K4/R7/8/8/k7/8/8 b - -" # Check mate
#FEN_string = "K7/P2n4/1n6/8/8/k4b2/8/8 w - -" # Check mate
#FEN_string = "K7/P2n4/b7/8/8/k7/8/8 w - -" # Stale mate
#FEN_string = "K7/P7/5N2/8/8/4k3/R7/3R1R2 b - -" # Stale mate
#FEN_string = "KBn5/PRP5/1P6/8/8/8/8/5k2 w - - 0 1" # No possible moves

# Castling tests
#FEN_string = "3k4/3p4/1q6/8/8/8/8/4K2R w K -"
#FEN_string = "r3k2r/8/8/8/8/8/8/R3K2R w KQkq -"
#FEN_string = "r3k2r/8/8/8/8/8/8/R3K2R w KQ -"
#FEN_string = "r3k2r/8/8/8/8/8/8/R3K2R b KQkq -"
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
#FEN_string = "rnbqkb1r/ppp2ppp/3p1n2/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq -"
#game_state = engine.GameState("1k6/8/8/8/8/8/8/R3K2R w KQ -")
#game_state = engine.GameState("r3k2r/8/8/8/8/8/8/4K3 b kq -")
#game_state = engine.GameState("r3k2r/8/6N1/8/8/8/8/4K3 b kq -")
#game_state = engine.GameState("8/8/8/8/4n3/2n4k/7P/4K2R w K -")
#game_state = engine.GameState("8/8/8/8/4n3/k5n1/P7/R3K3 w Q -")
#game_state = engine.GameState("8/8/8/8/8/k7/P7/R3K3 w Q -")
#game_state = engine.GameState("8/6b1/8/8/8/k7/P7/R3K3 w Q -")
#game_state = engine.GameState("r3k3/p5b1/K7/8/8/8/P6B/R6Q b q -")
#game_state = engine.GameState("4k2r/7p/7K/8/8/8/1B6/8 b k -")
#FEN_string = "4k3/8/8/8/2Q2n2/7b/8/R3K3 w Q -"
#FEN_string = "r3k3/8/8/8/5n2/7b/8/3NK3 b q -"
#FEN_string = "4k2r/8/8/8/5n2/7b/8/3NK3 b k -"

# En passant
#FEN_string = "8/8/8/2Pp3k/8/8/3K4/8 w - d6 0 2"
#FEN_string = "7Q/1k6/8/2q5/4Pp2/8/K7/8 b - e3 0 1"
#FEN_string = "4k2r/2p5/8/8/Pp6/8/5P2/R3K3 b Qk a3"

# Trigger en passant.
#FEN_string = "4k3/8/8/8/4p3/8/5P2/4K3 w - -"
#FEN_string = "4k3/8/4p3/8/8/8/2P5/4K3 w - -"
#FEN_string = "4k3/p2p2p1/8/8/8/8/2P5/4K3 b - -"
#FEN_string = "8/8/8/2Pp3k/8/8/3K1P2/8 w - d6 0 2"
#FEN_string = "4k2r/2p5/8/8/8/8/P4P2/R3K3 w Qk -"
#FEN_string = "4k2r/2p5/8/8/1p6/8/P4P2/R3K3 w Qk -"

# Captures
#FEN_string = "8/2k3r1/8/8/8/8/2K3R1/8 w - -"

# Insufficient material
#FEN_string = "8/8/1k6/8/8/8/2K5/8 w - -"
#FEN_string = "2k5/8/5n2/8/8/8/1K6/8 w - -"
#FEN_string = "2k5/8/5n2/8/8/8/1K2B3/8 w - -"
#FEN_string = "2k5/8/5R2/8/8/8/1K6/8 w - -"

# Forks
#FEN_string = "4k3/8/8/2K4b/5n2/8/8/2Q5 b - -"

# Promotions
FEN_string = "4k2r/P7/8/8/5n2/7b/8/3NK3 w K -"
#FEN_string = "4k2r/P7/8/8/5n2/7b/6p1/3NK3 b - -"

# 50 move rule
#FEN_string = "8/r7/8/5k2/8/7R/2K5/8 w - - 104 91"

#Other tests
#game_state = engine.GameState("8/4P3/8/8/7k/8/3r4/2K5 w - -")
#game_state = engine.GameState("8/4P3/8/8/3R3k/8/3r4/2K5 w - -")
#FEN_string = "8/4P3/8/7k/3R4/8/3K2p1/8 b - -"
#FEN_string = "8/8/8/2Pp3k/8/6n1/8/4K2R b K -"
#FEN_string = "7b/8/8/2Pp3k/8/8/8/R3K3 b Q -"
#FEN_string = "r3k2r/8/8/2PBB3/8/8/8/R3K3 w Qkq -"
#FEN_string = "4k3/1p6/8/8/8/8/1Q4P1/4K3 w - -"
#FEN_string = "4k3/1p6/1Q6/8/8/8/6P1/4K3 b - - 10"
#FEN_string = "4k2n/1p6/6R1/8/8/8/1Q4P1/4K3 w - -"
#FEN_string = "4k2n/1p6/6R1/8/8/1Q6/6P1/4K3 b - - 40"
#FEN_string = "4k3/1p3n2/6R1/8/8/1Q6/6P1/4K3 w - - 41"
#FEN_string = "4k3/1p3n2/6R1/8/6P1/1Q6/8/4K3 b - g3 0"
#FEN_string = "rnbqk1nr/pppp1ppp/1b2p3/8/3PP3/3B1N2/PPP2PPP/RNBQK2R b KQkq - 2 4"
#FEN_string = "rnbqk2r/pppp1ppp/1b2pn2/8/3PP3/3B1N2/PPP2PPP/RNBQK2R w KQkq - 3 5"
#FEN_string = "3n4/8/8/7K/8/8/2k4B/8 w - -"
#FEN_string = "r7/5k1p/6p1/5n2/3p3P/2pK4/P4Pb1/R3R3 w - - 2 34"

#FEN_string = ""
#FEN_string = ""
#FEN_string = ""
#FEN_string = ""
#FEN_string = ""
#FEN_string = ""
#FEN_string = ""
#FEN_string = ""
#FEN_string = ""
#FEN_string = ""
#FEN_string = ""
#FEN_string = ""
#FEN_string = ""
#FEN_string = ""

game_state = engine.GameState(FEN_string)
game = game_module.Game(FEN_string)
print(game)
print("FEN-string:", FEN_string)
print("Check:", engine.check(FEN_string))
print("Check mate:", engine.check_mate(FEN_string))
print("Stale mate:", engine.stale_mate(FEN_string))
print("Kingside castling possible:", game_state.castling_kingside_possible())
print("Queenside castling possible:", game_state.castling_queenside_possible())
print("Insufficient material:", game.insufficient_material())
print("Draw by the 50 move rule: ", game.possible_draw_by_50_move_rule())
print("Possible moves:", engine.legal_moves_UCI(FEN_string))

if engine.legal_moves_UCI(FEN_string):
    move = engine.computer_move_UCI(FEN_string)
    print("Best move found by engine:", move)

    game.make_move(move)

    print(game)
    print(game.FEN_string)

    print("Threefold repetition: ", game.threefold_repetition())




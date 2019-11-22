
"""This program is for testing the speed of the engine."""

import engine
import time

# Some positions to test.
test_positions = [
"rn1qkb1r/ppp2ppp/5n2/3p4/3P2b1/2N2N2/PPP2PPP/R1BQKB1R w KQkq - 3 6",
"rn1qkb1r/pp3ppb/2p2n1p/3pN3/3P2PB/2N4P/PPP2P2/R2QKB1R w KQkq - 3 11",
"r2q1rk1/pp3ppb/2p4p/3pn1P1/3P4/2N3Q1/PPP2P2/2KR1BR1 b - - 0 18",
"r7/pR6/2p1kp2/3p4/5p2/2NP4/PP6/2K5 b - - 0 29",
"rq3rk1/p1pbn1b1/2p1p1pp/3pPp2/3P1P2/2P2NQ1/PP4PP/RNB2RK1 w - - 2 14",
"1r3rk1/2p1n1b1/1q2p1pp/p2pPp2/3PbP2/1P2NNQ1/PR4PP/2B1R1K1 w - - 5 22"
]

t0 = time.time()
for n in range(3):
    for FEN_string in test_positions:
        print(engine.computer_move_UCI(FEN_string))
t1 = time.time()
print("Time:", t1 - t0)

import chess

import AI

board = chess.Board()
move_finder = AI.MoveFinder(board)

print(board)
counter = 0
while True:
    board.push(move_finder.findBestMoveNegaMax(board))
    counter += 1
    print("move: " + str(counter))
    print(board)

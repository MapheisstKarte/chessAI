import chess

import AI

board = chess.Board()
move_finder = AI.MoveFinder(board)

print(board)
counter = 0
while True:
    move = move_finder.findBestMoveNegaMax(board)
    board.push(move)
    counter += 1
    print("move: " + str(counter))
    print("move: " + str(move))
    print(board)

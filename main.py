import time

import chess

import AI

board = chess.Board()

print(board)
while not board.is_game_over():
    if not board.is_game_over():
        if board.turn:

            playerMove = input()
            board.push_san(playerMove)
            timeStart = time.time()
            print(board)

        elif not board.turn:

            print("-------------------------------")
            AIMove = AI.findBestMoveNegaMax(board, board.legal_moves)
            board.push(AIMove)
            timeEnd = time.time()
            print("Time to move: " + str(timeEnd - timeStart))
            evaluation = AI.evaluate(board)
            print("Evaluation " + str(evaluation))
            print("AI Move: " + chess.Move.__str__(AIMove))
            print(board)
            print("-------------------------------")

else:
    print("Game Over: " + board.result())

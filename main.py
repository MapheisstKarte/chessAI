import time

import chess

import AI
from test import find_best_move

if __name__ == "__main__":
    board = chess.Board()
    move_finder = AI.MoveFinder(board=board)
    print(board)

    while not board.is_game_over():

        if board.turn:

            player_move = input()
            board.push_san(player_move)
            timeStart = time.time()
            print(board)

        elif not board.turn:
            print("-------------------------------")
            move_result = find_best_move(board)
            # move_result = move_finder.findBestMoveNegaMax(board=board)
            print(move_result)
            board.push(move_result.move)
            evaluation = move_result.score
            # evaluation = move_result.maxScore
            print("Evaluation " + str(evaluation))
            print("AI Move: " + chess.Move.__str__(move_result.move))
            print(board)
            print("-------------------------------")

    else:
        print("Game Over: " + board.result())

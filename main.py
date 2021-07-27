import time
from concurrent.futures import ProcessPoolExecutor

import chess

from search import find_best_move

if __name__ == "__main__":
    pool = ProcessPoolExecutor()
    board = chess.Board()
    print(board)
    while not board.is_game_over():

        if board.turn:

            while True:
                try:
                    player_move = input()
                    if player_move == "pop":
                        if len(board.move_stack) >= 2:
                            board.pop()
                            board.pop()
                    else:
                        board.push_san(player_move)
                    break
                except:
                    print("move not in legal moves")
            timeStart = time.time()
            print(board)

        elif not board.turn:
            print("-------------------------------")
            move_result = find_best_move(board, pool)
            # move_result = move_finder.findBestMoveNegaMax(board)
            print(move_result)
            board.push(move_result.move)
            evaluation = move_result.score
            print("Evaluation " + str(evaluation * 10))
            print("AI Move: " + chess.Move.__str__(move_result.move))
            print(board)
            print("-------------------------------")

    else:
        print("Game Over: " + board.result())

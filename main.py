import time

import chess

from test import find_best_move

board = chess.Board()


print(board)

while not board.is_game_over():

    if board.turn:

        player_move = input()
        board.push_san(player_move)
        timeStart = time.time()
        print(board)

    elif not board.turn:
        print("-------------------------------")
        if __name__ == '__main__':
            move_result = find_best_move(board)
            board.push(move_result.move)
            evaluation = move_result.score
            print("Evaluation " + str(evaluation))
            print("AI Move: " + chess.Move.__str__(move_result.move))
            print(board)
            print("-------------------------------")

else:
    print("Game Over: " + board.result())

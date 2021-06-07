import random
import chess
import numpy
import numpy as np
import Evaluation

board = chess.Board()
evaluation = Evaluation.evaluate(board)
print(evaluation)

moves = []
while True:
    PlayerMove = input()
    board.push_san(PlayerMove)
    print(board)
    if not board.turn:
        for move in board.legal_moves:
            moves.append(move)
        AIMove = random.choice(moves)
        board.push(AIMove)
        print(board)

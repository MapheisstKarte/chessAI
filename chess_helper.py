from typing import Callable

import chess

EvaluationFunction = Callable[[chess.Board], float]


def invert_board(board: chess.Board):
    board.turn = 0 if board.turn == 1 else 1


def make_null_move(board: chess.Board, evaluation: EvaluationFunction):
    max_score: float = -999
    best_move: chess.Move = None
    invert_board(board)
    for move in board.legal_moves:
        board.push(move)
        board_rating = evaluation(board)
        if best_move is None or board_rating > max_score:
            max_score = board_rating
            best_move = move
        board.pop()
    board.push(best_move)


def undo_null_move(board: chess.Board):
    board.pop()
    invert_board(board)

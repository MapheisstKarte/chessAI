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

#
#
# def make_null_move(board: chess.Board, first_move: str, second_move: str) -> chess.Board:
#     board.push_san(first_move)
#     board = invert_player(board)
#     board.push_san(second_move)
#     return board
#
#
# @dataclasses.dataclass
# class RatedMove:
#     move_san: str
#     score: float
#
#
# def find_best_move(move_board: chess.Board, rate_board: Callable[[chess.Board], float]) -> RatedMove:
#     best_move: str = None
#     rating: float = -math.inf
#     for move in move_board.legal_moves:
#         move_board.push(move)
#         rating = rate_board(move_board)
#         move_board.pop()
#         if best_move is None or rating > rating:
#             best_move = move.uci()
#             rating = rating
#     return RatedMove(move_san=best_move, score=rating)
#
#
# def full_null_move(board: chess.Board, rate_board: Callable[[chess.Board], float]) -> chess.Board:
#     board = invert_player(board)
#     best_first_move = find_best_move(board, rate_board)
#     board.push_san(best_first_move.move_san)
#     best_second_move = find_best_move(board, rate_board)
#     board.pop()
#     return make_null_move(board, best_first_move.move_san, best_second_move.move_san)
#
#
# def invert_player(board: chess.Board) -> chess.Board:
#     board.turn = 0 if board.turn == 1 else 1
#     return board

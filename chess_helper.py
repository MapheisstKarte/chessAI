import dataclasses
import math
from typing import Callable

import chess


def make_null_move(board: chess.Board, first_move: str, second_move: str) -> chess.Board:
    board.push_san(first_move)
    board.turn = 0 if board.turn == 1 else 1
    board.push_san(second_move)
    return board


@dataclasses.dataclass
class RatedMove:
    move_san: str
    score: float


def take_best_move(move_board: chess.Board, rate_board: Callable[[chess.Board], float]) -> RatedMove:
    best_move: str = None
    rating: float = -math.inf
    for move in move_board.legal_moves:
        move_board.push(move)
        rating = rate_board(move_board)
        move_board.pop()
        if best_move is None or rating > rating:
            best_move = move.uci()
            rating = rating
    return RatedMove(move_san=best_move, score=rating)


def full_null_move(board: chess.Board, rate_board: Callable[[chess.Board], float]) -> chess.Board:
    best_first_move = take_best_move(board, rate_board)
    board.push_san(best_first_move.move_san)
    board.turn = 0 if board.turn == 1 else 1
    best_second_move = take_best_move(board, rate_board)
    board.pop()
    return make_null_move(board, best_first_move.move_san, best_second_move.move_san)

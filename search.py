import math
import time
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from typing import Optional

import chess

import ValueTables as vt
from chess_helper import make_null_move, undo_null_move


def evaluate(board: chess.Board):
    evaluation = 0
    if board.is_stalemate():
        evaluation = 0
        return evaluation
    if board.turn:  # if it's white's turn
        if board.is_checkmate():
            evaluation = math.inf
            return evaluation
        if board.is_check():
            evaluation += 0.1
    else:  # if it's blacks turn
        if board.is_checkmate():
            evaluation = -math.inf
            return evaluation
        if board.is_check():
            evaluation -= 0.1

    for fieldnumber in range(64):
        piece = board.piece_at(fieldnumber)
        if piece is not None:
            evaluation += evaluate_square(board, fieldnumber, piece)
    return evaluation


def evaluate_square(board: chess.Board, square: int, piece: chess.Piece) -> float:
    evaluation = 0
    color = piece.color
    piece_type = piece.piece_type
    if color:
        if piece_type == 1:
            evaluation += 10 + (vt.Heuristics.WHITE_PAWN_TABLE.flatten()[square] / 2)
        elif piece_type == 2:
            evaluation += 30 + (vt.Heuristics.KNIGHT_TABLE.flatten()[square] / 2)
        elif piece_type == 3:
            evaluation += 32.5 + (vt.Heuristics.BISHOP_TABLE.flatten()[square] / 2)
        elif piece_type == 4:
            evaluation += 50 + (vt.Heuristics.ROOK_TABLE.flatten()[square] / 2)
        elif piece_type == 5:
            evaluation += 90 + (vt.Heuristics.QUEEN_TABLE.flatten()[square] / 2)
        elif piece_type == 6:
            evaluation += 999 + (vt.Heuristics.KING_TABLE.flatten()[square] / 2)

    elif not color:
        if piece_type == 1:
            evaluation -= 10 + (vt.Heuristics.BLACK_PAWN_TABLE.flatten()[square] / 2)
        elif piece_type == 2:
            evaluation -= 30 + (vt.Heuristics.KNIGHT_TABLE.flatten()[square] / 2)
        elif piece_type == 3:
            evaluation -= 35 + (vt.Heuristics.BISHOP_TABLE.flatten()[square] / 2)
        elif piece_type == 4:
            evaluation -= 50 + (vt.Heuristics.ROOK_TABLE.flatten()[square] / 2)
        elif piece_type == 5:
            evaluation -= 90 + (vt.Heuristics.QUEEN_TABLE.flatten()[square] / 2)
        elif piece_type == 6:
            evaluation -= 999 + (vt.Heuristics.KING_TABLE.flatten()[square] / 2)
    return evaluation / 100


def order_moves(board: chess.Board):
    first_moves = []
    other = []

    for move in board.legal_moves:
        if board.gives_check(move) or board.is_capture(move):
            first_moves.append(move)
        else:
            other.append(move)
    return first_moves + other


@dataclass
class MoveResult:
    move: Optional[chess.Move]
    score: float


@dataclass
class BoardMove:
    move: chess.Move
    board: chess.Board


def find_best_move(board: chess.Board, pool: ProcessPoolExecutor) -> MoveResult:
    time_start = time.time()
    max_score = -999
    next_move = None

    next_boards = []
    for move in order_moves(board):
        next_boards.append(move)

    board_moves = [BoardMove(move=m, board=board.copy()) for m in order_moves(board)]

    results = pool.map(minimax_finder, board_moves)

    for result in results:
        if result.score > max_score:
            max_score = result.score
            next_move = result.move
    print("Time: " + str(time.time() - time_start))
    return MoveResult(move=next_move, score=max_score)


def minimax_finder(board_move: BoardMove) -> MoveResult:
    board = board_move.board
    result = minimax(board, board_move.move, 1 if board.turn else -1, 5, -999, 999)
    return MoveResult(move=board_move.move, score=result)


def minimax(board: chess.Board, move: chess.Move, player: int, depth: int, alpha: int, beta: int) -> float:
    if depth == 0:
        return evaluate(board)
    score = -999
    board.push(move)
    curr = -minimax_all_moves(board, -player, depth - 1, -beta, -alpha)
    if curr > score:
        score = curr
    if score > alpha:
        alpha = score
    board.pop()
    if alpha >= beta:
        return alpha
    return score


def minimax_all_moves(board: chess.Board, player: int, depth: int, alpha: int, beta: int) -> float:
    R = 2
    if depth <= 0:
        return evaluate(board) * player
    score = -999

    if not board.is_check() and depth >= 3:
        make_null_move(board, evaluate)
        rating_after_null_move = -minimax_all_moves(board, -player, -beta + 1, -beta, depth - 1 - R)
        undo_null_move(board)
        if rating_after_null_move >= beta:
            return beta

    for move in order_moves(board):
        board.push(move)
        curr = -minimax_all_moves(board, -player, depth - 1, -beta, -alpha)

        if curr > score:
            score = curr
        if score > alpha:
            alpha = score
        board.pop()
        if alpha >= beta:
            return alpha
    return score

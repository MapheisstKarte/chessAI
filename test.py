import math
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import Optional

import chess

import ValueTables as vt

# pool = ProcessPoolExecutor()
pool = ThreadPoolExecutor()


def evaluate(board: chess.Board):
    evaluation = 0
    rank = 0
    while rank < 8:
        file = 0
        while file < 8:
            square = chess.square(file, rank)
            piece = board.piece_at(square)
            if piece is not None:
                color = piece.color
                piece_type = piece.piece_type
                if color:
                    if piece_type == 1:
                        evaluation += 10 + (vt.Heuristics.WHITE_PAWN_TABLE[file, rank] / 10)
                    elif piece_type == 2:
                        evaluation += 30 + (vt.Heuristics.KNIGHT_TABLE[file, rank] / 10)
                    elif piece_type == 3:
                        evaluation += 32.5 + (vt.Heuristics.BISHOP_TABLE[file, rank] / 10)
                    elif piece_type == 4:
                        evaluation += 50 + (vt.Heuristics.ROOK_TABLE[file, rank] / 10)
                    elif piece_type == 5:
                        evaluation += 90 + (vt.Heuristics.QUEEN_TABLE[file, rank] / 10)
                    elif piece_type == 6:
                        evaluation += 999 + (vt.Heuristics.KING_TABLE[file, rank] / 10)

                elif not color:
                    if piece_type == 1:
                        evaluation -= 10 + (vt.Heuristics.BLACK_PAWN_TABLE[file, rank] / 10)
                    elif piece_type == 2:
                        evaluation -= 30 + (vt.Heuristics.KNIGHT_TABLE[file, rank] / 10)
                    elif piece_type == 3:
                        evaluation -= 35 + (vt.Heuristics.BISHOP_TABLE[file, rank] / 10)
                    elif piece_type == 4:
                        evaluation -= 50 + (vt.Heuristics.ROOK_TABLE[file, rank] / 10)
                    elif piece_type == 5:
                        evaluation -= 90 + (vt.Heuristics.QUEEN_TABLE[file, rank] / 10)
                    elif piece_type == 6:
                        evaluation -= 999 + (vt.Heuristics.KING_TABLE[file, rank] / 10)

            file = file + 1
        rank = rank + 1
    if board.is_stalemate():
        evaluation = 0

        if board.turn:  # if it's white's turn
            if board.is_checkmate():
                evaluation = math.inf
            if board.is_check():
                evaluation += 0.1

        else:  # if it's blacks turn
            if board.is_checkmate():
                evaluation = -math.inf
            if board.is_check():
                evaluation -= 0.1

    return evaluation / 10


def order_moves(board: chess.Board):
    first_moves = []
    other = []

    for move in board.legal_moves:
        if board.gives_check(move) or board.is_capture(move):
            first_moves.append(move)
        else:
            other.append(move)
    return first_moves + other


@dataclass()
class MoveResult:
    move: Optional[chess.Move]
    score: float


@dataclass()
class BoardMove:
    move: chess.Move
    board: chess.Board


def find_best_move(board: chess.Board) -> MoveResult:
    max_score = -math.inf
    next_move = None

    board_moves = [BoardMove(move=m, board=board.copy()) for m in order_moves(board)]

    with pool as executor:
        results = executor.map(minimax_finder, board_moves)

    for result in results:
        if result.score > max_score:
            max_score = result.score
            next_move = result.move

    return MoveResult(move=next_move, score=max_score)


def minimax_finder(board_move: BoardMove) -> MoveResult:
    result = minimax(board_move.board, board_move.move, 0, -999, 999, 1 if board_move.board.turn else -1)
    return MoveResult(move=result.move, score=result.score)


def minimax(board: chess.Board, board_move, depth: int, alpha: int, beta: int, turn_multiplier: int) -> MoveResult:
    max_score = -999
    next_move = board_move
    if depth == 3:
        return MoveResult(move=next_move, score=turn_multiplier * evaluate(board))

    for move in order_moves(board):
        board.push(move)
        score = -minimax(board, next_move, depth + 1, -beta, -alpha, -turn_multiplier).score
        if score > max_score:
            max_score = score

        board.pop()
        if max_score > alpha:  # pruning
            alpha = max_score
        if alpha >= beta:
            break

    return MoveResult(move=next_move, score=max_score)

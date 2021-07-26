import math
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import Optional

import chess

import ValueTables as vt

# pool = ProcessPoolExecutor()
pool = ThreadPoolExecutor(max_workers=1)


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


@dataclass
class MoveResult:
    move: Optional[chess.Move]
    score: float


@dataclass
class BoardMove:
    move: chess.Move
    board: chess.Board


def find_best_move(board: chess.Board) -> MoveResult:
    max_score = -math.inf
    next_move = None

    next_boards = []
    for move in order_moves(board):
        next_boards.append(move)

    board_moves = [BoardMove(move=m, board=board.copy()) for m in order_moves(board)]

    # with pool as executor:
    results = pool.map(minimax_finder, board_moves)

    for result in results:
        if result.score > max_score:
            max_score = result.score
            next_move = result.move

    return MoveResult(move=next_move, score=max_score)


def minimax_finder(board_move: BoardMove) -> MoveResult:
    result = minimax(board_move.board, 1 if board_move.board.turn else -1, 3, -999, 999)
    print(result)
    return MoveResult(move=board_move.move, score=result)


def minimax(board: chess.Board, player: int, depth: int, alpha: int, beta: int) -> float:
    if depth == 0:
        return evaluate(board) * player
    score = -math.inf
    moves = order_moves(board)
    for move in moves:
        board.push(move)
        curr = -minimax(board, -player, depth - 1, -beta, -alpha)
        if curr > score:
            score = curr
        if score > alpha:
            alpha = score
        board.pop()
        if alpha >= beta:
            return alpha
    return score

# def minimax(board: chess.Board, depth: int, alpha: int, beta: int, turn_multiplier: int, best_score_so_far: float = -999) -> float:
#     if depth == 0:
#         return evaluate(board) * turn_multiplier
#     else:
#         best_score = best_score_so_far
#         for move in order_moves(board):
#             board.push(move)
#             score = minimax(board, depth-1, -beta, -alpha, -turn_multiplier, best_score)
#             if score > best_score_so_far:
#                 best_score = max(best_score_so_far, score)
#             board.pop()
#             if best_score


#
# def minimax(board: chess.Board, board_move: chess.Move, depth: int, alpha: int, beta: int, turn_multiplier: int) -> float:
#     max_score = -999
#     next_move = board_move
#     if depth == 0:
#         evaluation = turn_multiplier * float(evaluate(board))
#         return float(evaluation)
#     else:
#         for move in order_moves(board):
#             board.push(move)
#             score = -minimax(board, next_move, depth - 1, -beta, -alpha, -turn_multiplier)
#             if score > max_score:
#                 max_score = score
#             board.pop()
#             if max_score > alpha:  # pruning
#                 alpha = max_score
#             if alpha >= beta:
#                 break
#         return float(max_score)

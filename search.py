import math
import operator
import time
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from typing import Optional

import chess

import ValueTables as vt
from chess_helper import make_null_move, undo_null_move


@dataclass
class MoveResult:
    move: Optional[chess.Move]
    score: float


@dataclass
class BoardMove:
    move: chess.Move
    board: chess.Board


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
    if board.is_variant_draw():
        evaluation = 0
        return evaluation

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


def order_moves(board: chess.Board, legal_moves: list) -> list:
    results = []
    moves = []
    for move in legal_moves:
        results.append(dict({"move": move, "score": move_score_guess(board, move)}))
    results.sort(reverse=True, key=operator.itemgetter("score"))
    for result in results:
        moves.append(result.get("move"))
    return moves


def move_score_guess(board: chess.Board, move):
    score_guess = 0

    def get_piece_value(chess_piece: chess.Piece):
        piece_value = 0
        if piece.piece_type == 1:
            piece_value = 10
        if piece.piece_type == 2:
            piece_value = 30
        if piece.piece_type == 3:
            piece_value = 35
        if piece.piece_type == 4:
            piece_value = 50
        if piece.piece_type == 5:
            piece_value = 90
        return piece_value

    if board.is_capture(move):
        piece = board.piece_at(move.from_square)
        taken_piece = board.piece_at(move.to_square)
        if piece.piece_type is not None:
            score_guess = 10 * get_piece_value(taken_piece) - get_piece_value(piece)
        else:
            score_guess = 0
    elif board.gives_check(move):
        score_guess = 25
    else:
        score_guess = 0

    return score_guess


def find_best_move(board: chess.Board, pool: ProcessPoolExecutor) -> MoveResult:
    time_start = time.time()
    board_moves = [BoardMove(move=m, board=board.copy()) for m in order_moves(board, list(board.legal_moves))]

    results = pool.map(minimax_finder, board_moves)
    new_list = []
    for result in results:
        new_list.append(dict({"move": result.move, "score": result.score}))
    new_list.sort(reverse=True, key=operator.itemgetter("score"))
    move = new_list[0].get("move")
    score = new_list[0].get("score")
    print("Time: " + str(time.time() - time_start))
    return MoveResult(move=move, score=score)


def minimax_finder(board_move: BoardMove) -> MoveResult:
    board = board_move.board
    result = minimax(board, board_move.move, 1 if board.turn else -1, 3, -999, 999)
    return MoveResult(move=board_move.move, score=result)


def minimax(board: chess.Board, move: chess.Move, player: int, depth: int, alpha: float, beta: float) -> float:
    if depth == 0:
        return evaluate(board)
    evalution = -math.inf
    board.push(move)
    evaluation = -minimax_all_moves(board, -player, depth - 1, -beta, -alpha)
    board.pop()
    if evaluation >= beta:
        return beta
    alpha = max(alpha, evaluation)
    return alpha


def minimax_all_moves(board: chess.Board, player: int, depth: int, alpha: float, beta: float) -> float:
    if depth <= 0:
        evaluation = evaluate(board) * player
        # return evaluation
        deepened_score = minimax_every_capture_and_check(board, player, -beta, -alpha)
        return max(evaluation, deepened_score)

    if not board.is_check() and depth >= 3:
        make_null_move(board, evaluate)
        rating_after_null_move = -minimax_all_moves(board, -player, depth - 2, -beta, -beta + 1)
        undo_null_move(board)
        if rating_after_null_move >= beta:
            return beta

    evaluation = -math.inf

    for move in order_moves(board, list(board.legal_moves)):
        board.push(move)
        evaluation = -minimax_all_moves(board, -player, depth - 1, -beta, -alpha)
        board.pop()
        if evaluation >= beta:
            return beta
        alpha = max(alpha, evaluation)
    return alpha


def minimax_every_capture_and_check(board: chess.Board, player: int, alpha: float, beta: float):
    def generate_capture_and_check_moves(board: chess.Board):
        moves = []
        for move in board.legal_moves:
            if board.is_capture(move) or board.gives_check(move):
                moves.append(move)
        return moves

    if len(generate_capture_and_check_moves(board=board)):
        return evaluate(board) * player

    for move in order_moves(board, generate_capture_and_check_moves(board)):
        board.push(move)
        evaluation = -minimax_every_capture_and_check(board, -player, -beta, -alpha)
        board.pop()
        if evaluation >= beta:
            return beta
        alpha = max(alpha, evaluation)

    return alpha

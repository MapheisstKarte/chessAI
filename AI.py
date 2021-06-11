from dataclasses import dataclass
from typing import Optional

import chess

import ValueTables as vt

DEPTH = 5


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
                        evaluation += 40 + (vt.Heuristics.BISHOP_TABLE[file, rank] / 10)
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
                        evaluation -= 40 + (vt.Heuristics.BISHOP_TABLE[file, rank] / 10)
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
                evaluation = 999
            if board.is_check():
                evaluation += 0.1
        else:  # if it's blacks turn
            if board.is_checkmate():
                evaluation = -999
            if board.is_check():
                evaluation -= 0.1

    return evaluation / 10


def orderMoves(board: chess.Board):
    firstMoves = []
    other = []

    for move in board.legal_moves:
        if board.gives_check(move) or board.is_capture(move):
            firstMoves.append(move)
        else:
            other.append(move)
    return firstMoves + other


# helping function

@dataclass
class MoveResult:
    move: Optional[chess.Move]
    maxScore: float


class MoveFinder:

    def __init__(self, board: chess.Board, counter: int = 0):
        self.board = board
        self.counter = counter

    def findBestMoveNegaMax(self, board: chess.Board):
        self.counter = 0
        nextMove = self.findMoveNegaMax(board, DEPTH, -999, 999, 1 if board.turn else - 1)
        print("Positions calculated: " + str(self.counter))
        return nextMove.move

    # negamax algorithm with Alpha-Beta pruning

    def findMoveNegaMax(self, board: chess.Board, depth, alpha, beta, turnMultiplier) -> MoveResult:
        self.counter += 1
        maxScore = -999
        nextMove = None

        if depth == 0:
            return MoveResult(move=nextMove, maxScore=turnMultiplier * evaluate(board))

        for move in orderMoves(board):
            board.push(move)
            score = -self.findMoveNegaMax(board, depth - 1, -beta, -alpha, -turnMultiplier).maxScore
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            board.pop()
            if maxScore > alpha:  # pruning
                alpha = maxScore
            if alpha >= beta:
                break

        return MoveResult(move=nextMove, maxScore=maxScore)

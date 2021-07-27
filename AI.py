import time
from dataclasses import dataclass
from typing import Optional

import chess

from search import evaluate

DEPTH = 6


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
        move_result = self.findMoveNegaMax(board, DEPTH, -999, 999, 1 if board.turn else - 1)
        print("Positions calculated: " + str(self.counter))
        print("Time: " + str(time.perf_counter()))
        return move_result

    # negamax algorithm with Alpha-Beta pruning

    def findMoveNegaMax(self, board: chess.Board, depth, alpha, beta, turnMultiplier) -> MoveResult:
        maxScore = -999
        nextMove = None
        R = 2

        if depth <= 0 or board.is_checkmate():
            return MoveResult(move=nextMove, maxScore=turnMultiplier * evaluate(board))

        # if not board.is_check() and depth >= 3:
        #    make_null_move(board, evaluate)
        #    rating_after_null_move = -self.findMoveNegaMax(board, depth-1 - R, -beta, -beta + 1, -turnMultiplier).maxScore
        #    undo_null_move(board)
        #    if rating_after_null_move >= beta:
        #        print("pruned")
        #        return MoveResult(move=nextMove, maxScore=beta)

        for move in orderMoves(board):
            board.push(move)
            self.counter += 1
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

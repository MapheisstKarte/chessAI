import numpy as np


class Heuristics:

    WHITE_PAWN_TABLE = np.array([
        [0, 0, 0, 0, 0, 0, 0, 0],
        [10, 10, 10, 10, 10, 10, 10, 10],
        [10, 10, 15, 20, 20, 15, 10, 10],
        [10, 10, 15, 25, 25, 15, 10, 10],
        [15, 10, 10, 20, 20, 10, 10, 15],
        [10, 10, 15, 15, 15, 15, 10, 10],
        [60, 50, 50, 50, 50, 50, 50, 60],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ])

    BLACK_PAWN_TABLE = np.array([
        [0, 0, 0, 0, 0, 0, 0, 0],
        [60, 50, 50, 50, 50, 50, 50, 60],
        [10, 10, 15, 15, 15, 15, 10, 10],
        [15, 10, 10, 20, 20, 10, 10, 15],
        [10, 10, 15, 25, 25, 15, 10, 10],
        [10, 10, 15, 20, 20, 15, 10, 10],
        [10, 10, 10, 10, 10, 10, 10, 10],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ])

    KNIGHT_TABLE = np.array([
        [10, 20, 20, 20, 20, 20, 20, 10],
        [15, 20, 25, 30, 30, 25, 20, 15],
        [15, 25, 35, 30, 30, 35, 25, 15],
        [15, 25, 40, 40, 40, 40, 25, 15],
        [15, 25, 40, 40, 40, 40, 25, 15],
        [15, 25, 35, 30, 30, 35, 25, 15],
        [15, 20, 25, 30, 30, 25, 20, 15],
        [10, 20, 20, 20, 20, 20, 20, 10]
    ])

    BISHOP_TABLE = np.array([
        [15, 15, 15, 15, 15, 15, 15, 15],
        [20, 30, 30, 30, 30, 30, 30, 20],
        [25, 30, 35, 35, 35, 35, 30, 25],
        [30, 30, 35, 40, 40, 35, 30, 30],
        [30, 30, 35, 40, 40, 35, 30, 30],
        [25, 30, 35, 35, 35, 35, 30, 25],
        [20, 30, 30, 30, 30, 30, 30, 20],
        [15, 15, 15, 15, 15, 15, 15, 15]
    ])

    ROOK_TABLE = np.array([
        [50, 50, 50, 50, 50, 50, 50, 50],
        [50, 40, 40, 40, 40, 40, 40, 50],
        [50, 35, 35, 35, 35, 35, 35, 50],
        [50, 35, 20, 15, 15, 20, 35, 50],
        [50, 35, 20, 15, 15, 20, 35, 50],
        [50, 35, 35, 35, 35, 35, 35, 50],
        [50, 40, 40, 40, 40, 40, 40, 50],
        [50, 50, 50, 50, 50, 50, 50, 50]
    ])

    QUEEN_TABLE = np.array([
        [30, 35, 35, 35, 35, 35, 35, 30],
        [35, 40, 40, 40, 40, 40, 40, 35],
        [35, 40, 45, 45, 45, 45, 40, 35],
        [35, 40, 45, 50, 50, 45, 40, 35],
        [35, 40, 45, 50, 50, 45, 40, 35],
        [35, 40, 45, 45, 45, 45, 40, 35],
        [35, 40, 40, 40, 40, 40, 40, 35],
        [30, 35, 35, 35, 35, 35, 35, 30]
    ])

    KING_TABLE = np.array([
        [10, 10, 10, 10, 10, 10, 10, 10],
        [10, 10, 10, 5, 5, 10, 10, 10],
        [5, 0, 0, 0, 0, 0, 0, 5],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [5, 0, 0, 0, 0, 0, 0, 5],
        [10, 10, 10, 5, 5, 10, 10, 10],
        [10, 15, 5, 5, 5, 5, 15, 10],
    ])

import numpy as np


class Heuristics:
    WHITE_PAWN_TABLE = np.array([

        [0, 0, 0, 0, 0, 0, 0, 0],
        [10, 10, 5, -5, -5, 5, 10, 10],
        [10, 10, 15, 15, 15, 15, 10, 10],
        [10, 10, 15, 25, 25, 15, 10, 10],
        [15, 10, 10, 20, 20, 10, 10, 15],
        [10, 10, 15, 15, 15, 15, 10, 10],
        [60, 50, 50, 50, 50, 50, 50, 60],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ], dtype=np.float)

    BLACK_PAWN_TABLE = np.array([

        [0, 0, 0, 0, 0, 0, 0, 0],
        [60, 50, 50, 50, 50, 50, 50, 60],
        [10, 10, 15, 15, 15, 15, 10, 10],
        [15, 10, 10, 20, 20, 10, 10, 15],
        [10, 10, 15, 25, 25, 15, 10, 10],
        [10, 10, 15, 15, 15, 15, 10, 10],
        [10, 10, 5, -5, -5, 5, 10, 10],
        [0, 0, 0, 0, 0, 0, 0, 0]

    ], dtype=np.float)

    KNIGHT_TABLE = np.array([

        [-5, -5, -5, -5, -5, -5, -5, -5],
        [-5, 5, 5, 5, 5, 5, 5, -5],
        [-5, 5, 15, 15, 15, 15, 5, -5],
        [-5, 5, 15, 15, 15, 15, 5, -5],
        [-5, 5, 15, 15, 15, 15, 5, -5],
        [-5, 5, 15, 15, 15, 15, 5, -5],
        [-5, 5, 5, 5, 5, 5, 5, -5],
        [-5, -5, -5, -5, -5, -5, -5, -5]

    ], dtype=np.float)

    BISHOP_TABLE = np.array([

        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 5, 5, 5, 5, 5, 5, 0],
        [0, 5, 10, 10, 10, 10, 5, 0],
        [0, 5, 10, 15, 15, 10, 5, 0],
        [0, 5, 10, 15, 15, 10, 5, 0],
        [0, 5, 10, 10, 10, 10, 5, 0],
        [0, 5, 5, 5, 5, 5, 5, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ], dtype=np.float)

    ROOK_TABLE = np.array([
        [10, 10, 10, 10, 10, 10, 10, 10],
        [10, 5, 5, 5, 5, 5, 5, 10],
        [10, 5, 0, 0, 0, 0, 5, 10],
        [10, 5, 0, 0, 0, 0, 5, 10],
        [10, 5, 0, 0, 0, 0, 5, 10],
        [10, 5, 0, 0, 0, 0, 5, 10],
        [10, 5, 5, 5, 5, 5, 5, 10],
        [10, 10, 10, 10, 10, 10, 10, 10]
    ], dtype=np.float)

    QUEEN_TABLE = np.array([
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 5, 5, 5, 5, 5, 5, 0],
        [0, 5, 10, 10, 10, 10, 5, 0],
        [0, 5, 10, 15, 15, 10, 5, 0],
        [0, 5, 10, 15, 15, 10, 5, 0],
        [0, 5, 10, 10, 10, 10, 5, 0],
        [0, 5, 5, 5, 5, 5, 5, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ], dtype=np.float)

    KING_TABLE = np.array([
        [10, 15, 5, 5, 5, 5, 15, 10],
        [10, 10, 10, 5, 5, 10, 10, 10],
        [5, 0, 0, 0, 0, 0, 0, 5],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [5, 0, 0, 0, 0, 0, 0, 5],
        [10, 10, 10, 5, 5, 10, 10, 10],
        [10, 15, 5, 5, 5, 5, 15, 10],
    ], dtype=np.float)

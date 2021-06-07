import chess
import ValueTables as vt

def evaluate(board):
    evaluation = 0
    file = 1
    while file < 8:
        rank = 1
        while rank < 8:
            square = chess.square(rank, file)
            piece = board.piece_at(square)
            piece_color = board.color
            board.color_at(square)
            if piece.color:
                if piece.piece_type == 1:
                    evaluation += vt.Heuristics.PAWN_TABLE[(rank * file)]
                elif piece.piece_type == 3:
                    evaluation += vt.Heuristics.BISHOP_TABLE[(rank * file)]
                elif piece.piece_type == 2:
                    evaluation += vt.Heuristics.KNIGHT_TABLE[(rank * file)]
                elif piece.piece_type == 4:
                    evaluation += vt.Heuristics.ROOK_TABLE[(rank * file)]
                elif piece.piece_type == 5:
                    evaluation += vt.Heuristics.QUEEN_TABLE[(rank * file)]
            elif not piece.color:
                if piece.piece_type == 1:
                    evaluation -= vt.Heuristics.PAWN_TABLE[(rank * file)]
                elif piece.piece_type == 3:
                    evaluation -= vt.Heuristics.BISHOP_TABLE[(rank * file)]
                elif piece.piece_type == 2:
                    evaluation -= vt.Heuristics.KNIGHT_TABLE[(rank * file)]
                elif piece.piece_type == 4:
                    evaluation -= vt.Heuristics.ROOK_TABLE[(rank * file)]
                elif piece.piece_type == 5:
                    evaluation -= vt.Heuristics.QUEEN_TABLE[(rank * file)]
            rank = rank + 1
        file = file + 1
    return evaluation
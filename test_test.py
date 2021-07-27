from unittest import TestCase

import chess

from search import find_best_move, evaluate


class Test(TestCase):
    def test_find_best_move_base_board(self):
        board = chess.Board()
        fen_before = board.fen()

        result = find_best_move(board)
        fen_after = board.fen()

        self.assertEqual(fen_before, fen_after)
        self.assertTrue(result.move in board.legal_moves)
        print(result)

    def test_find_best_move_for_board_after_e2e4(self):
        board = chess.Board()
        board.push_san("e2e4")
        fen_before = board.fen()

        result = find_best_move(board)
        fen_after = board.fen()

        self.assertEqual(fen_before, fen_after)
        self.assertTrue(result.move in board.legal_moves)
        print(result)


class TestEvaluate(TestCase):
    def test_plain_board(self):
        board = chess.Board()
        self.assertEqual(evaluate(board), -0.5)

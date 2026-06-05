import unittest
from engine import ChessGame


class TestChessGame(unittest.TestCase):
    #establish TestCase hook method (run before every test runs)
    def setUp(self):
        self.game = ChessGame()

    def test_initial_turn_is_white(self):
        self.assertEqual(self.game.turn, "white")

    def test_white_pawn_move_forward_one(self):
        success, message = self.game.move_piece('e2', 'e3')
        self.assertTrue(success)
        self.assertEqual(self.game.board[5][4], 'P')
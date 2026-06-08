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

    def test_white_pawn_move_forward_two_from_start(self):
        success, message = self.game.move_piece("e3", "e4")
        self.assertFalse(success)
        self.assertEqual(message, "No piece at starting square.")

    def test_cannot_move_from_empty_square(self):
        success, message = self.game.move_piece("e3", "e4")
        self.assertFalse(success)
        self.assertEqual(message, "No piece at starting square.")
    
    def test_cannot_move_black_first(self):
        success, message = self.game.move_piece("e7", "e5")
        self.assertFalse(success)
        self.assertEqual(message, "It is white's turn.")

    
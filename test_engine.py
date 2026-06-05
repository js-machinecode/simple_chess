import unittest
from engine import ChessGame


class TestChessGame(unittest.TestCase):
    #establish TestCase hook method (run before every test runs)
    def setUp(self):
        self.game = ChessGame()

    def test_initial_turn_is_white(self):
        self.assertEqual(self.game.turn, "white")
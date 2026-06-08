import unittest
from engine import ChessGame


class TestChessGame(unittest.TestCase):
    #establish TestCase hook method (run before every test runs)
    def setUp(self):
        self.game = ChessGame()

    # -------------------------
    # Board setup tests
    # -------------------------

    def test_initial_turn_is_white(self):
        self.assertEqual(self.game.turn, "white")

    def test_board_has_8_rows(self):
        self.assertEqual(len(self.game.board), 8)

    def test_each_board_row_has_8_columns(self):
        for row in self.game.board:
            self.assertEqual(len(row), 8)

    def test_white_king_starts_on_e1(self):
        self.assertEqual(self.game.board[7][4], 'K')

    def test_black_king_starts_on_e8(self):
        self.assertEqual(self.game.board[0][4], 'k')

    # -------------------------
    # Square conversion tests
    # -------------------------

    def test_square_to_index_e2(self):
        self.assertEqual(self.game.square_to_index("e2"), (6, 4))

    def test_square_to_index_a8(self):
        self.assertEqual(self.game.square_to_index("a8"), (0, 0))

    def test_square_to_index_h1(self):
        self.assertEqual(self.game.square_to_index("h1"), (7, 7))

    def test_invalid_square_raises_error(self):
        with self.assertRaises(ValueError):
            self.game.square_to_index("z9")

    # -------------------------
    # Basic move validation
    # -------------------------

    def test_cannot_move_from_empty_square(self):
        success, message = self.game.move_piece("e3", "e4")

        self.assertFalse(success)
        self.assertEqual(message, "No piece at starting square.")

    def test_cannot_move_black_piece_on_white_turn(self):
        success, message = self.game.move_piece("e7", "e5")

        self.assertFalse(success)
        self.assertEqual(message, "It is white's turn.")

    def test_turn_switches_after_successful_move(self):
        success, message = self.game.move_piece("e2", "e4")

        self.assertTrue(success)
        self.assertEqual(self.game.turn, "black")

    def test_cannot_capture_own_piece(self):
        success, message = self.game.move_piece("e1", "e2")

        self.assertFalse(success)
        self.assertEqual(message, "You cannot capture your own piece.")


    # -------------------------
    # Pawn tests
    # -------------------------

    def test_white_pawn_can_move_forward_one(self):
        success, message = self.game.move_piece("e2", "e3")

        self.assertTrue(success)
        self.assertEqual(self.game.board[5][4], "P")
        self.assertEqual(self.game.board[6][4], ".")

    def test_white_pawn_can_move_forward_two_from_start(self):
        success, message = self.game.move_piece("e2", "e4")

        self.assertTrue(success)
        self.assertEqual(self.game.board[4][4], "P")
        self.assertEqual(self.game.board[6][4], ".")

    def test_white_pawn_cannot_move_forward_three(self):
        success, message = self.game.move_piece("e2", "e5")

        self.assertFalse(success)
        self.assertEqual(message, "Invalid move for that piece.")

    def test_white_pawn_cannot_move_sideways(self):
        success, message = self.game.move_piece("e2", "f2")

        self.assertFalse(success)
        self.assertEqual(message, "You cannot capture your own piece.")

    def test_white_pawn_cannot_move_backward(self):
        # Put a white pawn in the middle of the board manually.
        self.game.board[4][4] = "P"
        self.game.board[6][4] = "."

        success, message = self.game.move_piece("e4", "e3")

        self.assertFalse(success)
        self.assertEqual(message, "Invalid move for that piece.")

    def test_white_pawn_cannot_move_two_after_leaving_starting_row(self):
        self.game.board[4][4] = "P"
        self.game.board[6][4] = "."

        success, message = self.game.move_piece("e4", "e6")

        self.assertFalse(success)
        self.assertEqual(message, "Invalid move for that piece.")

    def test_white_pawn_can_capture_diagonally(self):
        self.game.board[5][5] = "p"

        success, message = self.game.move_piece("e2", "f3")

        self.assertTrue(success)
        self.assertEqual(self.game.board[5][5], "P")
        self.assertEqual(self.game.board[6][4], ".")

    def test_white_pawn_cannot_capture_forward(self):
        self.game.board[5][4] = "p"

        success, message = self.game.move_piece("e2", "e3")

        self.assertFalse(success)
        self.assertEqual(message, "Invalid move for that piece.")

    def test_black_pawn_can_move_forward_one(self):
        self.game.move_piece("e2", "e4")  # Switch to black.

        success, message = self.game.move_piece("d7", "d6")

        self.assertTrue(success)
        self.assertEqual(self.game.board[2][3], "p")
        self.assertEqual(self.game.board[1][3], ".")

    def test_black_pawn_can_move_forward_two_from_start(self):
        self.game.move_piece("e2", "e4")  # Switch to black.

        success, message = self.game.move_piece("d7", "d5")

        self.assertTrue(success)
        self.assertEqual(self.game.board[3][3], "p")
        self.assertEqual(self.game.board[1][3], ".")

# -------------------------
    # Knight tests
    # -------------------------

    def test_knight_can_jump(self):
        success, message = self.game.move_piece("g1", "f3")

        self.assertTrue(success)
        self.assertEqual(self.game.board[5][5], "N")
        self.assertEqual(self.game.board[7][6], ".")

    def test_knight_can_move_other_l_shape(self):
        success, message = self.game.move_piece("b1", "c3")

        self.assertTrue(success)
        self.assertEqual(self.game.board[5][2], "N")
        self.assertEqual(self.game.board[7][1], ".")

    def test_knight_cannot_move_straight(self):
        success, message = self.game.move_piece("g1", "g3")

        self.assertFalse(success)
        self.assertEqual(message, "Invalid move for that piece.")

    # -------------------------
    # Rook tests
    # -------------------------

    def test_rook_cannot_jump_over_piece(self):
        success, message = self.game.move_piece("a1", "a3")

        self.assertFalse(success)
        self.assertEqual(message, "Invalid move for that piece.")

    def test_rook_can_move_straight_when_path_clear(self):
        self.game.board[6][0] = "."  # Clear pawn from a2.

        success, message = self.game.move_piece("a1", "a4")

        self.assertTrue(success)
        self.assertEqual(self.game.board[4][0], "R")
        self.assertEqual(self.game.board[7][0], ".")

    def test_rook_cannot_move_diagonally(self):
        self.game.board[6][0] = "."  # Clear a2.
        self.game.board[6][1] = "."  # Clear b2 so own-piece capture is not the issue.

        success, message = self.game.move_piece("a1", "b2")

        self.assertFalse(success)
        self.assertEqual(message, "Invalid move for that piece.")

    # -------------------------
    # Bishop tests
    # -------------------------

    def test_bishop_cannot_jump_over_piece(self):
        success, message = self.game.move_piece("c1", "g5")

        self.assertFalse(success)
        self.assertEqual(message, "Invalid move for that piece.")

    def test_bishop_can_move_diagonally_when_path_clear(self):
        self.game.board[6][3] = "."  # Clear pawn from d2.

        success, message = self.game.move_piece("c1", "g5")

        self.assertTrue(success)
        self.assertEqual(self.game.board[3][6], "B")
        self.assertEqual(self.game.board[7][2], ".")

    def test_bishop_cannot_move_straight(self):
        self.game.board[6][2] = "."  # Clear c2.

        success, message = self.game.move_piece("c1", "c3")

        self.assertFalse(success)
        self.assertEqual(message, "Invalid move for that piece.")

    # -------------------------
    # Queen tests
    # -------------------------

    def test_queen_can_move_straight_when_path_clear(self):
        self.game.board[6][3] = "."  # Clear d2.

        success, message = self.game.move_piece("d1", "d4")

        self.assertTrue(success)
        self.assertEqual(self.game.board[4][3], "Q")
        self.assertEqual(self.game.board[7][3], ".")

    def test_queen_can_move_diagonally_when_path_clear(self):
        self.game.board[6][4] = "."  # Clear e2.

        success, message = self.game.move_piece("d1", "h5")

        self.assertTrue(success)
        self.assertEqual(self.game.board[3][7], "Q")
        self.assertEqual(self.game.board[7][3], ".")

    def test_queen_cannot_move_like_knight(self):
        success, message = self.game.move_piece("d1", "e3")

        self.assertFalse(success)
        self.assertEqual(message, "Invalid move for that piece.")

    # -------------------------
    # King tests
    # -------------------------

    def test_king_can_move_one_square_when_clear(self):
        self.game.board[6][4] = "."  # Clear e2.

        success, message = self.game.move_piece("e1", "e2")

        self.assertTrue(success)
        self.assertEqual(self.game.board[6][4], "K")
        self.assertEqual(self.game.board[7][4], ".")

    def test_king_cannot_move_two_squares(self):
        self.game.board[6][4] = "."  # Clear e2.

        success, message = self.game.move_piece("e1", "e3")

        self.assertFalse(success)
        self.assertEqual(message, "Invalid move for that piece.")

if __name__ == "__main__":
    unittest.main()
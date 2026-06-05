'''Chess engine logic for a terminal two player chess game.'''


class ChessGame:
    def __init__(self):
        self.board = self.create_board()
        self.turn = "white"
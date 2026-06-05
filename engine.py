'''Chess engine logic for a terminal two player chess game.'''

COLS = 'abcdefgh'
ROWS = '12345678'

class ChessGame:
    def __init__(self):
        self.board = self.create_board()
        self.turn = "white"

    def create_board(self):
        return [
            ["r", "n", "b", "q", "k", "b", "n", "r"],
            ['p' for _ in range(8)],
            ['.' for _ in range(8)],
            ['.' for _ in range(8)],
            ['.' for _ in range(8)],
            ['.' for _ in range(8)],
            ['P' for _ in range(8)],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ]
    
    def display_board(self):
        print()
        for i, row in enumerate(self.board):
            rank = 8 - i
            print(rank, ' '.join(row))
        print('  ' + ' '.join(COLS))
        print()
'''Chess engine logic for a terminal two player chess game.'''

FILES = 'abcdefgh'
RANKS = '12345678'

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
        print('  ' + ' '.join(FILES))
        print()

    def square_to_index(self, square):
        if len(square) != 2:
            raise ValueError("Square must be like e2 or a7.")
        
        file = square[0]
        rank = square[1]

        if file not in FILES or rank not in RANKS:
            raise ValueError("Invalid square.")
        
        col = FILES.index(file)
        row = 8 - int(rank)

        return row, col
    
    def is_white_piece(self, piece):
        return piece.isupper()
    
    def piece_color(self, piece):
        if piece == '.':
            return None
        return "white" if self.is_white_piece(piece) else "black"

    def move_piece(self, start, end):
        start_row, start_col = self.square_to_index(start)
        end_row, end_col = self.square_to_index(end)

        piece = self.board[start_row][start_col]
        target = self.board[end_row][end_col]

        if piece == '.':
            return False, 'No piece at starting square.'
        
        if self.piece_color(piece) != self.turn:
            return False, f"It is {self.turn}'s turn."
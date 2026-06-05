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
    
    def is_valid_pawn_move(self, piece, start_row, start_col, end_row, end_col):
        direction = -1 if piece.isupper() else 1
        starting_row = 6 if piece.isupper() else 1

        row_diff = end_row - start_row
        col_diff = end_col - start_col

        target = self.board[end_row][end_col]

        # Move forward one square
        if col_diff == 0 and row_diff == direction and target == '.':
            return True
        
        # Move forward two squares from starting position
        if (
            col_diff == 0
            and start_row == starting_row
            and row_diff == 2 * direction
            and target == '.'
            and self.board[start_row + direction][start_col] == '.'
        ):
            return True
        
        # Capture Diagonally
        if abs(col_diff) == 1 and row_diff == direction and target != '.':
            return self.piece_color(target) != self.piece_color(piece)
        
        return False

    def is_valid_move(self, piece, start_row, start_col, end_row, end_col):
        piece_type = piece.lower()

        row_diff = end_row - start_row
        col_diff = end_col - start_col

        if piece_type == 'p':
            return self.is_valid_pawn_move(piece, start_row, start_col, end_row, end_col)
    
    def move_piece(self, start, end):
        start_row, start_col = self.square_to_index(start)
        end_row, end_col = self.square_to_index(end)

        piece = self.board[start_row][start_col]
        target = self.board[end_row][end_col]

        if piece == '.':
            return False, 'No piece at starting square.'
        
        if self.piece_color(piece) != self.turn:
            return False, f"It is {self.turn}'s turn."
        
        if target != '.' and self.piece_color(target) == self.turn:
            return False, "You cannot capture your own piece."
        
        if not self.is_valid_move(piece, start_row, start_col, end_row, end_col):
            return False, "Invalid move for that piece"
        

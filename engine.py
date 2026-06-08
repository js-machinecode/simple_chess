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

    def is_clear_straight_path(self, start_row, start_col, end_row, end_col):
        if start_row != end_row and start_col != end_col:
            return False
        
        row_step = 0
        col_step = 0

        if end_row > start_row:
            row_step = 1
        elif end_row < start_row:
            row_step = -1

        if end_col > start_col:
            col_step = 1
        elif end_col < start_col:
            col_step = -1

        row = start_row + row_step
        col = start_col + col_step

        while row != end_row or col != end_col:
            if self.board[row][col] != '.':
                return False
            row += row_step
            col += col_step
        
        return True

    def is_clear_diagonal_path(self, start_row, start_col, end_row, end_col):
        row_diff = end_row - start_row
        col_diff = end_col - start_col

        if abs(row_diff) != abs(col_diff):
            return False

        row_step = 1 if row_diff > 0 else -1
        col_step = 1 if col_diff > 0 else -1

        row = start_row + row_step
        col = start_col + col_step

        while row != end_row or col != end_col:
            if self.board[row][col] != ".":
                return False
            row += row_step
            col += col_step

        return True

    def is_valid_move(self, piece, start_row, start_col, end_row, end_col):
        piece_type = piece.lower()

        row_diff = end_row - start_row
        col_diff = end_col - start_col

        # pawn movement
        if piece_type == 'p':
            return self.is_valid_pawn_move(piece, start_row, start_col, end_row, end_col)
        
        # rook movement
        if piece_type == 'r':
            return self.is_clear_straight_path(start_row, start_col, end_row, end_col)

        # knight movement
        if piece_type == 'n':
            return (abs(row_diff), abs(col_diff)) in [(2,1), (1,2)]
        
        # bishop movement
        if piece_type == 'b':
            return self.is_clear_diagonal_path(start_row, start_col, end_row, end_col)
        
        # queen movement
        if piece_type == 'q':
            return (
                self.is_clear_straight_path(start_row, start_col, end_row, end_col)
                or self.is_clear_diagonal_path(start_row, start_col, end_row, end_col)
            )
        
        if piece_type == 'k':
            return abs(row_diff) <= 1 and abs(col_diff) <= 1
        
        return False
    
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
            return False, "Invalid move for that piece."
        

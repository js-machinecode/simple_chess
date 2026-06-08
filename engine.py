'''Chess engine logic for a terminal two player chess game.'''

FILES = 'abcdefgh'
RANKS = '12345678'

class ChessGame:
    def __init__(self):
        # create a new chess board with the starting positions for both players
        self.board = self.create_board()
        # turn is white since white always starts first
        self.turn = "white"

    def create_board(self):
        '''
        Create and return the initial chess board.

        uppercase letters = white
        lowercase letters = black

        '.' represents an empty square

        '''
        
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
        '''
        Print the board to the terminal.
        '''
        print()
        for i, row in enumerate(self.board):
            rank = 8 - i
            print(rank, ' '.join(row))
        print('  ' + ' '.join(FILES))
        print()

    def square_to_index(self, square):
        '''
        Convert chess notation into list indexes

        e.g.  e2 -> (6, 4)
              a8 -> (0, 0)

        the board is a list of lists
        player input has to be translated into row, col
        before the board can be accessed
        '''

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
        '''
        Determine which players owns a piece

        Returns:
                'white' for uppercase pieces
                'black' for lowercase pieces
                None for empty squares
        '''
        
        if piece == '.':
            return None
        return "white" if self.is_white_piece(piece) else "black"
    
    def is_valid_pawn_move(self, piece, start_row, start_col, end_row, end_col):
        '''
        Validate pawn movement.

        Pawns can:
            1. Move forward
            2. Capture diagonally
            3. Move two squares on first move

        white moves up
        black moves down
        '''
       
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
        '''
        Check whether every square between the start and destination is empty.

        Used by:
            1. Rook
            2. Queen

        Pieces are not allowed to move through other pieces.
        '''
        
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
        '''
        Verify that a diagonal path contains no blocking pieces.

        used by:
            1. bishop
            2. queen

        every square between start and destination must be empty
        '''
        
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
        '''
        Determine whether a piece can legally move
        from its current square to its destination

        This function acts as a dispatcher. It examines
        the piece type and sends the move to the appropriate movement rule.
        '''
        
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
        '''
        Attempt moving a piece from one square to another

        Responsible for:
            1. Converting user input into board indexes
            2. Verifying if a piece exists
            3. Verifying the correct player is moving
            4. Preventing capturing your own piece
            5. Verifying the move follows piece rules
            6. Update the board
            7. Switch turns

        Returns:
            (True, message) if successful
            (False, error_message) otherwise
        '''
        
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
        
        return True, 'Move successful.'

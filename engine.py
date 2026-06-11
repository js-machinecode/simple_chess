'''Chess engine logic for a terminal two player chess game.'''

FILES = 'abcdefgh'
RANKS = '12345678'

class ChessGame:
    def __init__(self):
        # create a new chess board with the starting positions for both players
        self.board = self.create_board()
        # turn is white since white always starts first
        self.turn = "white"

        self.winner = None
        self.game_over = False

        self.white_king_moved = False
        self.black_king_moved = False
        self.white_left_rook_moved = False
        self.white_right_rook_moved = False
        self.black_left_rook_moved = False
        self.black_right_rook_moved = False

    def opposite_color(self, color):
        return "black" if color == "white" else "white"

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
    
    def is_in_check(self, color):
        """
        Determine whether the specified player's king is currently under attack.

        A king is considered to be in check if any opposing piece can legally
        move to the king's square on its next turn.

        Parameters:
            color (str):
                The player whose king should be examined.
                Must be either "white" or "black".

        Returns:
            bool:
                True if the king is currently threatened by an opposing piece.
                False otherwise.

        Examples:
            is_in_check("white") -> True
            is_in_check("white") -> False
            is_in_check("black") -> True

        Design Strategy:
            1. Locate the specified king on the board.
            2. Determine the opposing player's color.
            3. Examine every enemy piece on the board.
            4. For each enemy piece, determine whether it has a legal move
            to the king's square.
            5. If any enemy piece can attack the king, return True.
            6. Otherwise return False.

        Note:
            This helper only detects whether a king is currently in check.
            It does not determine checkmate. Checkmate requires verifying
            that the checked player has no legal moves available to escape
            the threat.
        """
        king = "K" if color == "white" else "k"

        king_row = None
        king_col = None

        for row in range(8):
            for col in range(8):
                if self.board[row][col] == king:
                    king_row = row
                    king_col = col

        enemy_color = self.opposite_color(color)

        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]

                if piece != "." and self.piece_color(piece) == enemy_color:
                    if self.is_valid_move(piece, row, col, king_row, king_col):
                        return True

        return False
    
    
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
    
    def has_legal_moves(self, color):
        '''
        Check if the specified player has any legal moves available.

        This is used to determine checkmate. A player is in checkmate if
        their king is in check and they have no legal moves to escape the
        threat.

        Returns:
            True if the player has at least one legal move available.
            False if the player has no legal moves.
        '''
        
        for start_row in range(8):
            for start_col in range(8):
                piece = self.board[start_row][start_col]

                if piece != "." and self.piece_color(piece) == color:
                    for end_row in range(8):
                        for end_col in range(8):
                            target = self.board[end_row][end_col]

                            if (target == "." or self.piece_color(target) != color) and self.is_valid_move(piece, start_row, start_col, end_row, end_col):
                                # Make the move temporarily
                                original_piece = self.board[end_row][end_col]
                                self.board[end_row][end_col] = piece
                                self.board[start_row][start_col] = "."

                                # Check if the move leaves the king in check
                                in_check = self.is_in_check(color)

                                # Undo the move
                                self.board[start_row][start_col] = piece
                                self.board[end_row][end_col] = original_piece

                                if not in_check:
                                    return True
        
        return False
    
    def is_checkmate(self, color):
        """
        Determine whether the specified player is in checkmate.

        A player is in checkmate if:
            1. Their king is currently in check.
            2. They have no legal moves that remove the check.

        Parameters:
            color (str):
                "white" or "black"

        Returns:
            bool
        """
        return (self.is_in_check(color) and 
                not self.has_legal_moves(color))
    
    def update_game_over_and_winner(self):
        if self.is_checkmate("white"):
            self.game_over = True
            self.winner = "black"

        elif self.is_checkmate("black"):
            self.game_over = True
            self.winner = "white"

        else:
            self.game_over = False
            self.winner = None

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

        if piece == ".":
            return False, "No piece at starting square."

        if self.piece_color(piece) != self.turn:
            return False, f"It is {self.turn}'s turn."

        if target != "." and self.piece_color(target) == self.turn:
            return False, "You cannot capture your own piece."

        if not self.is_valid_move(piece, start_row, start_col, end_row, end_col):
            return False, "Invalid move for that piece."

        self.board[end_row][end_col] = piece
        self.board[start_row][start_col] = "."

        # If this move leaves the current player's king in check,
        # undo the move and reject it.
        if self.is_in_check(self.turn):
            self.board[start_row][start_col] = piece
            self.board[end_row][end_col] = target
            return False, "You cannot leave your king in check."

        self.turn = "black" if self.turn == "white" else "white"

        return True, "Move successful."

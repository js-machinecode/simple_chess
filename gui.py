import pygame
from engine import ChessGame
# Window dimensions.
# The chessboard itself is 800x800 pixels.
# An additional 50-pixel status bar is displayed at the bottom.
WIDTH = 800
BOARD_HEIGHT = 800
STATUS_HEIGHT = 50
HEIGHT = BOARD_HEIGHT + STATUS_HEIGHT

# Standard chess board dimensions.
ROWS = 8
COLS = 8

# Size of each square on the board.
SQUARE_SIZE = WIDTH // COLS

# RGB color values.
LIGHT_SQUARE = (240, 217, 181)
DARK_SQUARE = (181, 136, 99)
SELECTED_COLOR = (255, 255, 0)


def load_piece_images():
    '''
    Load all chess piece images from the assets folder.

    Creates a dictionary where:
        board character -> pygame image

    Example:
        "P" -> white pawn image
        "k" -> black king image

    Images are resized to fit a single board square.

    Returns:
        Dictionary containing all loaded images.
    '''
    piece_files = {
        "P": "white/pawn.svg",
        "R": "white/rook.svg",
        "N": "white/knight.svg",
        "B": "white/bishop.svg",
        "Q": "white/queen.svg",
        "K": "white/king.svg",
        "p": "black/pawn.svg",
        "r": "black/rook.svg",
        "n": "black/knight.svg",
        "b": "black/bishop.svg",
        "q": "black/queen.svg",
        "k": "black/king.svg",
    }

    images = {}

    for piece, file_path in piece_files.items():
        image = pygame.image.load(f"assets/{file_path}")
        image = pygame.transform.smoothscale(
            image,
            (SQUARE_SIZE, SQUARE_SIZE)
        )
        images[piece] = image

    return images


def draw_board(screen):
    '''
    Draw the checkerboard pattern.

    Alternates between light and dark colors to create
    the standard chess board appearance.

    Parameters:
        screen: pygame display surface
    '''
    for row in range(ROWS):
        for col in range(COLS):
            color = LIGHT_SQUARE if (row + col) % 2 == 0 else DARK_SQUARE

            pygame.draw.rect(
                screen,
                color,
                (
                    col * SQUARE_SIZE,
                    row * SQUARE_SIZE,
                    SQUARE_SIZE,
                    SQUARE_SIZE,
                ),
            )


def draw_pieces(screen, game, piece_images):
    '''
    Draw all pieces currently on the board.

    Loops through every square of the game board.
    If a square contains a piece, draw the corresponding
    image at that location.

    Parameters:
        screen: pygame display surface
        game: ChessGame object
        piece_images: dictionary of loaded piece images
    '''
    for row in range(ROWS):
        for col in range(COLS):
            piece = game.board[row][col]

            if piece != ".":
                screen.blit(
                    piece_images[piece],
                    (
                        col * SQUARE_SIZE,
                        row * SQUARE_SIZE,
                    ),
                )


def index_to_square(row, col):
    '''
    Convert board indexes into chess notation.

    Example:
        (7, 4) -> "e1"
        (0, 0) -> "a8"

    Used when the user clicks a square.

    Returns:
        Chess coordinate string.
    '''
    file_letter = "abcdefgh"[col]
    rank_number = str(8 - row)

    return file_letter + rank_number


def square_to_index(square):
    '''
    Convert chess notation into board indexes.

    Example:
        "e1" -> (7, 4)
        "a8" -> (0, 0)

    Used when highlighting selected squares.

    Returns:
        (row, col)
    '''
    col = "abcdefgh".index(square[0])
    row = 8 - int(square[1])

    return row, col


def draw_selected_square(screen, selected_square):
    '''
    Draw a yellow border around the selected square.

    Provides visual feedback showing which piece
    the player has currently selected.

    Parameters:
        screen: pygame display surface
        selected_square: chess coordinate or None
    '''
    if selected_square is None:
        return

    row, col = square_to_index(selected_square)

    pygame.draw.rect(
        screen,
        SELECTED_COLOR,
        (
            col * SQUARE_SIZE,
            row * SQUARE_SIZE,
            SQUARE_SIZE,
            SQUARE_SIZE,
        ),
        5,
    )


def handle_mouse_click(game, selected_square, mouse_position):
    '''
    Process a mouse click on the board.

    First click:
        Select a square.

    Second click:
        Attempt to move the selected piece to the
        destination square.

    Parameters:
        game: ChessGame object
        selected_square: currently selected square
        mouse_position: (x, y)

    Returns:
        (selected_square, message)
    '''
    mouse_x, mouse_y = mouse_position

    col = mouse_x // SQUARE_SIZE
    row = mouse_y // SQUARE_SIZE

    clicked_square = index_to_square(row, col)

    if selected_square is None:
        selected_square = clicked_square
        message = f"Selected {clicked_square}"
        return selected_square, message

    success, message = game.move_piece(selected_square, clicked_square)

    selected_square = None

    return selected_square, message

def draw_status_bar(screen, font, message):
    '''
    Draw the status bar beneath the board.

    Displays information such as:
        - selected piece
        - move success/failure
        - checkmate messages
        - draw messages

    Parameters:
        screen: pygame display surface
        font: pygame font object
        message: status text
    '''
    pygame.draw.rect(
        screen,
        (40, 40, 40),
        (0, BOARD_HEIGHT, WIDTH, STATUS_HEIGHT)
    )

    text = font.render(message, True, (255, 255, 255))

    screen.blit(
        text,
        (10, BOARD_HEIGHT + 10)
    )

def draw_game_over(screen, font, game):
    '''
    Display a game over overlay.

    A semi-transparent dark background is drawn
    over the board along with a winner message.

    Example:
        GAME OVER
        White Wins!

    Parameters:
        screen: pygame display surface
        font: pygame font object
        game: ChessGame object
    '''
    if not game.game_over:
        return

    overlay = pygame.Surface((WIDTH, BOARD_HEIGHT))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))

    screen.blit(overlay, (0, 0))

    if game.winner:
        text = f"{game.winner.capitalize()} Wins!"
    else:
        text = "Draw!"

    title = font.render("GAME OVER", True, (255, 255, 255))
    winner = font.render(text, True, (255, 255, 255))

    screen.blit(
        title,
        title.get_rect(center=(WIDTH // 2, 350))
    )

    screen.blit(
        winner,
        winner.get_rect(center=(WIDTH // 2, 450))
    )

def main():
    '''
    Main entry point of the graphical chess game.

    Responsibilities:
        1. Initialize pygame.
        2. Create the game window.
        3. Load chess piece images.
        4. Process user input.
        5. Draw the board and pieces.
        6. Display status messages.
        7. Run until the user closes the window.

    This function contains the main game loop.
    '''
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess")

    clock = pygame.time.Clock()

    status_font = pygame.font.SysFont(None, 32)
    large_font = pygame.font.SysFont(None, 96)

    game = ChessGame()
    piece_images = load_piece_images()

    selected_square = None
    message = "White to move"

    running = True
    # Main game loop.
    # Repeats approximately 60 times per second until
    # the user closes the window.
    while running:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                selected_square, message = handle_mouse_click(
                    game,
                    selected_square,
                    pygame.mouse.get_pos(),
                )

        draw_board(screen)
        draw_selected_square(screen, selected_square)
        draw_pieces(screen, game, piece_images)
        draw_status_bar(screen, status_font, message)

        if game.game_over:
            draw_game_over(screen, large_font, game)

        pygame.display.flip()
        clock.tick(60)


    pygame.quit()


if __name__ == "__main__":
    main()
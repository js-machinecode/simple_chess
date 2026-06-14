'''Terminal based two player chess game.'''

from engine import ChessGame

def parse_move_input(move):
    parts = move.strip().lower().split()
    input_length = len(parts)
    promotion_choice = 'q' # queen by default
    start, end = parts[:2]
    if input_length == 3:
        promotion_choice = move[2]
        if promotion_choice not in ('q', 'r', 'b', 'n'):
            raise ValueError("Promotion must be q, r, b, or n.")
    elif input_length > 3 or input_length < 2:
        raise ValueError('Enter moves like e2 e4 or e7 e8 q')
    
def main():
    game = ChessGame()

    print('Welcome to Terminal Chess!')
    print('Enter moves like: e2 e4\n If reaching final rank for pawn add' \
    ' the extra piece value you would like to promote your pawn to, e.g.: e7 e8 q')
    print('Type q to quit.')

    while True:
        game.display_board()
        print(f'{game.turn.capitalize()}\'s turn')

        move = input("Enter your move: ".strip().lower())

        try:
            start, end, promotion_choice = parse_move_input(move)
            success, message = game.move_piece(start, end, promotion_choice)
            print(message)
        except ValueError as error:
            print(error)



if __name__ == "__main__":
    main()
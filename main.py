'''Terminal based two player chess game.'''

from engine import ChessGame

def main():
    game = ChessGame()

    print('Welcome to Terminal Chess!')
    print('Enter moves like: e2 e4')
    print('Type q to quit.')

    while True:
        game.display_board()
        print(f'{game.turn.capitalize()}\'s turn')

        move = input("Enter your move: ".strip().lower())
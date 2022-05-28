import time
from typing import Optional, List

from progress.bar import IncrementalBar

from player import Player, HumanPlayer, RandomComputerPlayer, AIComputerPlayer


class TicTacToe:
    """TicTacToe class is used to hold game state."""
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.current_winner = None

    def print_board(self, board=None) -> None:
        """Print game board with state."""
        if not board:
            board = self.board
        for row in [board[i * 3:(i + 1) * 3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')

    def print_board_nums(self) -> None:
        """Print keymap for game board."""
        self.print_board(list(map(str, range(9))))

    def available_moves(self) -> List[int]:
        """Get list of available moves."""
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def empty_squares(self) -> bool:
        """Return True if there are empty squares on the game board."""
        return ' ' in self.board

    def num_empty_squares(self) -> int:
        """Count empty squares on the game board."""
        return self.board.count(' ')

    def make_move(self, square: int, letter: str) -> bool:
        """Change board state with current move (add X or O). Check if there is a winner."""
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square: int, letter: str) -> bool:
        """Verify if there is a row, column or diagonal with 3 same letters."""
        row_ind = square // 3
        row = self.board[row_ind*3: (row_ind+1)*3]
        if all([spot == letter for spot in row]):
            return True

        col_ind = square % 3
        column = [self.board[col_ind+i*3] for i in range(3)]
        if all([spot == letter for spot in column]):
            return True

        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            if all([spot == letter for spot in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([spot == letter for spot in diagonal2]):
                return True
        return False


def play(game: TicTacToe, x_player: Player, o_player: Player, print_game: bool = True) -> Optional[str]:
    """Main game loop. Render game state in console."""
    if print_game:
        game.print_board_nums()
    letter = 'X'
    while game.empty_squares():
        square = o_player.get_move(game) if letter == 'O' else x_player.get_move(game)
        if game.make_move(square, letter):
            if print_game:
                print(f'{letter} makes a move to square {square}')
                game.print_board()
                print()

            if game.current_winner:
                if print_game:
                    print(f'{letter} wins!')
                return letter

            letter = 'O' if letter == 'X' else 'X'

            if print_game:
                time.sleep(0.8)

    if print_game:
        print('It\'s a tie!')
    return None


if __name__ == '__main__':
    REPEATS = 1
    x_wins = o_wins = ties = 0
    bar = IncrementalBar('Countdown', max=REPEATS)
    for _ in range(REPEATS):
        x_player = AIComputerPlayer('X')
        o_player = HumanPlayer('O')
        t = TicTacToe()
        result = play(t, x_player, o_player, True)  # set print_game to False in multi-iteration runs.
        if result == 'X':
            x_wins += 1
        elif result == 'O':
            o_wins += 1
        else:
            ties += 1
        bar.next()
    bar.finish()
    print(f'Score: X: {x_wins}, O: {o_wins}, Tie: {ties}')

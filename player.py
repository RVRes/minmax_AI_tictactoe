import math
import random


class Player:
    """Base player class. Implementation will be in inheritors"""
    def __init__(self, letter):
        self.letter = letter  # letter X or O

    def get_move(self, game):
        """Get square on the game board to move next."""
        pass


class RandomComputerPlayer(Player):
    """Computer player which chooses random free square to move."""
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        """Get random square to move."""
        return random.choice(game.available_moves())


class HumanPlayer(Player):
    """Human player which can enter square to move in terminal."""
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        """Input square to move."""
        move = None
        while move is None:
            try:
                square = int(input(f'{self.letter} turn. Make move(0-8): '))
                if square not in game.available_moves():
                    raise ValueError
                move = square
            except ValueError:
                print('Invalid square. Try again.')
        return move


class AIComputerPlayer(Player):
    """Computer player which chooses square to move using minimax algorithm. Can't lose."""
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        """Run minimax to get move."""
        if len(game.available_moves()) == 9:
            square = random.randint(0, 8)
        else:
            square = self.minimax(game, self.letter)['position']
        return square

    def minimax(self, state, player):
        """Minimax algorithm. Chooses best move for current player when both players try to play efficiently."""
        max_player = self.letter
        other_player = 'O' if player == 'X' else 'X'

        if state.current_winner == other_player:
            return {'position': None,
                    'score': 1 * (state.num_empty_squares() + 1) if other_player == max_player else
                    -1 * (state.num_empty_squares() + 1)
                    }
        elif not state.empty_squares():
            return {'position': None, 'score': 0}

        if player == max_player:
            best = {'position': None, 'score': -math.inf}
        else:
            best = {'position': None, 'score': math.inf}

        for possible_move in state.available_moves():
            state.make_move(possible_move, player)
            sim_score = self.minimax(state, other_player)

            state.board[possible_move] = ' '
            state.current_winner = None
            sim_score['position'] = possible_move

            if player == max_player:
                if sim_score['score'] > best['score']:
                    best = sim_score
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score
        return best

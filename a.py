from easyAI import Negamax, AI_Player, Human_Player
from easyAI.games import TicTacToe
import random

SUCCESFUL_MOVE = 0.8


class TicTacDuh(TicTacToe):
    """The board positions are numbered as follows:
    1 2 3
    4 5 6
    7 8 9
    """

    def __init__(self, players):
        super().__init__(players)

    def make_move(self, move):
        if random.random() < SUCCESFUL_MOVE:
            super().make_move(move)


if __name__ == "__main__":
    # Start a match (and store the history of moves when it ends)
    player1 = AI_Player(Negamax(13))
    player2 = AI_Player(Negamax(13))
    game = TicTacToe([player1, player2])
    history = game.play()

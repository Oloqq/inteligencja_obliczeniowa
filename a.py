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
    ai = Negamax(13)  # The AI will think 13 moves in advance
    game = TicTacToe([Human_Player(), AI_Player(ai)])
    history = game.play()

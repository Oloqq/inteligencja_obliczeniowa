from easyAI import Negamax, AI_Player, Human_Player, TwoPlayerGame
import random

FAIL_PROB = 0.1

class Nimby(TwoPlayerGame):
    """
    The game starts with 4 piles of 5 pieces. In turn the players
    remove as much pieces as they want, but from one pile only. The
    player that removes the last piece loses.

    Parameters
    ----------

    players
      List of the two players e.g. [HumanPlayer(), HumanPlayer()]

    piles:
      The piles the game starts with. With piles=[2,3,4,4] the
      game will start with 1 pile of 2 pieces, 1 pile of 3 pieces, and 2
      piles of 4 pieces.

    max_removals_per_turn
      Max number of pieces you can remove in a turn. Default is no limit.

    """

    def __init__(self, players=None, max_removals_per_turn=None, piles=(5, 5, 5, 5)):
        """ Default for `piles` is 5 piles of 5 pieces. """
        self.players = players
        self.piles = list(piles)
        self.max_removals_per_turn = max_removals_per_turn
        self.current_player = 1  # player 1 starts.

    def possible_moves(self):
        return [
            "%d,%d" % (i + 1, j)
            for i in range(len(self.piles))
            for j in range(
                1,
                self.piles[i] + 1
                if self.max_removals_per_turn is None
                else min(self.piles[i] + 1, self.max_removals_per_turn),
            )
        ]

    def make_move(self, move):
        move = list(map(int, move.split(",")))
        pile = move[0] - 1
        amt = move[1]
        if random.random() < FAIL_PROB:
            amt -= 1
        self.piles[pile] -= amt

    # def unmake_move(self, move):  # optional, speeds up the AI
    #     print("unmake")
    #     move = list(map(int, move.split(",")))
    #     self.piles[move[0] - 1] += move[1]

    def show(self):
        print(" ".join(map(str, self.piles)))

    def win(self):
        return max(self.piles) == 0

    def is_over(self):
        return self.win()

    def scoring(self):
        return 100 if self.win() else 0

    def ttentry(self):
        return tuple(self.piles)  # optional, speeds up AI


if __name__ == "__main__":
    ai1 = AI_Player(Negamax(3))
    ai2 = AI_Player(Negamax(5))
    samples = 100

    for i in range(samples):
        if random.random() < 0.5:
            player1 = ai1
            player2 = ai2
        else:
            player1 = ai2
            player2 = ai1

        game = Nimby([player1, player2])
        history = game.play()

from easyAI import Negamax, AI_Player, TwoPlayerGame
from easyAI.games import Nim
import random


class Nimby(TwoPlayerGame):
    """
    1. c) Nimby: Nim, ale z 10% prawdopodobieństwem gracz, który się porusza, musi wziąć z wybranego stosu o jeden element mniej niż zamierzał.

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

    def __init__(self, fail_prob, players=None, max_removals_per_turn=None, piles=(5, 5, 5, 5)):
        """ Default for `piles` is 5 piles of 5 pieces. """
        self.players = players
        self.piles = list(piles)
        self.max_removals_per_turn = max_removals_per_turn
        self.current_player = 1  # player 1 starts.
        self.fail_prob = fail_prob

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
        if random.random() < self.fail_prob:
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

# 2.
# Napisz kod, który uruchamia dwóch graczy AI z algorytmem Negamax
# przeciwko sobie wielokrotnie, zmieniając gracza rozpoczynającego.
# Policz liczbę zwycięstw każdego z graczy.
# Porównaj dwa różne ustawienia maksymalnej głębokości
# dla gier na deterministycznym i probabilistycznym wariancie Twojej gry.


class PlayerReport:
    def __init__(self, ai):
        self.ai = ai
        self.report = {
            "deterministic": {
                "wins": 0,
                "losses": 0,
            },
            "probabilistic": {
                "wins": 0,
                "losses": 0,
            }
        }


def maybe_swap_players(p1, p2):
    if random.random() < 0.5:
        return p2, p1
    else:
        return p1, p2


def play(game, reports, casename):
    game.verbose = False
    game.play(verbose=False)
    winner = reports[game.current_player - 1]
    loser = reports[game.opponent_index - 1]
    winner.report[casename]["wins"] += 1
    loser.report[casename]["losses"] += 1


if __name__ == "__main__":
    report1 = PlayerReport(AI_Player(Negamax(3)))
    report2 = PlayerReport(AI_Player(Negamax(5)))
    samples = 100

    for i in range(samples):
        print(f"Case {i}")

        player1, player2 = maybe_swap_players(report1, report2)
        reports = [player1, player2]
        ais = [p.ai for p in reports]

        play(Nimby(0.1, ais), reports, "probabilistic")
        play(Nim(ais), reports, "deterministic")

    print("depth 3")
    print(report1.report)
    print()
    print("depth 5")
    print(report2.report)
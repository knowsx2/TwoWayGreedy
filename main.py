# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from game import Game
from agent import Agent


def main():
    b1, b2, b3 = 10, 22, 36
    bids = [b1, b2, b3]
    a1 = Agent("a1", [10, 22, 36], 10)
    a2 = Agent("a2", [10, 22, 36], 22)
    a3 = Agent("a3", [10, 22, 36], 36)
    players = [a1, a2, a3]
    solutions = [[a1], [a2, a3]]
    game = Game(players, bids, solutions)
    game.compute_tree(solutions, players, bids)
    return


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

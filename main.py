# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from game import *
from agent import Agent
from app import *
from algorithms import *


def run_app(root):
    app = App(0)
    print_node_on_frame(root, app.frame[0])
    app.add_frame()
    print_node_on_frame(root, app.frame[1])
    print(display(root))
    app.MainLoop()


def main():
    bids = [3.1, 4, 5]
    a1 = Agent("a1", bids, bids[0])
    a2 = Agent("a2", bids, bids[1])
    a3 = Agent("a3", bids, bids[2])
    a4 = Agent("a4", bids, bids[2])
    a5 = Agent("a5", bids, bids[2])

    #a4 = Agent("a4", bids, bids[0])
    players = [a1, a2, a3, a4, a5]
    # solutions = [[a1, a2, a3], [a2, a3, a4], [a1, a3, a4]]
    solutions = [[a2, a3], [a1, a4, a5]]
    app = App(0)
    '''
    #for game in all_directions_games(players, bids, solutions):
    game = Game(players, (1, 0, 0, 1, 1), bids, solutions)
    #for trees in game.compute_all_trees():
    trees = game.compute_all_trees()[0]
    tree = list(elaborate_trees(trees))[0]
    #for tree in list(elaborate_trees(trees)):
    app.add_frame(str(game.directions).replace(": 0", ": out").replace(": 1", ": in"))
    print_node_on_frame(tree, app.frame[-1])
    app.MainLoop()
    
    '''
    # testing search of incomplete nodes:
    game = Game(players, (1, 0, 0, 1, 1), bids, solutions)
    tree = Node(solutions, player=game.players[0], direction=1, bid=bids[0])
    app.add_frame(str(game.directions).replace(": 0", ": out").replace(": 1", ": in"))
    print_node_on_frame(tree, app.frame[-1])
    new_tree = euch_search(tree, game)
    app.add_frame(str(game.directions).replace(": 0", ": out").replace(": 1", ": in"))
    print_node_on_frame(new_tree, app.frame[-1])

    app.MainLoop()

    return


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

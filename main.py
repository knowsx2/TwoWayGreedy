# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from game import *
from agent import Agent
from app import *
import algorithms as algo
import algorithmsV2 as algov2
import algorithmsV2_1 as algov2_1
import copy


def run_app(root):
    app = App(0)
    print_node_on_frame(root, app.frame[0])
    app.add_frame()
    print_node_on_frame(root, app.frame[1])
    print(display(root))
    app.MainLoop()


def main():
    bids = [8, 17, 36]
    a1 = Agent("a1", bids, bids[0])
    a2 = Agent("a2", bids, bids[1])
    a3 = Agent("a3", bids, bids[2])
    # a4 = Agent("a4", bids, bids[2])
    # a5 = Agent("a5", bids, bids[2])

    players = [a1, a2, a3]
    # solutions = [[a1, a2, a3], [a2, a3, a4], [a1, a3, a4]]
    solutions = [[a1], [a2, a3]]
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
    game = Game(players, (1, 0, 1), bids, solutions)
    tree = next(possible_queries(players, game.directions, game.domains, solutions), None)
    if tree is None:
        print("non posso generare nessun nodo iniziale con questa configurazione")
        return
    tree = algov2.fill_tree(tree, game.directions, tree.domains, game.players)
    app.add_frame(str(game.directions).replace(": 0", ": out").replace(": 1", ": in"))
    print_node_on_frame(tree, app.frame[-1])
    # new_tree, changes = algo.euch_search(tree, game)
    # new_tree, changes = algov2.euch_search(tree, game)
    new_tree, changes = algov2_1.euch_search(tree, game)
    if new_tree is None:
        print("non è stata trovata una soluzione")
    else:
        print("sono stati effettuati " + str(changes) + " cambi di direzione")
    app.add_frame(str(game.directions).replace(": 0", ": out").replace(": 1", ": in"))
    print_node_on_frame(new_tree, app.frame[-1])

    app.MainLoop()

    return


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

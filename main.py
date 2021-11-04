# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from game import *
from agent import Agent
from app import *
from test_generator import generate
import algorithms as algo
import algorithmsV2 as algov2
import algorithmsV2_1 as algov2_1
import copy
import heapdict


def search_direction(players, forbidden):
    last = forbidden[-1]
    diffs = heapdict.heapdict()
    for direction in it.product([0, 1], repeat=len(players)):
        diffs[direction] = sum([abs(direction[i] - last[i]) for i in range(len(last))])
    while len(diffs) > 0:
        current = diffs.popitem()[0]
        if list(current) not in forbidden:
            return list(current)
    return None


def run_app(root):
    app = App(0)
    print_node_on_frame(root, app.frame[0])
    app.add_frame()
    print_node_on_frame(root, app.frame[1])
    print(display(root))
    app.MainLoop()


def main():
    # bids = [8, 17, 36]
    # a1 = Agent("a1", bids, bids[0])
    # a2 = Agent("a2", bids, bids[1])
    # a3 = Agent("a3", bids, bids[2])
    # a4 = Agent("a4", bids, bids[2])
    # a5 = Agent("a5", bids, bids[2])

    # players = [a1, a2, a3]
    # solutions = [[a1, a2, a3], [a2, a3, a4], [a1, a3, a4]]
    # solutions = [[a1], [a2, a3]]

    #bids, players, directions, solutions = generate()
    bids = [14, 32, 45, 86, 120, 126, 131]
    players = [Agent("a0", bids, bids[1]), Agent("a1", bids, bids[1]), Agent("a2", bids, bids[1])]
    directions, solutions = [0, 0, 1], [[players[0], players[1]], [players[0], players[2]]]

    print(bids, players, directions, solutions)
    app = App(0)
    red_flag = False
    white_flag = False
    for game in all_directions_games(players, bids, solutions):
        for trees in game.compute_all_trees():
            for tree in list(elaborate_trees(trees)):
                if not white_flag and check_solutioned_tree(tree):
                    app.add_frame(str(game.directions).replace(": 0", ": out").replace(": 1", ": in"))
                    print_node_on_frame(tree, app.frame[-1])
                    white_flag = True
                if not red_flag and not check_solutioned_tree(tree):
                    app.add_frame(str(game.directions).replace(": 0", ": out").replace(": 1", ": in"))
                    print_node_on_frame(tree, app.frame[-1])
                    red_flag = True

    #app.MainLoop()

    # testing search of incomplete nodes:
    temp_game = Game(players, directions, bids, solutions)
    tree = next(possible_queries(players, temp_game.directions, temp_game.domains, solutions), None)
    tested = []
    while tree is None:
        tested.append(directions)
        new_dir = search_direction(players, tested)
        if new_dir is not None:
            directions = new_dir
        else:
            print(bids, players, directions, solutions)
            print("non ci sono nodi iniziali con qualsiasi direzioni")
            return
        temp_game = Game(players, directions, bids, solutions)
        tree = next(possible_queries(players, temp_game.directions, temp_game.domains, solutions), None)

    print(bids, players, directions, solutions)
    game1 = Game(players, directions, bids, solutions)
    game2 = Game(players, directions, bids, solutions)
    game3 = Game(players, directions, bids, solutions)

    node = copy.copy(tree)

    tree = algov2.fill_tree(tree, game1.directions, tree.domains, game1.players)

    #app.add_frame(str(game1.directions).replace(": 0", ": out").replace(": 1", ": in"))
    #print_node_on_frame(tree, app.frame[-1])
    # app.MainLoop()

    new_tree, changes = algo.euch_search(tree, game1)
    if new_tree is None:
        print("VERSION 1: non è stata trovata una soluzione con " + str(changes) + " cambi di direzione")
    else:
        print("VERSION 1: sono stati effettuati " + str(changes) + " cambi di direzione")
        app.add_frame("Algo1 " + str(game1.directions).replace(": 0", ": out").replace(": 1", ": in"))
        print_node_on_frame(new_tree, app.frame[-1])

    tree = copy.copy(node)
    tree = algov2.fill_tree(tree, game2.directions, tree.domains, game2.players)
    new_tree, changes = algov2.euch_search(tree, game2)
    if new_tree is None:
        print("VERSION 2: non è stata trovata una soluzione con " + str(changes) + " cambi di direzione")
    else:
        print("VERSION 2: sono stati effettuati " + str(changes) + " cambi di direzione")
        app.add_frame("Algo2 " + str(game2.directions).replace(": 0", ": out").replace(": 1", ": in"))
        print_node_on_frame(new_tree, app.frame[-1])

    tree = copy.copy(node)
    tree = algov2.fill_tree(tree, game3.directions, tree.domains, game3.players)
    new_tree, changes = algov2_1.euch_search(tree, game3)
    if new_tree is None:
        print("VERSION 3: non è stata trovata una soluzione con " + str(changes) + " cambi di direzione")
    else:
        print("VERSION 3: sono stati effettuati " + str(changes) + " cambi di direzione")
        app.add_frame("Algo3 " + str(game3.directions).replace(": 0", ": out").replace(": 1", ": in"))
        print_node_on_frame(new_tree, app.frame[-1])

    app.MainLoop()
    return


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

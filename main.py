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

    # ******* PARAMETRI ********
    #n_players = 4

    while True:
        players, directions, solutions = generate()
        #bids = [29, 735, 1035, 1348, 1516, 3490, 4105, 4506, 4926, 5247, 5833, 5908, 6609]
        #players = [Agent("a" + str(i), bids, bids[0]) for i in range(n_players)]
        #players = [Agent("a0", bids, bids[0]), Agent("a9", bids, bids[0]), Agent("a1", bids, bids[0]), Agent("a2", bids, bids[0]), Agent("a3", bids, bids[0]), Agent("a8", bids, bids[0]), Agent("a6", bids, bids[0]), Agent("a7", bids, bids[0]), Agent("a5", bids, bids[0]), Agent("a4", bids, bids[0])]

        #directions = [0, 1, 1, 0, 0, 0, 0, 0, 1, 0]
        #solutions = [[players[0], players[9], players[1]], [players[0], players[2]], [players[2], players[9], players[3]], [players[2], players[8]], [players[6], players[9]], [players[7]], [players[0], players[5]], [players[4], players[9]]]
        print({players[i]: players[i].domain for i in range(len(players))}, directions, solutions)
        #app = App(0)
        '''
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
        '''
        #app.MainLoop()

        # testing search of incomplete nodes:
        temp_game = Game(players, directions, solutions)
        tree = next(possible_queries(players, temp_game.directions, temp_game.domains, solutions), None)
        #tested = []
        av_dir = set(it.product([0, 1], repeat=len(directions)))
        flag = False
        while tree is None:
            #tested.append(directions)
            av_dir.remove(tuple(directions))
            new_dir = algo.search_direction(av_dir, directions)
            if new_dir is not None:
                directions = new_dir
            else:
                print({players[i]: players[i].domain for i in range(len(players))}, directions, solutions)
                print("non ci sono nodi iniziali con qualsiasi direzione")
                flag = True
                break
        if flag:
            print("\n")
            continue
        temp_game = Game(players, directions, solutions)
        tree = next(possible_queries(players, temp_game.directions, temp_game.domains, solutions), None)

        print({players[i]: players[i].domain for i in range(len(players))}, directions, solutions)
        game1 = Game(players, directions, solutions)
        game2 = Game(players, directions, solutions)
        game3 = Game(players, directions, solutions)
        game4 = Game(players, directions, solutions)

        node = copy.copy(tree)

        tree = algov2.fill_tree(tree, game1.directions, tree.domains, game1.players)
    
        #app.add_frame(str(game1.directions).replace(": 0", ": out").replace(": 1", ": in"))
        #print_node_on_frame(tree, app.frame[-1])
        #app.MainLoop()
    
        new_tree, changes = algo.euch_search(tree, game1)
        if new_tree is None:
            print("VERSION 2.1: non è stata trovata una soluzione con " + str(sum(changes.values())) + " cambi di direzione")
        else:
            print("VERSION 2.1: sono stati effettuati " + str(changes) + " cambi di direzione: " + str(sum(changes.values())))
            #app.add_frame("Algo2.1 " + str(game1.directions).replace(": 0", ": out").replace(": 1", ": in"))
            #print_node_on_frame(new_tree, app.frame[-1])


        tree = copy.copy(node)
        tree = algov2.fill_tree(tree, game2.directions, tree.domains, game2.players)
        new_tree, changes = algov2.euch_search(tree, game2)
        if new_tree is None:
            print("VERSION 2.2: non è stata trovata una soluzione con " + str(sum(changes.values())) + " cambi di direzione")
        else:
            print("VERSION 2.2: sono stati effettuati " + str(changes) + " cambi di direzione: " + str(sum(changes.values())))
            #app.add_frame("Algo2.2 " + str(game2.directions).replace(": 0", ": out").replace(": 1", ": in"))
            #print_node_on_frame(new_tree, app.frame[-1])


        tree = copy.copy(node)
        tree = algov2.fill_tree(tree, game4.directions, tree.domains, game4.players)
        new_tree, changes = algov2.euch_search(tree, game4, False)
        if new_tree is None:
            print(
                "VERSION 2.3: non è stata trovata una soluzione con " + str(sum(changes.values())) + " cambi di direzione")
        else:
            print(
                "VERSION 2.3: sono stati effettuati " + str(changes) + " cambi di direzione: " + str(sum(changes.values())))
            #app.add_frame("Algo2.3 " + str(game4.directions).replace(": 0", ": out").replace(": 1", ": in"))
            #print_node_on_frame(new_tree, app.frame[-1])
    
        tree = copy.copy(node)
        tree = algov2.fill_tree(tree, game3.directions, tree.domains, game3.players)
        new_tree, changes = algov2_1.euch_search(tree, game3)
        if new_tree is None:
            print("VERSION 2.4: non è stata trovata una soluzione con " + str(sum(changes.values())) + " cambi di direzione")
        else:
            print("VERSION 2.4: sono stati effettuati " + str(changes) + " cambi di direzione: " + str(sum(changes.values())))
            #app.add_frame("Algo2.4 " + str(game3.directions).replace(": 0", ": out").replace(": 1", ": in"))
            #print_node_on_frame(new_tree, app.frame[-1])
        print("\n")
    #app.MainLoop()
    return


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

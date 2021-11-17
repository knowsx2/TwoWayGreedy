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
import time
from math import log


def run_app(root):
    app = App(0)
    print_node_on_frame(root, app.frame[0])
    app.add_frame()
    print_node_on_frame(root, app.frame[1])
    print(display(root))
    app.MainLoop()


def main():
    # ******* PARAMETRI ********

    # n_players = 4
    # bids = [29, 735, 1035, 1348, 1516, 3490, 4105, 4506, 4926, 5247, 5833, 5908, 6609]
    # players = [Agent("a" + str(i), bids, bids[0]) for i in range(n_players)]
    # players = [Agent("a0", bids, bids[0]), Agent("a9", bids, bids[0]), Agent("a1", bids, bids[0]), Agent("a2", bids, bids[0]), Agent("a3", bids, bids[0]), Agent("a8", bids, bids[0]), Agent("a6", bids, bids[0]), Agent("a7", bids, bids[0]), Agent("a5", bids, bids[0]), Agent("a4", bids, bids[0])]
    # directions = [0, 1, 1, 0, 0, 0, 0, 0, 1, 0]
    # solutions = [[players[0], players[9], players[1]], [players[0], players[2]], [players[2], players[9], players[3]], [players[2], players[8]], [players[6], players[9]], [players[7]], [players[0], players[5]], [players[4], players[9]]]

    with open("test_del_2_2.txt", "w") as fx:
        cicli = 0
        while True:

            players, directions, solutions = generate()
            # print({players[i]: players[i].domain for i in range(len(players))}, directions, solutions)
            # app = App(0)
            appr = 2
            '''
            **************** BRUTE FORCE ****************
            red_flag = False
            white_flag = False
            for game in all_directions_games(players, solutions):
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
            app.MainLoop()
            '''

            # testing search of incomplete nodes:
            temp_game = Game(players, directions, solutions)
            tree = next(possible_queries(players, temp_game.directions, temp_game.domains, solutions), None)
            if tree is None:
                tree = next(possible_queries(players, temp_game.directions, temp_game.domains, solutions, appr), None)
            av_dir = set(it.product([0, 1], repeat=len(directions)))
            flag = False
            while tree is None:
                av_dir.remove(tuple(directions))
                new_dir = algo.search_direction(av_dir, directions)
                if new_dir is not None:
                    directions = new_dir
                    temp_game = Game(players, directions, solutions)
                    tree = next(possible_queries(players, temp_game.directions, temp_game.domains, solutions), None)
                    if tree is None:
                        tree = next(possible_queries(players, temp_game.directions, temp_game.domains, solutions, appr),
                                    None)
                else:
                    # print({players[i]: players[i].domain for i in range(len(players))}, directions, solutions)
                    # print("non ci sono nodi iniziali con qualsiasi direzione")
                    flag = True
                    break
            if flag:
                # print("\n")
                continue


            stampa_game = str({players[i]: players[i].domain for i in range(len(players))}) + str(directions) + str(
                solutions)
            # game1 = Game(players, directions, solutions)
            game2 = Game(players, directions, solutions)
            # game3 = Game(players, directions, solutions)
            # game4 = Game(players, directions, solutions)

            # print(stampa_game, file=fx)

            node = copy.copy(tree)
            '''
            tree = algov2.fill_tree(tree, game1.directions, tree.domains, game1.players)
            # app.add_frame(str(game1.directions).replace(": 0", ": out").replace(": 1", ": in"))
            # print_node_on_frame(tree, app.frame[-1])
            # app.MainLoop()
    
            t1_start = time.process_time()
            new_tree, changes = algo.euch_search(tree, game1)
            t1 = time.process_time() - t1_start
            stampa_flag = True
            if new_tree is None:
                # pass
                print(stampa_game, file=fx)
                stampa_flag = False
                print("VERSION 2.1: non è stata trovata una soluzione con " + str(
                    sum(changes.values())) + " cambi di direzione. t= %0.3f" % t1, file=fx)
            else:
                if sum(changes.values()) > 0:
                    print(stampa_game, file=fx)
                    stampa_flag = False
                    print("VERSION 2.1: sono stati effettuati " + str(changes) + " cambi di direzione: " + str(
                        sum(changes.values())) + ". t= %0.3f" % t1, file=fx)
                # app.add_frame("Algo2.1 " + str(game1.directions).replace(": 0", ": out").replace(": 1", ": in"))
                # print_node_on_frame(new_tree, app.frame[-1])
            '''
            tree = copy.copy(node)
            tree = algov2.fill_tree(tree, game2.directions, tree.domains, game2.players, appr)
            t2_start = time.process_time()
            new_tree, changes = algov2.euch_search(tree, game2, appr)
            t2 = time.process_time() - t2_start
            if new_tree is None:
                # pass
                # if stampa_flag:
                print(stampa_game, file=fx)
                #    stampa_flag = True
                print("VERSION 2.2: non è stata trovata una soluzione con " + str(
                    sum(changes.values())) + " cambi di direzione. t= %0.3f" % t2, file=fx)
                print("VERSION 2.2: non è stata trovata una soluzione con " + str(
                    sum(changes.values())) + " cambi di direzione. t= %0.3f" % t2)
            else:
                if sum(changes.values()) > 0:
                    # if stampa_flag:
                    #    print(stampa_game, file=fx)
                    #    stampa_flag = True
                    print(stampa_game, file=fx)
                    print("VERSION 2.2: sono stati effettuati " + str(changes) + " cambi di direzione: " + str(
                        sum(changes.values())) + ". t= %0.3f" % t2, file=fx)
                    print(stampa_game)
                    print("VERSION 2.2: sono stati effettuati " + str(changes) + " cambi di direzione: " + str(
                        sum(changes.values())))

                # app.add_frame("Algo2.2 " + str(game2.directions).replace(": 0", ": out").replace(": 1", ": in"))
                # print_node_on_frame(new_tree, app.frame[-1])
            '''
            tree = copy.copy(node)
            tree = algov2.fill_tree(tree, game4.directions, tree.domains, game4.players)
            t3_start = time.process_time()
            new_tree, changes = algov2.euch_search(tree, game4, False)
            t3 = time.process_time() - t3_start
            if new_tree is None:
                if stampa_flag:
                    print(stampa_game, file=fx)
                    stampa_flag = True
                print("VERSION 2.3: non è stata trovata una soluzione con " + str(
                    sum(changes.values())) + " cambi di direzione. t= %0.3f" % t3, file=fx)
            else:
                if sum(changes.values()) > 0:
                    if stampa_flag:
                        print(stampa_game, file=fx)
                        stampa_flag = True
                    print(
                        "VERSION 2.3: sono stati effettuati " + str(changes) + " cambi di direzione: " + str(
                            sum(changes.values())) + ". t= %0.3f" % t3, file=fx)
                # app.add_frame("Algo2.3 " + str(game4.directions).replace(": 0", ": out").replace(": 1", ": in"))
                # print_node_on_frame(new_tree, app.frame[-1])

            tree = copy.copy(node)
            tree = algov2.fill_tree(tree, game3.directions, tree.domains, game3.players)
            t4_start = time.process_time()
            new_tree, changes = algov2_1.euch_search(tree, game3)
            t4 = time.process_time() - t4_start
            if new_tree is None:
                if stampa_flag:
                    print(stampa_game, file=fx)
                print("VERSION 2.4: non è stata trovata una soluzione con " + str(
                    sum(changes.values())) + " cambi di direzione. t= %0.3f" % t4, file=fx)
            else:
                if sum(changes.values()) > 0:
                    if stampa_flag:
                        print(stampa_game, file=fx)
                    print("VERSION 2.4: sono stati effettuati " + str(changes) + " cambi di direzione: " + str(
                        sum(changes.values())) + ". t= %0.3f" % t4, file=fx)
                    # app.add_frame("Algo2.4 " + str(game3.directions).replace(": 0", ": out").replace(": 1", ": in"))
                    # print_node_on_frame(new_tree, app.frame[-1])
            '''
            print("ciclo: ", cicli)
            cicli += 1
        # app.MainLoop()
    return


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

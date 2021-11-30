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
import matplotlib.pyplot as plt

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

    with open("test_outliners.txt", "w") as fx:
        avarage_time_w_sol = []
        avarage_time_wo_sol = []
        ratio_fast_finish = []
        sol_exists_not_found = []
        avarage_changes = []
        avarage_time_bf_w_sol = []
        avarage_time_bf_wo_sol = []
        all_vett_changes = []
        n_from = 5
        n_to = 14
        for n_players in range(n_from, n_to):
            time_without_solutions = []
            time_with_solutions = []
            time_bruteforce_with_solutions = []
            time_bruteforce_with_no_solutions = []
            counter_fast_finish = 0
            counter_total_finish = 0
            trashout_fast_finish = 2 * n_players
            trashout_outliner = 25 * n_players
            vett_changes = []
            outliners = []
            counter = 0
            while counter_total_finish < 100:
                players, directions, solutions = generate(n_players, 5, 3)
                # print({players[i]: players[i].domain for i in range(len(players))}, directions, solutions)
                # app = App(0)
                appr = 1
                '''
                #  ** ** ** ** ** ** ** ** BRUTEFORCE ** ** ** ** ** ** ** **
                tb_start = time.process_time()
                exists = False
                for game in all_directions_games(players, solutions):
                    trees = list(game.compute_all_trees())
                    if check_if_sol_exists(trees):
                        exists = True
                        break
                tb = time.process_time() - tb_start
                if exists:
                    time_bruteforce_with_solutions.append(tb)
                else:
                    time_bruteforce_with_no_solutions.append(tb)
                '''

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

                temp_game = Game(players, directions, solutions)
                tree, new_appr = next(possible_queries(players, temp_game.directions, temp_game.domains, solutions),
                                      (None, 1))
                if tree is None:
                    tree, new_appr = next(
                        possible_queries(players, temp_game.directions, temp_game.domains, solutions, appr), (None, 1))
                av_dir = set(it.product([0, 1], repeat=len(directions)))
                flag = False
                while tree is None:
                    av_dir.remove(tuple(directions))
                    new_dir = algo.search_direction(av_dir, directions)
                    if new_dir is not None:
                        directions = new_dir
                        temp_game = Game(players, directions, solutions)
                        tree, new_appr = next(
                            possible_queries(players, temp_game.directions, temp_game.domains, solutions), (None, 1))
                        if tree is None:
                            tree, new_appr = next(
                                possible_queries(players, temp_game.directions, temp_game.domains, solutions, appr),
                                (None, 1))
                    else:
                        #print(stampa_game)
                        #print("non ci sono nodi iniziali con qualsiasi direzione")
                        flag = True
                        break
                if flag:
                    # print("\n")
                    continue

                # game1 = Game(players, directions, solutions)
                game2 = Game(players, directions, solutions)
                # game3 = Game(players, directions, solutions)
                # game4 = Game(players, directions, solutions)

                # print(game2, file=fx)

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
                param_game = copy.copy(game2)
                tree = algov2.fill_tree(tree, game2.directions, tree.domains, game2.players, new_appr)
                t2_start = time.process_time()
                new_tree, changes = algov2.euch_search(tree, game2, new_appr)
                t2 = time.process_time() - t2_start
                if new_tree is None:
                    time_without_solutions.append(t2)
                else:
                    if sum(changes.values()) > 0:
                        time_with_solutions.append(t2)
                        vett_changes.append(sum(changes.values()))
                        if sum(changes.values()) <= trashout_fast_finish:
                            counter_fast_finish += 1
                        counter_total_finish += 1
                        #print(counter_total_finish, counter)
                        if sum(changes.values()) >= trashout_outliner:
                            outliners.append(sum(changes.values()))
                            print(str(param_game) + "\n", file=fx)

                    # app.add_frame("Algo2.2 " + str(game2.directions).replace(": 0", ": out").replace(": 1", ": in"))
                    # print_node_on_frame(new_tree, app.frame[-1])
                counter+=1
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
            print(str(n_players) + " players fatto")
            print(outliners)
            avarage_time_w_sol.append(sum(time_with_solutions)/len(time_with_solutions))
            avarage_time_wo_sol.append(sum(time_without_solutions)/len(time_without_solutions))

            #avarage_time_bf_w_sol.append(sum(time_bruteforce_with_solutions) / len(time_bruteforce_with_solutions))
            #avarage_time_bf_wo_sol.append(sum(time_bruteforce_with_no_solutions) / len(time_bruteforce_with_no_solutions))

            avarage_changes.append((sum(vett_changes)/len(vett_changes), len(vett_changes)))
            all_vett_changes.append(vett_changes)
            ratio_fast_finish.append(counter_fast_finish/counter_total_finish)
            #sol_exists_not_found.append(solution_exists_but_not_found)

        fig, axs = plt.subplots(3, 1)  # Create a figure containing a single axes.
        fig.set_size_inches(18.5, 10.5)

        axs[0].plot(range(n_from, n_to), avarage_time_w_sol, 'g', label="av time with sols")  # Plot some data on the axes.
        axs[0].plot(range(n_from, n_to), avarage_time_wo_sol, 'r', label="av time with no sols")
        #axs[0].plot(range(n_from, n_to), avarage_time_bf_w_sol, 'b', label="av time bf with sols")
        #axs[0].plot(range(n_from, n_to), avarage_time_bf_wo_sol, 'm', label="av time bf with no sols")
        axs[0].set_ylabel("time (s)")
        axs[0].legend()

        axs[1].plot(range(n_from, n_to), [x[0] for x in avarage_changes], 'r')
        axs[1].set_ylabel("avarage changes")
        for i in range(n_from, n_to):
            axs[1].plot([i]*len(all_vett_changes[i-n_from]), all_vett_changes[i-n_from], 'bo')
        #axs[2].plot(range(n_from, n_to), [x[1] for x in avarage_changes], 'bo')
        #axs[2].set_ylabel("rounds")

        #axs[3].plot(range(n_from, n_to), sol_exists_not_found, 'ro')
        #axs[3].set_ylabel("not found existing sol")

        axs[2].plot(range(n_from, n_to), ratio_fast_finish, 'ro')
        axs[2].set_ylabel("ratio fast finish")
        axs[2].set_xlabel("n_players")
        plt.savefig("agents_from5_to13")

            # app.MainLoop()
    return


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

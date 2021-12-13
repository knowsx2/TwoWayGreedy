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


def main():
    with open("test_outliners.txt", "w") as fx:
        avarage_time_w_sol = []
        avarage_time_wo_sol = []
        ratio_fast_finish = []
        avarage_changes = []
        # avarage_time_bf_w_sol = [] UNCOMMENT IF BRUTEFORCE IS USED
        # avarage_time_bf_wo_sol = [] UNCOMMENT IF BRUTEFORCE IS USED
        all_vett_changes = []
        n_from = 5
        n_to = 14
        for n_players in range(n_from, n_to):
            time_without_solutions = []
            time_with_solutions = []
            # time_bruteforce_with_solutions = [] UNCOMMENT IF BRUTEFORCE IS USED
            # time_bruteforce_with_no_solutions = [] UNCOMMENT IF BRUTEFORCE IS USED
            counter_fast_finish = 0
            counter_total_finish = 0
            trashout_fast_finish = 2 * n_players
            trashout_outliner = 25 * n_players
            vett_changes = []
            outliners = []
            counter = 0
            while counter_total_finish < 100:
                players, directions, solutions = generate(n_players, 5, 3)
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
                Create a initial node of mechanism
                '''
                temp_game = Game(players, directions, solutions)
                tree = next(possible_queries(players, temp_game.directions, temp_game.domains, solutions),
                            None)
                if tree is None:
                    tree = next(
                        possible_queries(players, temp_game.directions, temp_game.domains, solutions, appr), None)
                av_dir = set(it.product([0, 1], repeat=len(directions)))
                while tree is None:
                    av_dir.remove(tuple(directions))
                    new_dir = algo.search_direction(av_dir, directions)
                    if new_dir is not None:
                        directions = new_dir
                        temp_game = Game(players, directions, solutions)
                        tree = next(
                            possible_queries(players, temp_game.directions, temp_game.domains, solutions), None)
                        if tree is None:
                            tree = next(
                                possible_queries(players, temp_game.directions, temp_game.domains, solutions, appr),
                                None)

                # create the game
                game2 = Game(players, directions, solutions)

                # if more then one algorithm will be used on the tree, a copy of initial tree will be useful
                # node = copy.copy(tree)

                # tree = copy.copy(node)
                param_game = copy.copy(game2)  # save the initial parameters, during the algorithm execution they will
                # be changed to find a configuration of a complete mechanism
                tree = algov2.fill_tree(tree, game2.directions, tree.domains, game2.players, appr)
                t2_start = time.process_time()
                new_tree, changes = algov2.euch_search(tree, game2, appr)
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
                        print(counter_total_finish, counter)
                        if sum(changes.values()) >= trashout_outliner:
                            outliners.append(sum(changes.values()))
                            print(str(param_game) + "\n", file=fx)
                counter += 1

            print(str(n_players) + " players fatto")
            print(outliners)
            avarage_time_w_sol.append(sum(time_with_solutions) / len(time_with_solutions))
            avarage_time_wo_sol.append(sum(time_without_solutions) / len(time_without_solutions))

            avarage_changes.append((sum(vett_changes) / len(vett_changes), len(vett_changes)))
            all_vett_changes.append(vett_changes)
            ratio_fast_finish.append(counter_fast_finish / counter_total_finish)

        fig, axs = plt.subplots(3, 1)  # Create a figure containing a single axes.
        fig.set_size_inches(18.5, 10.5)

        axs[0].plot(range(n_from, n_to), avarage_time_w_sol, 'g',
                    label="av time with sols")  # Plot some data on the axes.
        axs[0].plot(range(n_from, n_to), avarage_time_wo_sol, 'r', label="av time with no sols")

        axs[0].set_ylabel("time (s)")
        axs[0].legend()

        axs[1].plot(range(n_from, n_to), [x[0] for x in avarage_changes], 'r')
        axs[1].set_ylabel("avarage changes")
        for i in range(n_from, n_to):
            axs[1].plot([i] * len(all_vett_changes[i - n_from]), all_vett_changes[i - n_from], 'bo')

        axs[2].plot(range(n_from, n_to), ratio_fast_finish, 'ro')
        axs[2].set_ylabel("ratio fast finish")
        axs[2].set_xlabel("n_players")
        plt.savefig("agents_from5_to13")
    return


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

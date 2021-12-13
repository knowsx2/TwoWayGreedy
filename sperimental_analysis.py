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

time_without_solutions = [[], [], [], []]
time_with_solutions = [[], [], [], []]
time_bruteforce_with_solutions = [[], [], [], []]
time_bruteforce_with_no_solutions = [[], [], [], []]
counter_fast_finish = [0, 0, 0, 0]
counter_total_finish = [0, 0, 0, 0]
vett_changes = [[], [], [], []]
outliners = [[], [], [], []]
solution_exists_but_not_found = 0
for i in range(100):
    players, directions, solutions = generate()
    trashout_fast_finish = max((2 ** len(players)) / 50, 2 * len(players))
    trashout_outliner = (2 ** len(players)) / 10
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

    temp_game = Game(players, directions, solutions)
    tree = next(possible_queries(players, temp_game.directions, temp_game.domains, solutions), None)
    if tree is None:
        tree = next(
            possible_queries(players, temp_game.directions, temp_game.domains, solutions, appr), None)
    av_dir = set(it.product([0, 1], repeat=len(directions)))
    flag = False
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

    game1 = Game(players, directions, solutions)
    game2 = Game(players, directions, solutions)
    game3 = Game(players, directions, solutions)
    game4 = Game(players, directions, solutions)


    node = copy.copy(tree)

    tree = algov2.fill_tree(tree, game1.directions, tree.domains, game1.players, appr)

    t1_start = time.process_time()
    new_tree, changes = algo.euch_search(tree, game1, appr)
    t1 = time.process_time() - t1_start
    stampa_flag = True
    if new_tree is None:
        time_without_solutions[0].append(t1)
        # if exists:
        #    solution_exists_but_not_found += 1
    else:
        if sum(changes.values()) > 0:
            time_with_solutions[0].append(t1)
            vett_changes[0].append(sum(changes.values()))
            if sum(changes.values()) <= trashout_fast_finish:
                counter_fast_finish[0] += 1
            counter_total_finish[0] += 1
            if sum(changes.values()) >= trashout_outliner:
                outliners[0].append(sum(changes.values()))

    tree = copy.copy(node)
    tree = algov2.fill_tree(tree, game2.directions, tree.domains, game2.players, appr)
    t2_start = time.process_time()
    new_tree, changes = algov2.euch_search(tree, game2, appr)
    t2 = time.process_time() - t2_start
    if new_tree is None:
        time_without_solutions[1].append(t2)
    else:
        if sum(changes.values()) > 0:
            time_with_solutions[1].append(t2)
            vett_changes[1].append(sum(changes.values()))
            if sum(changes.values()) <= trashout_fast_finish:
                counter_fast_finish[1] += 1
            counter_total_finish[1] += 1
            if sum(changes.values()) >= trashout_outliner:
                outliners[1].append(sum(changes.values()))

    tree = copy.copy(node)
    tree = algov2.fill_tree(tree, game4.directions, tree.domains, game4.players, appr)
    t3_start = time.process_time()
    new_tree, changes = algov2.euch_search(tree, game4, appr, False)
    t3 = time.process_time() - t3_start
    if new_tree is None:
        time_without_solutions[2].append(t3)
    else:
        if sum(changes.values()) > 0:
            time_with_solutions[2].append(t3)
            vett_changes[2].append(sum(changes.values()))
            if sum(changes.values()) <= trashout_fast_finish:
                counter_fast_finish[2] += 1
            counter_total_finish[2] += 1
            if sum(changes.values()) >= trashout_outliner:
                outliners[2].append(sum(changes.values()))

    tree = copy.copy(node)
    tree = algov2.fill_tree(tree, game3.directions, tree.domains, game3.players, appr)
    t4_start = time.process_time()
    new_tree, changes = algov2_1.euch_search(tree, game3)
    t4 = time.process_time() - t4_start
    if new_tree is None:
        time_without_solutions[3].append(t4)
    else:
        if sum(changes.values()) > 0:
            time_with_solutions[3].append(t4)
            vett_changes[3].append(sum(changes.values()))
            if sum(changes.values()) <= trashout_fast_finish:
                counter_fast_finish[3] += 1
            counter_total_finish[3] += 1
            if sum(changes.values()) >= trashout_outliner:
                outliners[3].append(sum(changes.values()))
for i in range(4):
    print(len(time_with_solutions[i]))
    print(counter_total_finish[i])
    avarage_time_w_sol.append(sum(time_with_solutions[i]) / len(time_with_solutions[i]))
    avarage_time_wo_sol.append(sum(time_without_solutions[i]) / len(time_without_solutions[i]))

    # avarage_time_bf_w_sol[i].append(sum(time_bruteforce_with_solutions[i]) / len(time_bruteforce_with_solutions[i]))
    # avarage_time_bf_wo_sol[i].append(sum(time_bruteforce_with_no_solutions[i]) / len(time_bruteforce_with_no_solutions[i]))

    avarage_changes.append((sum(vett_changes[i]) / len(vett_changes[i]), len(vett_changes[i])))
    all_vett_changes.append(vett_changes[i])
    ratio_fast_finish.append(counter_fast_finish[i] / counter_total_finish[i])
print(avarage_time_w_sol)
print(avarage_time_wo_sol)
print(avarage_changes)
print(ratio_fast_finish)

# sol_exists_not_found.append(solution_exists_but_not_found)

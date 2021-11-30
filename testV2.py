# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from game import *
from agent import Agent
from app import *
from algorithmsV2 import *
import heapdict

appr = 1.5
players = [Agent("a0", [546, 553, 682], 44),
           Agent("a1", [239, 643, 711], 40),
           Agent("a2", [72, 690, 696], 36),
           Agent("a3", [155, 158, 510], 66),
           Agent("a4", [52, 438, 611], 14),
           Agent("a5", [89, 93, 683], 71),
           Agent("a6", [429, 620, 679], 8),
           Agent("a7", [64, 419, 710], 117),
           Agent("a8", [21, 358, 392], 117)]
directions = [0, 1, 0, 1, 0, 0, 1, 0, 1]
solutions = [[players[6], players[5]],
             [players[1], players[7], players[4]],
             [players[8], players[3]],
             [players[2]],
             [players[0]]]

app = App(0)

'''
# for game in all_directions_games(players, bids, solutions):
game = Game(players, (1, 1, 1), bids, solutions)
# for trees in game.compute_all_trees():
trees = game.compute_all_trees()[0]
tree = list(elaborate_trees(trees))[0]
# for tree in list(elaborate_trees(trees)):
app.add_frame(str(game.directions).replace(": 0", ": out").replace(": 1", ": in"))
print_node_on_frame(tree, app.frame[-1])



app.MainLoop()
'''
# testing search of incomplete nodes:
game = Game(players, directions, solutions)
tree = next(possible_queries(players, game.directions, game.domains, solutions), None)
if tree is None:
    tree = next(possible_queries(players, game.directions, game.domains, solutions, appr=appr), None)
tree = v2.fill_tree(tree, game.directions, tree.domains, game.players, des_appr=appr)
print_node_on_frame(tree, app.frame[-1])
new_tree, changes = euch_search(tree, game, appr)
if new_tree is None:
    print("non è stata trovata una soluzione")
else:
    print("sono stati effettuati " + str(changes) + " cambi di direzione")
    app.add_frame(str(game.directions).replace(": 0", ": out").replace(": 1", ": in"))
    print_node_on_frame(new_tree, app.frame[-1])

app.MainLoop()


# Press the green button in the gutter to run the script.
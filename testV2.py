# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from game import *
from agent import Agent
from app import *
import algorithmsV2 as v2
import heapdict

appr = 1.1
players = [Agent("a0", [9, 10, 14], 10),
           Agent("a1", [7, 8, 15], 7),
           Agent("a2", [3, 9, 14], 9),
           Agent("a3", [4, 7, 12], 4)]
directions = [0, 1, 0, 1]
solutions = [[players[0]],
             [players[1]],
             [players[2], players[3]]]

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
app.add_frame(str(game.directions).replace(": 0", ": out").replace(": 1", ": in"))
print_node_on_frame(tree, app.frame[-1])
new_tree, changes = v2.euch_search(tree, game, appr)
if new_tree is None:
    print("not solution found")
else:
    print("Have been made " + str(changes) + " changes")
    app.add_frame(str(game.directions).replace(": 0", ": out").replace(": 1", ": in"))
    print_node_on_frame(new_tree, app.frame[-1])

app.MainLoop()


# Press the green button in the gutter to run the script.
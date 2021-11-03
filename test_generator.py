from random import *
from agent import Agent
import itertools as it

def remove_sublists(lists):
    for list1, list2 in it.permutations(lists,2):
        if set(list1) <= set(list2):
            if list1 in lists:
                lists.remove(list1)
    return

def generate():
    n_domains = randrange(3) + 3
    n_players = randrange(3) + 3
    n_solutions = randrange(5) + 2
    domains = []
    players = []
    solutions = []

    for _ in range(n_domains):
        domains.append(randrange(150))
    domains = sorted(domains)

    for i in range(n_players):
        players.append(Agent("a" + str(i), domains, domains[0]))

    for _ in range(n_solutions):
        solution = []
        for player in players:
            if randrange(n_players) < 1:
                solution.append(player)
        solutions.append(solution)
    for player in players:
        if all(player not in solution for solution in solutions):
            solutions[randrange(n_solutions)].append(player)
    for solution in solutions:
        if not solution:
            solution.append(players[randrange(n_players)])
    remove_sublists(solutions)
    directions = [randrange(2) for _ in range(n_players)]
    return domains, players, directions, solutions

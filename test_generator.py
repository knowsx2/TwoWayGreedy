from random import *
from agent import Agent
from game import filter_solutions
import itertools as it

def remove_sublists(lists):
    for list1, list2 in it.permutations(lists,2):
        if set(list1) <= set(list2):
            if list1 in lists:
                lists.remove(list1)
    return

def generate():
    n_domains = randrange(7) + 3
    n_players = randrange(8) + 3
    n_solutions = randrange(9) + 2
    domains = []
    players = []
    solutions = []

    for _ in range(n_domains):
        domains.append(choice([i for i in range(1, n_players*2*n_domains*2*n_solutions) if i not in domains]))
    domains = sorted(domains)

    for i in range(n_players):
        players.append(Agent("a" + str(i), domains, domains[0]))

    while len(solutions) < 2:
        for _ in range(n_solutions):
            solution = []
            for player in players:
                if randrange(n_players) < 1 and len(solution) < n_players-2:
                    solution.append(player)
            solutions.append(solution)
        for solution in solutions:
            if not solution:
                for player in players:
                    if randrange(n_players) < 1 and len(solution) < n_players - 2:
                        solution.append(player)

        new_sol=[x for x in solutions if len(x) < n_players-2]
        for player in players:
            if all(player not in solution for solution in solutions):
                new_sol[randrange(len(new_sol))].append(player)

        remove_sublists(solutions)
        solutions, players = filter_solutions({players[i]: players[i].domain for i in range(len(players))}, solutions)

    directions = [randrange(2) for _ in range(len(players))]
    return domains, players, directions, solutions

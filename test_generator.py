from random import *
from agent import Agent
from game import filter_solutions
import itertools as it


def remove_sublists(lists):
    for list1, list2 in it.permutations(lists, 2):
        if set(list1) <= set(list2):
            if list1 in lists:
                lists.remove(list1)
    return lists


def generate():
    n_solutions = randrange(10) + 2
    n_players = randrange(11) + 3
    domains = []
    players = []
    solutions = []

    for _ in range(n_players):
        domain = []
        n_domains = randrange(11) + 3
        for _ in range(n_domains):
            domain.append(choice([i for i in range(1, n_players * n_domains * 2 * n_solutions) if i not in domain]))
        domain = sorted(domain)
        domains.append(domain)

    for i in range(n_players):
        players.append(Agent("a" + str(i), domains[i], domains[i][0]))

    while len(solutions) < 2:
        for _ in range(n_solutions):
            solution = []
            for player in players:
                if randrange(n_players) < 1 and len(solution) < n_players - 2:
                    solution.append(player)
            solutions.append(solution)
        for solution in solutions:
            if not solution:
                for player in players:
                    if randrange(n_players) < 1 and len(solution) < n_players - 2:
                        solution.append(player)

        for player in players:
            if all(player not in solution for solution in solutions):
                min(solutions, key=lambda x: len(x)).append(player)

        solutions = remove_sublists(solutions)
        solutions, players = filter_solutions({players[i]: players[i].domain for i in range(len(players))}, solutions)
        if not players:
            for i in range(n_players):
                players.append(Agent("a" + str(i), domains[i], domains[i][0]))

    directions = [randrange(2) for _ in range(len(players))]
    return players, directions, solutions

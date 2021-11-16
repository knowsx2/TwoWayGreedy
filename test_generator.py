from random import *
from agent import Agent
from game import filter_solutions
import itertools as it


def remove_sublists(lists):
    for list1, list2 in it.permutations(lists, 2):
        if set(list1) <= set(list2):
            if list1 in lists:
                lists.remove(list1)
    return


def generate():
    n_solutions = randrange(12) + 6
    n_players = randrange(10) + 10
    domains = []
    players = []
    solutions = []

    '''
    ********** Equal domains for agents **********
    domain = []
    for _ in range(3):
        domain.append(choice([i for i in range(1, n_players * 3 * 2 * n_solutions) if i not in domain]))
    for _ in range(n_players):
        domains.append(domain)
    '''
    for _ in range(n_players):
        domain = []
        n_domains = 5
        for _ in range(n_domains):
            domain.append(choice([i for i in range(1, n_players * n_domains * 2 * n_solutions) if i not in domain]))
        domain = sorted(domain)
        domains.append(domain)

    while len(solutions) < 2 or len(players) < 5:
        solutions = []
        players = []
        for i in range(n_players):
            players.append(Agent("a" + str(i), domains[i], domains[i][0]))
        for _ in range(n_solutions):
            solution = sample(players, randrange(1, n_players))
            solutions.append(solution)
        remove_sublists(solutions)
        solutions, players = filter_solutions({players[i]: players[i].domain for i in range(n_players)}, solutions)

    directions = [randrange(2) for _ in range(len(players))]
    return players, directions, solutions

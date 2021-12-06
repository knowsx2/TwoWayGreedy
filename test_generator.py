from random import *
from agent import Agent
from game import filter_solutions
import itertools as it
import math

def remove_sublists(lists):
    for list1, list2 in it.permutations(lists, 2):
        if set(list1) <= set(list2):
            if list1 in lists:
                lists.remove(list1)
    return


def generate(n_players=None, n_solutions=None, len_domain=None):
    if n_players is None:
        n_players = randrange(5, 11)
    if n_solutions is None:
        n_solutions = 5
    if len_domain is None:
        len_domain = 3
    domains = []
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
        for j in range(len_domain):
            domain.append(choice([i for i in range(1, (j+1)*100) if i not in domain]))
        domain = sorted(domain)
        domains.append(domain)

    new_players = []
    while len(solutions) < 2 or len(new_players) != n_players:
        solutions = []
        players = []
        for i in range(n_players):
            players.append(Agent("a" + str(i), domains[i], domains[i][0]))
        for _ in range(n_solutions):
            solution = sample(players, randrange(1, math.ceil(n_players/n_solutions)+1))
            solutions.append(solution)
        remove_sublists(solutions)
        solutions, new_players = filter_solutions({players[i]: players[i].domain for i in range(n_players)}, solutions)
        if len(solutions) < 2:
            continue
        eliminated = set(players)-set(new_players)
        for player in eliminated:
            new_players.append(player)
            solutions.append([player])
        #remove_sublists(solutions)
        #solutions, new_players = filter_solutions({new_players[i]: new_players[i].domain for i in range(n_players)},
        #                                              solutions)
    directions = [randrange(2) for _ in range(len(new_players))]
    return new_players, directions, solutions

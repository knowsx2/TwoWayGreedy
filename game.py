import itertools as it
from node import Node
import copy
from builtins import sum, max, min


class Game:
    def __init__(self, players, directions, solutions):
        self.players = players
        self.directions = {players[i]: directions[i] for i in range(len(players))}
        self.domains = {players[i]: players[i].domain for i in range(len(players))}
        self.solutions = solutions
        # self.directions[player] : the in (1) or out (0) question for each agent

    def compute_all_trees(self):
        return list(trees(self.players, self.directions, self.domains, self.solutions))

    def __str__(self):
        string = "dms: " + str(self.domains) + " | " + "dirs: " + str(self.directions) + " | " + "sol: " \
                 + str(self.solutions)
        return string


def elaborate_trees(node):
    if node is None:
        return [node]
    if node.no is None and node.yes is None:
        return [node]
    nodes = []
    couples = list(it.product(node.no, node.yes))
    for couple in couples:
        for no_child in elaborate_trees(couple[0]):
            for yes_child in elaborate_trees(couple[1]):
                node_copy = copy.copy(node)
                node_copy.no = no_child
                node_copy.yes = yes_child
                if no_child is not None:
                    no_child.parent = node_copy
                if yes_child is not None:
                    yes_child.parent = node_copy
                nodes.append(node_copy)
    return nodes


def filter_solutions(domains, old_solutions):
    new_solutions = copy.copy(old_solutions)
    for sol1, sol2 in it.permutations(old_solutions, 2):
        sum1 = sum([min(domains[agent]) for agent in sol1])
        sum2 = sum([min(domains[agent]) if agent in sol1 else max(domains[agent]) for agent in sol2])
        if sum1 >= sum2 and sol2 in new_solutions:
            new_solutions.remove(sol2)
    agents = []
    for sol in new_solutions:
        for agent in sol:
            if agent not in agents:
                agents.append(agent)
    agents = sorted(agents, key=lambda x: int(x.name[1:]))
    return new_solutions, agents


def trees(players, directions, domains, solutions, appr=1):
    '''
    def check_solutions(domains, old_solutions):
        solutions = copy.copy(old_solutions)
        if len(solutions) <= 1:
            return solutions
        _players = []
        for player in players:
            if any(player not in sol for sol in solutions):
                _players.append(player)
        maximum = [sum(max(domains[agent]) for agent in sol if agent in _players) for sol in solutions]
        i = 0
        for sol in solutions:
            summ = 0
            for agent in sol:
                summ += min(domains[agent]) if agent in _players else 0
            if all(summ >= boh for boh in maximum[:i] + maximum[i + 1:]):
                return [sol]
            i += 1
        return solutions
    '''

    solutions, surv_agents = filter_solutions(domains, solutions)
    # solutions = check_solutions(domains, solutions)
    if len(solutions) <= 1:
        yield Node(solutions, ro=1)
    else:
        new_players = []

        for player in players:
            if player in surv_agents:
                new_players.append(player)
                # domains.pop(player)
        for node in list(possible_queries(new_players, directions, domains, solutions, appr)):
            # "no" side of node
            no_domains = copy.copy(domains)
            no_players = copy.copy(players)
            no_solutions = copy.copy(solutions)
            no_directions = copy.copy(directions)
            if node.direction is not directions[node.player]:
                # interleaving
                no_directions[node.player] = node.direction
                no_domains[node.player] = [domains[node.player][-1]] if directions[node.player] \
                    else [domains[node.player][0]]
            else:
                no_domains[node.player] = no_domains[node.player][:-1] if directions[node.player] else \
                    no_domains[node.player][1:]  # reduce sub domain
            if not no_domains[node.player]:
                no_players.remove(node.player)
                no_domains.pop(node.player)
                no_solutions = [solution for solution in solutions if node.player not in solution]
            no_solutions, surv_agents = filter_solutions(no_domains, no_solutions)
            # no_solutions = check_solutions(no_domains, no_solutions)

            node.no = list(trees(no_players, no_directions, no_domains, no_solutions, appr=appr))
            if not node.no:
                node.no = [None]
            # "yes" side of node
            P_t = [solution for solution in solutions if node.player in solution] if node.direction else \
                [solution for solution in solutions if node.player not in solution]
            if not P_t:
                # there aren't suitable solutions
                pass
            else:
                yes_players = copy.copy(players)
                yes_solutions = P_t
                yes_domains = copy.copy(domains)
                yes_domains[node.player] = [node.bid]
                # yes_players.remove(node.player)
                yes_solutions, surv_agents = filter_solutions(yes_domains, yes_solutions)
                # yes_solutions = check_solutions(yes_domains, yes_solutions)
                node.yes = list(trees(yes_players, directions, yes_domains, yes_solutions, appr * node.ro))
                if not node.yes:
                    node.yes = [None]
            yield node


def all_directions_games(players, solutions):
    directions = list(it.product([0, 1], repeat=len(players)))
    for direction in directions:
        yield Game(players, direction, solutions)


def possible_queries(players, directions, domains, solutions, appr=1):
    def is_query_possible(node):
        def in_val(sol):
            value = 0
            for agent in sol:
                if agent is player:
                    value += bid
                else:
                    value += domains[agent][0]
            return value

        def out_val(sol):
            value = 0
            for agent in sol:
                if agent is player:
                    value += bid
                else:
                    value += domains[agent][-1]
            return value

        def a_sum(sol):
            value = 0
            if dire:
                for agent in sol:
                    if agent in worst:
                        value += domains[agent][0]
                    else:
                        value += domains[agent][-1]
            else:
                for agent in sol:
                    if agent in best:
                        value += domains[agent][-1]
                    else:
                        value += domains[agent][0]
            return value

        if node.direction:
            worst = min([solution for solution in node.solutions if node.player in solution], key=in_val)
            best = max([solution for solution in node.solutions if node.player not in solution], key=a_sum)
            if in_val(worst) >= (1 / appr) * a_sum(best):
                if in_val(worst) / a_sum(best) < 1:
                    return True, in_val(worst) / a_sum(best)
                else:
                    return True, 1
            else:
                return False, 1

        else:
            best = max([solution for solution in node.solutions if node.player in solution], key=out_val)
            worst = min([solution for solution in node.solutions if node.player not in solution], key=a_sum)
            if a_sum(worst) >= (1 / appr) * out_val(best):
                if a_sum(worst) / out_val(best) < 1:
                    return True, a_sum(worst) / out_val(best)
                else:
                    return True, 1
            else:
                return False, 1

    fl_inter = True
    for player in players:
        if all(player in sol for sol in solutions) or len(domains[player]) == 1:
            continue
        dire = directions[player]
        bid = domains[player][-1] if dire else domains[player][0]
        node = Node(solutions, player, dire, bid, domains)
        is_possible, ro = is_query_possible(node)
        if is_possible:
            node.ro = ro
            fl_inter = False
            yield node

    if fl_inter:
        for player in players:
            if all(player in sol for sol in solutions):
                continue
            if len(domains[player]) >= 2:
                dire = 1 - directions[player]
                bid = domains[player][-2] if directions[player] else domains[player][1]
                node = Node(solutions, player, dire, bid, domains)
                is_possible, ro = is_query_possible(node)
                if is_possible:
                    node.ro = ro
                    yield node


def check_solutioned_tree(node):
    if node.player is None:
        return True
    if node.no is None or node.yes is None:
        return False
    if node.no.player is None and node.yes.player is None:
        return True
    return check_solutioned_tree(node.no) and check_solutioned_tree(node.yes)

def check_if_sol_exists(list):
    for node in list:
        if node.player is None:
            return True
        if all(x is None for x in node.no) or all(x is None for x in node.yes):
            continue
        return check_if_sol_exists(node.no) and check_if_sol_exists(node.yes)
    return False
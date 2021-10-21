import itertools as it
from node import Node
import copy
from builtins import sum, max, min


class Game:
    def __init__(self, players, directions, bids, solutions):
        self.bids = sorted(bids)
        self.players = players
        self.directions = {players[i]: directions[i] for i in range(len(players))}
        self.domains = {players[i]: players[i].domain for i in range(len(players))}
        self.solutions = solutions
        # self.directions[player] : the in (1) or out (0) question for each agent

    def compute_all_trees(self):
        return list(trees(self.players, self.directions, self.domains, self.solutions))

    def __str__(self):
        string = "bid: " + str(self.bids) + " | " + "sol: " + str(self.solutions) + " | " + "ply: " + str(self.players) \
                 + " | " + "dirs: " + str(self.directions) + " | " + "dms: " + str(self.domains)
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


def trees(players, directions, domains, solutions):
    def check_solutions(domains, solutions):
        if len(solutions) <= 1:
            return solutions
        _players = copy.copy(players)
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

    def filter_solutions(domains, solutions):
        if len(solutions) <= 1:
            return solutions, None
        _players = copy.copy(players)
        for player in players:
            if any(player not in sol for sol in solutions):
                _players.append(player)
        minimum = [sum(min(domains[agent]) for agent in sol if agent in _players) for sol in solutions]
        i = 0
        for sol in solutions:
            summ = 0
            for agent in sol:
                summ += max(domains[agent]) if agent in _players else 0
            if any(summ <= boh for boh in minimum[:i] + minimum[i + 1:]):
                solutions.remove(sol)
                minimum = minimum[:i] + minimum[i + 1:]
            i += 1
        agents = []
        for sol in solutions:
            for agent in sol:
                if agent not in agents:
                    agents.append(agent)
        return solutions, agents

    solutions, surv_agents = filter_solutions(domains, solutions)
    solutions = check_solutions(domains, solutions)
    if len(solutions) <= 1:
        yield Node(solutions)
    else:
        if surv_agents is not None:
            for player in players:
                if player not in surv_agents:
                    players.remove(player)
                    domains.pop(player)
        for node in list(possible_queries(players, directions, domains, solutions)):
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
            #elif len(no_domains[node.player]) == 1:
             #   no_solutions = check_solutions(no_domains, solutions)
                # no_players.remove(node.player)

            node.no = list(trees(no_players, no_directions, no_domains, no_solutions))
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
                #yes_players.remove(node.player)
                node.yes = list(trees(yes_players, directions, yes_domains, yes_solutions))
                if not node.yes:
                    node.yes = [None]
            yield node


def all_directions_games(players, bids, solutions):
    directions = list(it.product([0, 1], repeat=len(players)))
    for direction in directions:
        yield Game(players, direction, bids, solutions)


def possible_queries(players, directions, domains, solutions):
    def is_query_possible(node):
        def in_val(sol):
            value = 0
            for agent in sol:
                if agent is player:
                    value += bid
                elif agent in considered_agents:
                    value += domains[agent][-1]
                else:
                    value += domains[agent][0]
            return value

        def out_val(sol):
            value = 0
            for agent in sol:
                if agent is player:
                    value += bid
                elif agent in considered_agents:
                    value += domains[agent][0]
                else:
                    value += domains[agent][-1]
            return value

        def a_sum(sol):
            value = 0
            if dire:
                for agent in sol:
                    value += domains[agent][-1]
            else:
                for agent in sol:
                    value += domains[agent][0]
            return value

        considered_agents = []
        for sol in node.solutions:
            if node.player not in sol:
                considered_agents += [agent for agent in sol if agent not in considered_agents]
        if node.direction:
            best = max([solution for solution in node.solutions if node.player not in solution], key=a_sum)
            worst = min([solution for solution in node.solutions if node.player in solution], key=in_val)
            return True if in_val(worst) >= a_sum(best) else False
        else:
            worst = min([solution for solution in node.solutions if node.player not in solution], key=a_sum)
            best = max([solution for solution in node.solutions if node.player in solution], key=out_val)
            return True if a_sum(worst) >= out_val(best) else False

    fl_inter = True
    for player in players:
        if all(player in sol for sol in solutions) or len(domains[player]) == 1:
            continue
        dire = directions[player]
        bid = domains[player][-1] if dire else domains[player][0]
        node = Node(solutions, player, dire, bid)
        if is_query_possible(node):
            fl_inter = False
            yield node

    if fl_inter:
        for player in players:
            if all(player in sol for sol in solutions):
                continue
            if len(domains[player]) >= 2:
                dire = 1 - directions[player]
                bid = domains[player][-2] if directions[player] else domains[player][1]
                node = Node(solutions, player, dire, bid)
                if is_query_possible(node):
                    yield node


def check_solutioned_tree(node):
    if node.player is None:
        return True
    if node.no is None or node.yes is None:
        return False
    if node.no.player is None and node.yes.player is None:
        return True
    return check_solutioned_tree(node.no) and check_solutioned_tree(node.yes)

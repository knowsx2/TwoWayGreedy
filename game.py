import itertools as it
from node import Node
import copy


# escludere gli alberi che non danno soluzioni ottimali (se includo qualcuno la peggior soluzione in cui è presente
# deve essere migliore di tutte le altre in cui non è presente). Questa cosa tiene conto dei sub domini, ovvero se
# qualcuno risponde no, la bid non farà più parte del suo dominio

# l'ordine degli agenti non si alterna per forza

# la stessa bid può essere fatta da più agenti
class Game:
    def __init__(self, players, directions, bids, solutions):
        self.bids = sorted(bids)
        self.players = players
        self.directions = {players[i]: directions[i] for i in range(len(players))}
        self.domains = {players[i]: players[i].domain for i in range(len(players))}
        self.solutions = solutions
        # self.directions[player] = 1  # the in (1) or out (0) question for each agent

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
                node_copy = copy.deepcopy(node)
                node_copy.no = no_child
                node_copy.yes = yes_child
                nodes.append(node_copy)
    return nodes


def trees(players, directions, domains, solutions):
    if len(solutions) <= 1:
        yield Node(solutions)
    else:
        for node in list(possible_queries(players, directions, domains, solutions)):
            # "no" side of node
            no_domains = copy.copy(domains)
            no_players = copy.copy(players)
            no_domains[node.player] = no_domains[node.player][:-1] if directions[node.player] else \
                no_domains[node.player][1:]  # reduce sub domain
            no_solutions = copy.copy(solutions)
            if not no_domains[node.player]:
                no_players.remove(node.player)
                no_domains.pop(node.player)
                no_solutions = [solution for solution in solutions if node.player not in solution]

            node.no = list(trees(no_players, directions, no_domains, no_solutions))
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
                yes_domains.pop(node.player)
                yes_players.remove(node.player)
                node.yes = list(trees(yes_players, directions, yes_domains, yes_solutions))
                if not node.yes:
                    node.yes = [None]
            yield node


def all_directions_games(players, bids, solutions):
    directions = list(it.product([0, 1], repeat=len(players)))
    for direction in directions:
        yield Game(players, direction, bids, solutions)


def possible_queries(players, directions, domains, solutions):
    def in_val(sol):
        value = 0
        for agent in sol:
            value += domains[agent][-1] if agent is player else domains[agent][0]
        return value

    def out_val(sol):
        value = 0
        for agent in sol:
            value += domains[agent][0] if agent is player else domains[agent][-1]
        return value

    def a_sum(sol):
        value = 0
        if directions[player]:
            for agent in sol:
                value += domains[agent][-1]
        else:
            for agent in sol:
                value += domains[agent][0]
        return value

    for player in players:
        if directions[player]:
            bid = domains[player][-1]
            wrost = min([solution for solution in solutions if player in solution], key=in_val)
            best = max([solution for solution in solutions if player not in solution], key=a_sum)
            if in_val(wrost) > a_sum(best):
                yield Node(solutions, player, directions[player], bid)

        else:
            bid = domains[player][0]
            wrost = min([solution for solution in solutions if player not in solution], key=a_sum)
            best = max([solution for solution in solutions if player in solution], key=out_val)
            if a_sum(wrost) > out_val(best):
                yield Node(solutions, player, directions[player], bid)


def is_query_possible(directions, node):
    if directions[node.player]:
        wrost = min([solution for solution in node.solutions if node.player in solution], key=in_val)
        best = max([solution for solution in node.solutions if node.player not in solution], key=a_sum)
        return True if in_val(wrost) > in_val(best) else False
    else:
        wrost = min([solution for solution in node.solutions if node.player not in solution], key=a_sum)
        best = max([solution for solution in node.solutions if node.player in solution], key=out_val)
        return True if a_sum(wrost) > out_val(best) else False

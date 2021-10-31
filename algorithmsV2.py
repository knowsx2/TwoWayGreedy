import copy
from bisect import insort
from game import *
import heapdict
from collections import Counter


def twowaygreedy(agents, solutions):
    P = solutions
    I = set()
    A = agents
    while len(P) > 1:
        i_in = max(enumerate(A.difference(I)), key=lambda x: x[1].domain[-1])[1]  # ritorna l'agente col massimo dominio
        i_out = min(enumerate(A.difference(I)), key=lambda x: x[1].domain[0])[1]  # ritorna l'agente col minimo dominio
        i = i_in
        if i == i_in and [solution for solution in P if i in P]:
            P_in = [solution for solution in P if i in P]
            P = P_in
            A.remove(i)
        elif i == i_out and [solution for solution in P if i not in P]:
            P_out = [solution for solution in P if i not in P]
            P = P_out
            A.remove(i)
        else:
            I.add(i)
    return P.pop()


def search_last_nodes(node):
    nodes = []
    if node is None:
        return nodes
    if node.player is None:
        return nodes
    if node.no is None or node.yes is None:
        nodes.append(node)
        return nodes
    return nodes + search_last_nodes(node.no) + search_last_nodes(node.yes)


def is_ancestor(node, ancestor):
    if node.parent is None:
        return False
    if node.parent == ancestor:
        return True
    return is_anchestor(node.parent, ancestor)


def same_player_ancestor(node, domains):
    root = node
    stack = [root]
    new_domains = {key: copy.deepcopy(value) for (key, value) in domains.items()}
    while root.parent is not None:
        root = root.parent
        stack.append(root)
    while stack[-1].player != node.player:
        edon = stack.pop()
        new_domains[edon.player].remove(edon.bid)
    agents = []
    for agent, domain in new_domains.items():
        if not domain:
            new_domains.pop(agent)
        else:
            agents += [agent]
    return stack[-1], new_domains, agents


def count_appears(node):
    if node.player is None:
        return Counter()
    occurrs = Counter([node.player])
    no_occurs = Counter()
    yes_occurs = Counter()
    if node.no is None and node.yes is None:
        return occurrs
    if node.no is not None:
        no_occurs = count_appears(node.no)
    if node.yes is not None:
        yes_occurs = count_appears(node.yes)
    return occurrs + no_occurs + yes_occurs


def first_to_appears_order(node, players):

    # Base Case
    if node is None:
        return

    # Create an empty queue
    # for level order traversal
    order = []
    queue = [node]

    # Enqueue Root and initialize height

    while len(queue) > 0 or len(order) == len(players):

        # Print front of queue and
        # remove it from queue
        if queue[0].player is not None and queue[0].player not in order:
            order.append(node.player)
        # print(queue[0].data)
        node = queue.pop(0)

        # Enqueue left child
        if node.no is not None:
            queue.append(node.no)

        # Enqueue right child
        if node.yes is not None:
            queue.append(node.yes)
    return order


def player_first_nodes(node, player):
    if node is None:
        return
    if node.player == player:
        return [node]
    return player_first_nodes(node.no, player) + player_first_nodes(node.yes, player)


def euch_search(tree, game):
    def search_direction(players, forbidden):
        for direction in it.product([0, 1], repeat=len(players)):
            if list(direction) not in forbidden:
                return {players[i]: direction[i] for i in range(len(players))}
        return None

    changes = 0
    tested_directions = [[value for (_, value) in game.directions.items()]]
    while not check_solutioned_tree(tree):
        occurrences = count_appears(tree)
        occurrences.update({x: 0 for x in game.players if x not in occurrences.keys()})
        hd = heapdict.heapdict(occurrences)
        # hd is a priority queue ordered by occurrences
        ties = [hd.popitem()]  # store the items that appears equal times
        while len(hd) > 0 and hd.peekitem()[1] == ties[-1][1]:
            ties += [hd.popitem()]
        anchestors = []
        for agent in first_to_appears_order(tree, game.players):
            if agent in ties[:][0]:
                anchestors = player_first_nodes(tree, agent)
                break
        if not anchestors:
            tree.player = ties[0][0]
            anchestors.append(tree)
        for node in anchestors:
            agents = []
            for agent, domain in node.domains.items():
                if domain:
                    agents += [agent]
                else:
                    node.domains.pop(agent)
            game.directions[node.player] = 1 - game.directions[node.player]
            if [value for (_, value) in game.directions.items()] in tested_directions:
                new_directions = search_direction(game.players, tested_directions)
                if new_directions is None:
                    return None
                else:
                    for agent in game.directions.keys():
                        if game.directions[agent] != new_directions[agent]:
                            changes += 1
                    game.directions = new_directions
            else:
                changes += 1
            new = next(possible_queries(agents, game.directions, node.domains, node.solutions), None)
            if new is None and node.parent is not None:
                node.parent.no = node.parent.yes = None
                continue
            if node.parent is None:
                tested_directions += [[value for (_, value) in game.directions.items()]]
            if new is not None:
                node.change(fill_tree(new, game.directions, node.domains, agents))
    return tree, changes


# ciao
def fill_tree(node, directions, domains, players):
    def check_solutions(domains, solutions):
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

    no_domains = copy.copy(domains)
    no_players = copy.copy(players)
    no_solutions = copy.copy(node.solutions)
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
        no_solutions = [solution for solution in node.solutions if node.player not in solution]
    # elif len(no_domains[node.player]) == 1:
    #   no_solutions = check_solutions(no_domains, solutions)
    # no_players.remove(node.player)
    no_solutions, surv_agents = filter_solutions(no_domains, no_solutions)
    no_solutions = check_solutions(no_domains, no_solutions)
    if len(no_solutions) <= 1:
        node.no = Node(no_solutions)
    else:
        if surv_agents is not None:
            for player in no_players:
                if player not in surv_agents:
                    no_players.remove(player)
                    no_domains.pop(player)
        node.no = next(possible_queries(no_players, no_directions, no_domains, no_solutions), None)
        if node.no is not None:
            node.no.parent = node
            fill_tree(node.no, no_directions, no_domains, no_players)

    # "yes" side of node
    P_t = [solution for solution in node.solutions if node.player in solution] if node.direction else \
        [solution for solution in node.solutions if node.player not in solution]
    if not P_t:
        # there aren't suitable solutions
        pass
    else:
        yes_players = copy.copy(players)
        yes_solutions = P_t
        yes_domains = copy.copy(domains)
        yes_domains[node.player] = [node.bid]
        # yes_players.remove(node.player)
        if len(yes_solutions) == 1:
            node.yes = Node(yes_solutions)
        else:
            node.yes = next(possible_queries(yes_players, directions, yes_domains, yes_solutions), None)
            if node.yes is not None:
                node.yes.parent = node
                fill_tree(node.yes, directions, yes_domains, yes_players)
    return node

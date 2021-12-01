import copy
from game import *
import heapdict


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
    return is_ancestor(node.parent, ancestor)


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
            if any(agent in sol for sol in stack[-1].solutions):
                agents += [agent]
    return stack[-1], new_domains, agents


def player_first_nodes(node, player):
    if node is None:
        return []
    if node.player == player:
        return [node]
    return player_first_nodes(node.no, player) + player_first_nodes(node.yes, player)


def old_search_direction(av_dir, last):
    if not av_dir:
        return None
    diffs = heapdict.heapdict()
    for direction in av_dir:
        diffs[direction] = sum([abs(direction[i] - last[i]) for i in range(len(last))])
        if diffs[direction] <= 1:
            return direction
    return list(diffs.popitem()[0])


def search_direction(av_dir, last):
    if not av_dir:
        return None
    queue = [last]
    viewed = set()
    while queue:
        current = queue.pop()
        for i in range(len(current)):
            new_dir = copy.copy(current)
            new_dir[i] = 1 - new_dir[i]
            if tuple(new_dir) in viewed:
                continue
            if tuple(new_dir) in av_dir:
                return new_dir
            queue.append(new_dir)
            viewed.add(tuple(new_dir))
    return None


def compute_node_appr(node, des_appr=1):
    up_node = node
    # n_appr represents the available utility remaining after the node,
    # it needs to not subscribe des_appr that represent the desired approximation of mechanism
    n_appr = des_appr * node.ro
    while up_node.parent is not None:
        if up_node == up_node.parent.yes:
            n_appr *= up_node.parent.ro
        up_node = up_node.parent
    return n_appr


def euch_search(tree, game, des_appr=1):
    changes = {x: 0 for x in game.players}
    # tested_directions = [[value for (_, value) in game.directions.items()]]
    av_dir = set(it.product([0, 1], repeat=len(game.players)))
    av_dir.remove(tuple(value for (_, value) in game.directions.items()))
    while not check_solutioned_tree(tree):
        nodes = search_last_nodes(tree)
        anchestors = []
        last_directions = copy.copy(game.directions)
        new_directions = copy.copy(game.directions)
        change_agents = []
        for node in nodes:
            if node.player not in change_agents:
                change_agents.append(node.player)
        for player in change_agents:
            new_directions[player] = 1 - new_directions[player]
            anchestors += player_first_nodes(tree, player)
        if tuple([value for (_, value) in new_directions.items()]) not in av_dir:
            dir = search_direction(av_dir, list(last_directions.values()))
            if dir is None:
                return None, changes
            else:
                new_directions = {game.players[i]: dir[i] for i in range(len(game.players))}
                change_agents = [agent for agent in list(new_directions.keys()) if
                                 last_directions[agent] != new_directions[agent]]
                anchestors = []
                for player in change_agents:
                    anchestors += player_first_nodes(tree, player)
                for node in nodes:
                    if all([not is_ancestor(node, anch) for anch in anchestors]):
                        anchestors += [node]
        for agent in new_directions.keys():
            if last_directions[agent] != new_directions[agent]:
                changes[agent] += 1
        # tested_directions += [[value for (_, value) in last_directions.items()]]
        av_dir.remove(tuple([value for (_, value) in new_directions.items()]))
        game.directions = new_directions
        for node in anchestors:
            new_node = next(possible_queries(list(node.domains.keys()), game.directions, node.domains, node.solutions),
                            None)
            if new_node is None:
                new_node = next(
                    possible_queries(list(node.domains.keys()), game.directions, node.domains, node.solutions,
                                     compute_node_appr(node, des_appr)), None)
            if new_node is None and node.parent is not None:
                node.parent.no = node.parent.yes = None
                continue
            if new_node is not None:
                node.change(fill_tree(new_node, game.directions, new_node.domains, list(new_node.domains.keys()),
                                      des_appr))
    return tree, changes


# ciao
def fill_tree(node, directions, domains, players, des_appr=1):
    solutions, surv_agents = filter_solutions(node.domains, node.solutions)
    # solutions = check_solutions(node.domains, solutions)
    if len(solutions) <= 1:
        return Node(solutions, ro=1)
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
    # no_solutions = check_solutions(no_domains, no_solutions)
    if len(no_solutions) <= 1:
        node.no = Node(no_solutions, ro=1)
    else:
        if surv_agents is not None:
            no_players = copy.copy(surv_agents)
            no_domains = {agent: no_domains[agent] for agent in no_players}
        node.no = next(possible_queries(no_players, no_directions, no_domains, no_solutions), None)
        if node.no is None:
            node.no = next(possible_queries(no_players, no_directions, no_domains, no_solutions, des_appr), None)
        if node.no is not None:
            node.no.parent = node
            fill_tree(node.no, no_directions, no_domains, no_players, des_appr)

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
        yes_directions = copy.copy(directions)
        yes_domains[node.player] = [node.bid]
        if node.direction is not directions[node.player]:
            # interleaving
            yes_directions[node.player] = node.direction

        yes_solutions, surv_agents = filter_solutions(yes_domains, yes_solutions)
        # yes_solutions = check_solutions(yes_domains, yes_solutions)
        if len(yes_solutions) <= 1:
            node.yes = Node(yes_solutions, ro=1)
        else:
            if surv_agents is not None:
                yes_players = copy.copy(surv_agents)
                yes_domains = {agent: yes_domains[agent] for agent in yes_players}

            node.yes = next(possible_queries(yes_players, yes_directions, yes_domains, yes_solutions), None)
            if node.yes is None:
                node.yes = next(
                    possible_queries(yes_players, yes_directions, yes_domains, yes_solutions, compute_node_appr(node, des_appr)), None)
            if node.yes is not None:
                node.yes.parent = node
                fill_tree(node.yes, directions, yes_domains, yes_players, des_appr)
    return node

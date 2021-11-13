from collections import Counter
from algorithms import *


# Cambia il nodo che ha cambiato meno e in caso di parità quello che ha effettuato il primo cambio per ultimo
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

    while len(queue) > 0 and len(order) < len(players):

        # Print front of queue and
        # remove it from queue
        if queue[0].player is not None and queue[0].player not in order:
            order.append(queue[0].player)
        # print(queue[0].data)
        node = queue.pop(0)

        # Enqueue left child
        if node.no is not None:
            queue.append(node.no)

        # Enqueue right child
        if node.yes is not None:
            queue.append(node.yes)
    return order

def changing_order(tree, game, flag=True):
    order = []
    occurrences = count_appears(tree)
    occurrences.update(
        {x: 0 for x in game.players if x not in occurrences.keys() and not all(x in sol for sol in tree.solutions)})
    hd = heapdict.heapdict(occurrences)
    # hd is a priority queue ordered by occurrences
    # store the items that appears equal times
    ties = [hd.popitem()]
    if ties[0][1] == 0:
        while len(hd) > 0 and hd.peekitem()[1] == ties[-1][1]:
            ties += [hd.popitem()]
    for couple in ties[:]:
        order.append(couple[0])
    if len(hd) > 0:
        ties = [hd.popitem()]
    while len(hd) > 0 and hd.peekitem()[1] == ties[-1][1]:
        ties += [hd.popitem()]
    for agent in first_to_appears_order(tree, game.players)[::-1]:
        if agent in ties[:][0]:
            order.append(agent)
    return order if flag else order[::-1]

def euch_search(tree, game, flag=True):
    changes = {x: 0 for x in game.players}
    #tested_directions = [[value for (_, value) in game.directions.items()]]
    last_agent_changed = None
    av_dir = set(it.product([0, 1], repeat=len(game.directions.keys())))
    av_dir.remove(tuple(value for (_, value) in game.directions.items()))
    while not check_solutioned_tree(tree):
        last_directions = copy.copy(game.directions)
        new_directions = copy.copy(game.directions)
        anchestors = []
        order_to_change = changing_order(tree, game, flag)
        for agent in order_to_change:
            if last_agent_changed is None or agent != last_agent_changed:
                agent_to_change = agent
                last_agent_changed = agent
                break
        new_directions[agent_to_change] = 1 - new_directions[agent_to_change]
        if tuple([value for (_, value) in new_directions.items()]) not in av_dir:
            dir = search_direction(av_dir, list(last_directions.values()))
            if dir is None:
                return None, changes
            else:
                new_directions = {game.players[i]: dir[i] for i in range(len(game.players))}
                change_agents = [agent for agent in list(new_directions.keys()) if last_directions[agent] != new_directions[agent]]
                for player in change_agents:
                    anchestors += player_first_nodes(tree, player)

        elif agent_to_change in first_to_appears_order(tree, game.players):
            anchestors += player_first_nodes(tree, agent_to_change)
        last_nodes = search_last_nodes(tree)
        anchestors += [x for x in last_nodes if x not in anchestors and all([not is_ancestor(x, k) for k in anchestors])]
        for agent in new_directions.keys():
            if last_directions[agent] != new_directions[agent]:
                changes[agent] += 1
        #tested_directions += [[value for (_, value) in new_directions.items()]]
        av_dir.remove(tuple(value for (_, value) in new_directions.items()))
        game.directions = new_directions

        for node in anchestors:
            new = next(possible_queries(list(node.domains.keys()), game.directions, node.domains, node.solutions), None)
            if new is None and node.parent is not None:
                node.parent.no = node.parent.yes = None
                continue
            if new is not None:
                node.change(fill_tree(new, game.directions, node.domains, list(node.domains.keys())))
    return tree, changes

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


def euch_search(tree, game):
    def search_direction(players, forbidden):
        last = [value for (_, value) in last_directions.items()]
        diffs = heapdict.heapdict()
        for direction in it.product([0, 1], repeat=len(players)):
            diffs[direction] = sum([abs(direction[i] - last[i]) for i in range(len(last))])
        while len(diffs) > 0:
            current = diffs.popitem()[0]
            if list(current) not in forbidden:
                return {players[i]: current[i] for i in range(len(players))}
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
        last_directions = copy.copy(game.directions)
        new_directions = copy.copy(game.directions)
        for agent in first_to_appears_order(tree, game.players)[::-1]:
            if agent in ties[:][0]:
                anchestors = player_first_nodes(tree, agent)
                new_directions[agent] = 1 - new_directions[agent]
                break
        if not anchestors:
            anchestors = search_last_nodes(tree)
            new_directions[ties[0][0]] = 1 - new_directions[ties[0][0]]

        if [value for (_, value) in new_directions.items()] in tested_directions:
            new_directions = search_direction(game.players, tested_directions)
            if new_directions is None:
                return None, changes
            else:
                change_agents = [agent for agent in list(new_directions.keys()) if last_directions[agent] != new_directions[agent]]
                anchestors = []
                for player in change_agents:
                    anchestors += player_first_nodes(tree, player)
        for agent in new_directions.keys():
            if last_directions[agent] != new_directions[agent]:
                changes += 1
        tested_directions += [[value for (_, value) in last_directions.items()]]
        game.directions = new_directions

        for node in anchestors:
            new = next(possible_queries(list(node.domains.keys()), game.directions, node.domains, node.solutions), None)
            if new is None and node.parent is not None:
                node.parent.no = node.parent.yes = None
                continue
            if new is not None:
                node.change(fill_tree(new, game.directions, node.domains, list(node.domains.keys())))
    return tree, changes

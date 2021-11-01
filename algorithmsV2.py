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
        last = forbidden[-1]
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
        for agent in first_to_appears_order(tree, game.players)[::-1]:
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
            last_directions = copy.copy(game.directions)
            game.directions[node.player] = 1 - game.directions[node.player]
            if [value for (_, value) in game.directions.items()] in tested_directions:
                new_directions = search_direction(game.players, tested_directions)
                if new_directions is None:
                    return None
                else:
                    for agent in game.directions.keys():
                        if last_directions[agent] != new_directions[agent]:
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

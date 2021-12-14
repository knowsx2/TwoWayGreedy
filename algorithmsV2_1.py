from algorithmsV2 import *


# Changes the last agent to appears first

def euch_search(tree, game, des_appr=1):
    """
    Search a complete mechanism from incomplete

    Parameters
    ----------
    tree: node
        Root of a tree

    game: game

    des_appr: float
        desired approximation of the solution

    Returns
    -------
    tree: node
        the root of the new tree

    changes: dictionary
        key: agent, value: int represents the number of changes for the key player

    """
    changes = {x: 0 for x in game.players}
    last_agents_changed = []
    av_dir = set(it.product([0, 1], repeat=len(game.directions.keys())))
    av_dir.remove(tuple(value for (_, value) in game.directions.items()))
    while not check_solutioned_tree(tree):
        last_directions = copy.copy(game.directions)
        new_directions = copy.copy(game.directions)
        order_to_change = first_to_appears_order(tree, game.players)[::-1]

        for agent in order_to_change:
            if agent not in last_agents_changed:
                agent_to_change = agent
                last_agents_changed.append(agent)
                if len(last_agents_changed) == len(order_to_change):
                    last_agents_changed = [agent_to_change]
                break
        new_directions[agent_to_change] = 1 - new_directions[agent_to_change]
        anchestors = []
        if tuple([value for (_, value) in new_directions.items()]) not in av_dir:
            dir = search_direction(av_dir, list(last_directions.values()))
            if dir is None:
                return None, changes
            else:
                new_directions = {game.players[i]: dir[i] for i in range(len(game.players))}
                change_agents = [agent for agent in list(new_directions.keys()) if
                                 last_directions[agent] != new_directions[agent]]
                for player in change_agents:
                    anchestors += player_first_nodes(tree, player)
                for node in search_last_nodes(tree):
                    if all([not is_ancestor(node, anch) for anch in anchestors]):
                        anchestors += [node]
        else:
            anchestors += player_first_nodes(tree, agent_to_change)
        last_nodes = search_last_nodes(tree)
        anchestors += [x for x in last_nodes if
                       x not in anchestors and all([not is_ancestor(x, k) for k in anchestors])]
        for agent in new_directions.keys():
            if last_directions[agent] != new_directions[agent]:
                changes[agent] += 1
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
                node.change(fill_tree(new_node, game.directions, node.domains, list(node.domains.keys()), des_appr))
    return tree, changes

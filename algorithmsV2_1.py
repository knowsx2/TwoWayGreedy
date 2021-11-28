from algorithmsV2 import *


def euch_search(tree, game):

    changes = {x: 0 for x in game.players}
    #tested_directions = [[value for (_, value) in game.directions.items()]]
    last_player_changed = None
    av_dir = set(it.product([0, 1], repeat=len(game.directions.keys())))
    av_dir.remove(tuple(value for (_, value) in game.directions.items()))
    while not check_solutioned_tree(tree):
        last_directions = copy.copy(game.directions)
        new_directions = copy.copy(game.directions)

        for player in first_to_appears_order(tree, game.players)[::-1]:
            if last_player_changed is None or player != last_player_changed:
                agent = player
                last_player_changed = player
                break
        new_directions[agent] = 1 - new_directions[agent]
        anchestors = []
        if tuple([value for (_, value) in new_directions.items()]) not in av_dir:
            dir = search_direction(av_dir, list(last_directions.values()))
            if dir is None:
                return None, changes
            else:
                new_directions = {game.players[i]: dir[i] for i in range(len(game.players))}
                change_agents = [agent for agent in list(new_directions.keys()) if last_directions[agent] != new_directions[agent]]
                for player in change_agents:
                    anchestors += player_first_nodes(tree, player)
        else:
            anchestors = player_first_nodes(tree, agent)
        last_nodes = search_last_nodes(tree)
        anchestors += [x for x in last_nodes if x not in anchestors and all([not is_ancestor(x, k) for k in anchestors])]
        for agent in new_directions.keys():
            if last_directions[agent] != new_directions[agent]:
                changes[agent] += 1
        #tested_directions += [[value for (_, value) in last_directions.items()]]
        av_dir.remove(tuple([value for (_, value) in new_directions.items()]))
        game.directions = new_directions
        for node in anchestors:
            new, _ = next(possible_queries(list(node.domains.keys()), game.directions, node.domains, node.solutions), (None,1))
            if new is None and node.parent is not None:
                node.parent.no = node.parent.yes = None
                continue
            if new is not None:
                node.change(fill_tree(new, game.directions, node.domains, list(node.domains.keys())))
    return tree, changes

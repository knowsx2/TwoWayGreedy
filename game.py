import itertools as it
from node import Node


class Game:
    def __init__(self, players, bids, solutions):
        self.bids = sorted(bids)
        self.players = players
        self.directions = {}
        self.solutions = solutions
        for player in players:
            self.directions[player] = 1  # the in (1) or out (0) question for each agent

    def compute_tree(self, solutions, players, bids, a=0):
        P = solutions
        A = players
        node = Node(A[a], self.directions[A[a]], solutions=P,
                    bid=bids[-1] if self.directions[A[a]] else bids[0])
        root = node
        print(root)

        if len(solutions) <= 1:
            return root
        # A_I = [x for x in A if x not in I]  # players in A not present in I

        # "no" side of node
        if a < len(A)-1:  # otherwise it never ends
            node = self.compute_tree(P, A, bids, a + 1)
            root.no = node
            node.parent = root

        # "yes" side of node
        P_t = [solution for solution in P if root.player in solution]
        if not P_t:
            # there aren't suitable solutions
            # I.add(root.player)
            pass
        else:
            P = P_t
            bids = bids[:-1] if self.directions[A[a]] else bids[1:]
        A = A[:a] + A[a + 1:]
        node = self.compute_tree(P, A, bids)
        root.yes = node
        node.parent = root
        return root

    def compute_all_trees(self):
        permutations = list(it.permutations(self.players))
        for order in permutations:
            yield self.compute_tree(self.solutions, order, self.bids)

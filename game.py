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

    def compute_tree(self, solutions, players):
        P = solutions
        I = set()
        A = players
        node = Node(A(0), self.directions(A(0)), solutions=P,
                    bid=self.bids(-1) if self.directions(A(0)) else self.bids(0))
        root = node
        for player in A[1:]:
            # tutti i nodi "no"
            no_child = Node(player, self.directions(player), solutions=P,
                            bid=self.bids(-1) if self.directions(player) else self.bids(0))
            node.no = no_child
            no_child.parent = node
            node = no_child
        A = A[:-1]
        P = [solution for solution in P if node.player in P]
        #l'idea qui è usare la ricorsione
        return root

    #   permutations = list(it.permutations(self.players))
    #   for order in permutations:

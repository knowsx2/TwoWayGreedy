class Node:
    def __init__(self, solutions, player=None, direction=None, bid=None, domains=None):
        self.player = player
        self.direction = direction
        self.bid = bid
        self.solutions = solutions
        self.domains = domains
        self.yes = None
        self.no = None
        self.parent = None


    def get_player(self):
        return self.player

    def get_direction(self):
        return self.direction

    def get_bid(self):
        return self.bid

    def get_yes(self):
        return self.yes

    def get_no(self):
        return self.no

    def set_player(self, player):
        self.player = player

    def set_direction(self, direction):
        self.direction = direction

    def set_bid(self, bid):
        self.bid = bid

    def set_yes(self, node):
        self.yes = node

    def set_no(self, node):
        self.no = node

    def change(self, node):
        self.player = node.player
        self.direction = node.direction
        self.bid = node.bid
        self.solutions = node.solutions
        self.yes = node.yes
        self.no = node.no
        self.parent = node.parent

    def __str__(self):
        strdir = "in" if self.direction == 1 else "out"
        string = "ply: " + str(self.player) + " | " + "dir: " + strdir + " | " + "bid: " + str(self.bid) \
                 + " | " + "sol:: " + str(self.solutions)
        return string

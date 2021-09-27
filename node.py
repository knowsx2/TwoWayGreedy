class Node:
    def __init__(self, solutions, player=None, direction=None, bid=None ):
        self.player = player
        self.direction = direction
        self.bid = bid
        self.solutions = solutions
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

    def __str__(self):
        string = "ply: " + str(self.player) +" | " + "dir: " + str(self.direction) + " | " + "bid: " + str(self.bid)\
                 + " | " + "sol:: " + str(self.solutions)
        return string


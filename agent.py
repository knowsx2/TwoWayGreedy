from my_exceptions import BidError


class Agent:

    """
    Class represents a player of a game.
    Each player has: a name, a domain of valuation and a private bid

    Parameters
    ----------
    name: string
        the name of agent

    val_domain: float tuple
        the agent's domain of valuations

    bid: float
        the private real bid of agent (it must be present in val_domain)

    Returns
    -------
    tipo
        descrizione del tipo di ritorno

    Raises
    ------
    Exception
        the bid isn't present in val_domain
    """
    def __init__(self, name, val_domain, bid):
        self.name = name
        self.domain = sorted(val_domain)
        self.set_bid(bid)

    def get_name(self):
        return self.name

    def get_domain(self):
        return self.domain

    def get_bid(self):
        return self.bid

    def set_name(self, name):
        self.name = name

    def set_domain(self, domain):
        self.domain = domain

    def set_bid(self, bid):
        if bid in self.domain:
            self.bid = bid
        else:
            raise BidError("the bid is not present in val_domain")

import random

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 10, 'Q': 10, 'K': 10}


# define card class
class Card(object):
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print("Invalid card: %s %s" % (suit, rank))

    def __str__(self):
        return self.suit + "-" + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank


# card = Card('C', str(4))
# print(card)

class Hand(object):
    aces = False

    def __init__(self):
        self.cards = []

    def __str__(self):
        ans = "Hand Contains: "
        for i in self.cards:
            ans += str(i) + " "
        return ans

    def add_card(self, card):
        self.cards.append(card)
        if card.get_rank() == 'A':
            aces = True

    # get_max_value by considering A = 11 when not bust
    def get_value(self):
        value = self.get_least_value()
        if self.aces and value < 12:
            value += 10
        return value

    # consider potential A as 1
    def get_least_value(self):
        value = 0
        for card in self.cards:
            rank = card.get_rank()
            v = VALUES[rank]
            value += v
        return value


class Deck(object):
    def __init__(self):
        self.deck = []
        # append 54 cards as one deck
        for s in SUITS:
            for r in RANKS:
                self.deck.append(Card(s, r))

    def shuffle(self):
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop()

    def __str__(self):
        ans = "The deck: "
        for card in self.deck:
            ans += str(card) + " "
        return ans

"""
keep the record of wins and total times for each
(value, dealer face) combination
"""


class RelativeRate(object):
    def __init__(self):
        self.total = 0
        self.wins = 0

    def __str__(self):
        return str(self.wins) + " / " + str(self.total)

    def win(self):
        self.total += 1
        self.wins += 1

    def lose(self):
        self.total += 1


# Monte Carlo Simulation
def sim(trials):
    print("sim function!");


def hitme(playerand, dealerfacecard):
    """ dealerfacecard in [2, 3, 4, 5, 6, 7, 8, 9, 10[ * 3], A(1 or 11)]
    # playerhand = hard []
    get strategy of strategy table(file)
    """
    hit = True
    return hit;


def play(trials):
    print("play " + str(trials) + " times!");


play(100000);

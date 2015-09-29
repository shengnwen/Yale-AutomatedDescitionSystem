__author__ = 'shengwen'
import random

# set all values to 0
# set hit win percentage
# calculate hit win percentage
# 1/50 hit
# 1/50 hand
# transcript keep modify
# > 40 hit
# > 45 hit
# >

def hitme (playerhand = 12, dealerfacecard = 1):
        return True

# return a float number
def play (trials = 5):
        return 0.89

# index start from 1 to 10, 1 - 21
def get_hit_table():
    hit_table = []
    with open("hit_table","r") as fin:
        lines = fin.read().splitlines()
    hit_table = []
    for line in lines:
        hit_table.append(line.split())
    return hit_table

def print_hit_table(hit_table):
    for row in hit_table:
        for col in row:
            print(str(col)),
        print


def store_hit_table(hit_table):
    with open('./hit_table', 'w') as f:
        for row in xrange(0, 22):
            for col in xrange(0, 11):
                f.write(str(hit_table[row][col]) + " ")
            f.write("\n")

def initiate_hit_table():
    # start from hit! \\ hit stand for true
    with open("hit_table", "w") as output:
        for x in xrange(0, 22):
            for y in xrange(0, 11):
                if x == 0:
                    output.write("- ")
                    continue
                if y == 0:
                    output.write("| ")
                    continue
                output.write("1 ")
            output.write("\n")


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
        return "(" + self.suit + " " + self.rank + ")"

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

class Hand:
    def __init__(self):
        self.cards = []

    def __str__(self):
        ans = "Hand contains "
        for i in range(len(self.cards)):
            ans += str(self.cards[i]) + " "
        return ans
        # return a string representation of a hand

    def add_card(self, card):
        self.cards.append(card)
        # add a card object to a hand

    def get_value(self):
        value = 0
        aces = False
        for c in self.cards:
            rank = c.get_rank()
            v = VALUES[rank]
            if rank == 'A': aces = True
            value += v
        if aces and value < 12: value += 10
        return value
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video

# define deck class
class Deck:
    def __init__(self):
        self.deck = []
        for s in SUITS:
            for r in RANKS:
                self.deck.append(Card(s, r))
        # create a Deck object

    def shuffle(self):
        random.shuffle(self.deck)
        # shuffle the deck

    def deal_card(self):
        return self.deck.pop()
        # deal a card object from the deck

    def __str__(self):
        ans = "The deck: "
        for c in self.deck:
            ans += str(c) + " "
        return ans
        # return a string representing the deck

# generate the transcript file

# return a float number
def play (trials = 5):
        return 0.89

def sim (trials = 5):
    initiate_hit_table()
    hit_table = get_hit_table()
    print_hit_table(hit_table)
    trialTotal = 0
    while trialTotal < trials:
        theDeck = Deck()
        theDeck.shuffle()
        playerHand = Hand()
        houseHand = Hand()
        playerHand.add_card(theDeck.deal_card())
        playerHand.add_card(theDeck.deal_card())
        houseHand.add_card(theDeck.deal_card())

        houseFaceCard = theDeck.deal_card()
        houseHand.add_card(houseFaceCard)
        trialTotal += 1

    with open("transcript", "w") as output:
        for x in xrange (0, 22):
            for y in xrange (0, 11):
                output.write ("0.01 ")
                output.write ("\n")
    hit_table[1][2] = str(0)
    print_hit_table()
    store_hit_table()


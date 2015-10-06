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
hit_table = []
final_win_transcript_table = []
final_transcript_table = []
thresh_hold = 0.40
def hitme (playerhand = 12, dealerfacecard = 1):
    global hit_table
    if len(hit_table) == 0:
        get_hit_table()
    return hit_table[playerhand][dealerfacecard] == '1'

# return a float number
def play(trials = 5):
    global hit_table
    global final_transcript_table
    get_hit_table()
    trialTotal = 0
    winNum = 0
    while trialTotal < trials:
        theDeck = Deck()
        theDeck.shuffle()
        playerHand = Hand()
        houseHand = Hand()
        playerHand.add_card(theDeck.deal_card())
        playerHand.add_card(theDeck.deal_card())
        houseHand.add_card(theDeck.deal_card())

        houseFaceCard = theDeck.deal_card()
        houseFaceValue = VALUES[houseFaceCard.get_rank()]
        houseHand.add_card(houseFaceCard)
        trialTotal += 1
#        print("round:" + str(trialTotal))
        # print("Player:" + str(playerHand)),
        # print("House face:" + str(houseFaceValue))
        finished = False
        win = False
        val = playerHand.get_value()
        isHit = hitme(val, houseFaceValue)
        while isHit:
            playerHand.add_card(theDeck.deal_card())
            val = playerHand.get_value()
            if val > 21:
                finished = True
                win = False
                break
            isHit = hitme(val, houseFaceValue)
        if not finished:
            houseVal = houseHand.get_value()
            while houseVal < 17:
                houseHand.add_card(theDeck.deal_card())
                houseVal = houseHand.get_value()
            val = playerHand.get_value()
            if houseVal > 21:
                if val > 21:
                    win = False
                else:
                    win = True
                finished = True
            else:
                if val == houseVal:
                    win = False
                elif val > houseVal:
                    win = True
                else:
                    win = False
                finished = True
        if finished:
            if win:
#                print("win!")
                winNum += 1
#                print("lose!")
#    print_table(hit_table)
#    print("success rate:" + str(float(winNum) / float(trials)))
    return float(winNum)/trials



# index start from 1 to 10, 1 - 21
def get_hit_table():
    global hit_table
    hit_table = []
    with open("hit_table","r") as fin:
        lines = fin.read().splitlines()
    hit_table = []
    for line in lines:
        hit_table.append(line.split())

def print_table(table, transcript = False):
    if transcript:
        print("Transcript:")
    else:
        print("Hit Me Table")
    for x in table:
        for y in x:
            print(str(y) + " "),
        print




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
                if x <= 11:
                    output.write("1 ")
                else:
                    output.write("0 ")
            output.write("\n")

def initiate_transcript():
    global final_transcript_table,  final_win_transcript_table
    final_transcript_table = []
    final_win_transcript_table = []
    for x in xrange(0, 22):
        line = []
        for y in xrange(0, 11):
            if x == 0 or y == 0:
                line.append("-")
            else:
                line.append(0)
        final_transcript_table.append(line)
    for x in xrange(0, 22):
        line = []
        for y in xrange(0, 11):
            if x == 0 or y == 0:
                line.append("-")
            else:
                line.append(0)
        final_win_transcript_table.append(line)



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



def renew_hit_table(trials):
    global thresh_hold
    global tmp_transcript_table, final_transcript_table, final_win_transcript_table
    global hit_table
    count = 0
    for x in range(1, 22):
        for y in range(1, 11):
            if final_transcript_table[x][y] != 0:
                count += 1
                if float(final_win_transcript_table[x][y]) / final_transcript_table[x][y] < thresh_hold:
                    if hit_table[x][y] == '0':
                        hit_table[x][y] = '1'
                    else:
                        hit_table[x][y] = '0'
    if count == 0:
        thresh_hold += 0.01


def store_hit_table():
    global hit_table
    with open('hit_table', 'w') as f:
        for row in hit_table:
            ans = ''
            for col in row:
                ans += str(col)
                ans += " "
            ans += "\n"
            f.write(ans)

def sim (trials = 5):
    global hit_table
    global tmp_transcript_table
    global final_transcript_table
    global final_win_transcript_table
    trial_summary = []
    initiate_hit_table()
    initiate_transcript()
    get_hit_table()
    trialTotal = 0
    winNum = 0
    while trialTotal < trials:
        theDeck = Deck()
        theDeck.shuffle()
        playerHand = Hand()
        houseHand = Hand()
        playerHand.add_card(theDeck.deal_card())
        playerHand.add_card(theDeck.deal_card())
        houseHand.add_card(theDeck.deal_card())

        houseFaceCard = theDeck.deal_card()
        houseFaceValue = VALUES[houseFaceCard.get_rank()]
        houseHand.add_card(houseFaceCard)
        trialTotal += 1
        if trialTotal >= 400 and trialTotal % 30 == 0:
            renew_hit_table(trials)
        # print("Player:" + str(playerHand)),
        # print("House face:" + str(houseFaceValue))
        finished = False
        win = False
        hit_val = []
        val = playerHand.get_value()
        isHit = hitme(val, houseFaceValue)
        while isHit:
            hit_val.append(val)
            playerHand.add_card(theDeck.deal_card())
            val = playerHand.get_value()
            if val > 21:
                finished = True
                win = False
                break
            isHit = hitme(val, houseFaceValue)
        if not finished:
            houseVal = houseHand.get_value()
            while houseVal < 17:
                houseHand.add_card(theDeck.deal_card())
                houseVal = houseHand.get_value()
            val = playerHand.get_value()
            if houseVal > 21:
                if val > 21:
                    win = False
                else:
                    win = True
                finished = True
            else:
                if val == houseVal:
                    win = False
                elif val > houseVal:
                    win = True
                else:
                    win = False
                finished = True
        if finished:
            outcome = ""
            if win:
                winNum += 1
                outcome = "Win"
                for val in hit_val:
                    final_win_transcript_table[val][houseFaceValue] += 1
                    final_transcript_table[val][houseFaceValue] += 1
            else:
                outcome = "Lose"
                for val in hit_val:
                    final_transcript_table[val][houseFaceValue] += 1
            result = "Round" + str(trialTotal) + ":" + outcome + "\n--player:" + str(playerHand) + "\n" + "--dealer:" + str(houseHand)
            trial_summary.append(result)
#    print_table(hit_table)
    print("success rate:" + str(float(winNum) / float(trials)))
    store_hit_table()
    with open("transcript", "w") as output:
        for x in xrange (1, 22):
            for y in xrange (1, 11):
                if final_transcript_table[x][y] != 0:
                    output.write(str(float(final_win_transcript_table[x][y]) / final_transcript_table[x][y]) + " ")
                else:
                    output.write("0 ")
            output.write ("\n")
    with open("summary", "w") as output:
        for line in trial_summary:
            output.write(line + "\n")

#sim(100000)
#print(play(10000))
print hitme(1, 5)

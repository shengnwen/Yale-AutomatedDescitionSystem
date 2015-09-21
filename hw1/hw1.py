import random

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 10, 'Q': 10, 'K': 10}

OUTCOME = {
    'PB': 'Lose: Player Busted',
    'HB': 'Win: House Busted',
    'Tie': 'Lose: This is a tie',
    'PS': 'Lose: Player\'s value is smaller than House\'s',
    'HS': 'Win: House\'s value is smaller than Player\'s'
}

# define global variables
the_deck = None
player_hand = None
house_hand = None
finished = False
outcome = None
win = None
winNumber = 0
total = 0
hit_table = [['-A', 'VL', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'A']]


# 3 main Card Type
# 1. A * 1 = (1, 11)
# 2. (2 - 9) * 8 = [2 - 9]
# 3. (10 J Q K) * 4 = 10
# basic strategy
# 1 represents A, 10 represents (10, J, Q, K)
# hard(5 - 20) : 16 rows
# soft(A, 2 - 9) : 8 rows
# True = 1, False =  0
def initiate_hit_table():
    global hit_table
    for row in range(0, 25):
        single_row_strategy = []
        if row + 5 < 10:
            single_row_strategy.append('0A')
            single_row_strategy.append("0" + str(row + 5))
        elif row + 5 < 21:
            single_row_strategy.append('0A')
            single_row_strategy.append(str(row + 5))
        elif row < 24:
            single_row_strategy.append('1A')
            single_row_strategy.append("0" + str(row - 14))
        else:
            single_row_strategy.append('2A')
            single_row_strategy.append("##")
        if row + 5 in range(5, 9):
            for col in range(1, 11):
                single_row_strategy.append('H')
        elif row + 5 == 9:
            for col in range(1, 11):
                single_row_strategy.append('H')
        elif row + 5 in range(10, 12):
            for col in range(1, 11):
                single_row_strategy.append('H')
        elif row + 5 == 12:
            for col in range(1, 11):
                if col <= 2 or col >= 6:
                    single_row_strategy.append('H')
                else:
                    single_row_strategy.append('S')
        elif row + 5 in range(13, 17):
            for col in range(1, 11):
                if col < 6:
                    single_row_strategy.append('S')
                else:
                    single_row_strategy.append('H')
        elif row + 5 in range(17, 21):
            for col in range(1, 11):
                single_row_strategy.append('S')
        elif row - 14 in range(2, 7):
            for col in range(1, 11):
                single_row_strategy.append('H')
        elif row - 14 == 7:
            for col in range(1, 11):
                if col < 8:
                    single_row_strategy.append('H')
                else:
                    single_row_strategy.append('S')
        elif row - 14 in range(8, 10):
            for col in range(1, 11):
                single_row_strategy.append('S')
        else:
            for col in range(1, 11):
                single_row_strategy.append('S')
        hit_table.append(single_row_strategy)


def print_hit_table():
    global hit_table
    for row in hit_table:
        for col in row:
            print str(col),
        print


def load_hit_table():
    global hit_table
    with open('./hit-me.txt', 'r') as f:
        lines = f.read().splitlines()
    hit_table = []
    for line in lines:
        hit_table.append(line.split(" "))


def store_hit_table():
    global hit_table
    with open('./hit-me.txt', 'w') as f:
        for row in hit_table:
            ans = ''
            for col in row:
                ans += str(col)
                ans += " "
            ans += "\n"
            f.write(ans)


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


# card = Card('C', str(4))
# print(card)
class Hand(object):
    aces = False
    double_aces = False

    def __init__(self):
        self.cards = []

    def __str__(self):
        ans = "Hand Contains: "
        for i in self.cards:
            ans += str(i) + " "
        return ans

    def add_card(self, card):
        self.cards.append(card)
        if card.get_rank() == 'A' and self.aces == False:
            self.aces = True
        elif card.get_rank() == 'A' and self.aces == True:
            self.double_aces = True

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


# HouseHand inherits Hand to
# get the behaviour of show second hand
class HouseHand(Hand):
    def initial_show(self):
        return "Hand Contains: (# #) " + str(self.cards[1])

    def get_face_card(self):
        return self.cards[1]


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


# keep the record of wins and total times for each
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


def hit_process():
    global finished, player_hand, outcome, win
    if not finished:
        new_card = the_deck.deal_card()
        print("Player add: " + str(new_card))
        player_hand.add_card(new_card)
        val = player_hand.get_value()
        if val > 21:
            outcome = OUTCOME['PB']
            finished = True
            win = False


def stand_process():
    global finished, player_hand, house_hand, outcome, win
    if player_hand.get_value() > 21:
        outcome = OUTCOME['PB']
        finished = True
        win = False
        return None
    if finished:
        return None
    val = house_hand.get_value()
    while val < 17:
        new_card = the_deck.deal_card()
        print("House add: " + str(new_card))
        house_hand.add_card(str(new_card))
        val = house_hand.get_value()
    if val > 21:
        if player_hand.get_value() > 21:
            outcome = OUTCOME['Tie']
            win = False
        else:
            outcome = OUTCOME['HB']
            win = True
    else:
        if val == player_hand.get_value():
            outcome = OUTCOME['Tie']
            win = False
        elif val > player_hand.get_value():
            outcome = OUTCOME['PS']
            win = False
        else:
            outcome = OUTCOME['HS']
            win = True


#  Monte Carlo Simulation
# calculate the 'hit me' table
# simulate game for only 1 trial
def single_sim():
    global the_deck, player_hand, house_hand, finished, outcome, win

    the_deck = Deck()
    the_deck.shuffle()
    player_hand = Hand()
    house_hand = HouseHand()

    # initial state
    # 2 cards can be seen from player
    # 1 card can be seen from house
    player_hand.add_card(the_deck.deal_card())
    player_hand.add_card(the_deck.deal_card())
    print("Initial state:")
    print("Player: " + str(player_hand))
    house_hand.add_card(the_deck.deal_card())
    house_hand.add_card(the_deck.deal_card())
    print("House: " + house_hand.initial_show())

    # simulate game process
    # is_hit = True
    global finished
    if not finished:
        # hit me return true - > hit
        # hit me return false -> stand
        is_hit = player_hand.cards, house_hand.get_face_card()
        while not finished and  is_hit:
            hit_process()
            is_hit = player_hand.cards, house_hand.get_face_card()
        stand_process()
    print("Player: " + str(player_hand))
    print("House: " + str(house_hand))
    print outcome
    return win


def simulation(trials, is_sim):
    global winNumber, total
    if is_sim:
        initiate_hit_table()
        store_hit_table()
        print_hit_table()
        print("# Simulate games %d times" % trials);
        for i in range(1, trials + 1):
            print("\n#SIM-" + str(i))
            result = single_sim()
            print("#win:" + str(result))
        print("## Hit me table installed!\n\n")
    else:
        # play_glame
        load_hit_table()
        print_hit_table()
        total = trials
        for i in range(1, trials + 1):
            print("\n#Game Round-" + str(i))
            result = single_sim()
            print("#win:" + str(result))
            if result:
                winNumber += 1
        print("Win Ratio: " + str(winNumber) + " / " + str(total))


def hitme():
    """returns a boolean value, true or false,
    specifying whether the player should ask for
    another card or not
    """
    global hit_table, player_hand, house_hand
    face_card = house_hand.get_face_card.get_rank() # 1 - 10
    aces = player_hand.aces

    # return hit


# After sim function, use hitme table to play trial times game
# return winning percentage
def sim(trials):
    simulation(trials, True)

def play(trials):
    win_ratio = 0.5
    simulation(trials, False)
    print("The winning rate: " + str(win_ratio))


# initiate_hit_table()
# print_hit_table()
#store_hit_table()

sim(1000)
play(3)

# play(1000)
# single_sim()
# sim(3, True)
# play(3)
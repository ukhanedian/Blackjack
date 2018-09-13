# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
outcome2 = ""
outcome_var = 0
score = 0
player_hand_value = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.cards = []	
        # create Hand object

    def __str__(self):
        cards_in_hand = "Hand contains "	
        for i in range(len(self.cards)):
            cards_in_hand += " " + str(self.cards[i])
        return cards_in_hand
        
        # return a string representation of a hand

    def add_card(self, card):
        self.cards.append(card)	
        # add a card object to a hand

    def get_value(self):
        sum = 0
        aces = False
        for xcard in self.cards:
            if xcard.get_rank() == 'A':
                aces = True
            sum += VALUES.get(xcard.get_rank())
        # checks if hand has aces
        if aces:
            if sum + 10 <= 21:
                sum += 10
        return sum
        # if hand has aces, adds the most useful amount
        
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
   
    def draw(self, canvas, pos):
        for i in self.cards:
            card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(i.get_rank()), CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(i.get_suit()))
            canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + (CARD_SIZE[0] * self.cards.index(i)), pos[1] + CARD_CENTER[1]], CARD_SIZE)
        # draw a hand on the canvas, use the draw method for cards
 
        
# define deck class 
class Deck:
    def __init__(self):
        self.all_cards = []
        for suit in SUITS:
            for rank in RANKS:
                card = Card(suit, rank)
                self.all_cards.append(card)
        # create a Deck object

    def shuffle(self):
        random.shuffle(self.all_cards)
        # shuffle the deck 
        # use random.shuffle()

    def deal_card(self):
        return self.all_cards.pop(0)
        # deal a card object from the deck
    
    def __str__(self):
        deck = "Deck contains "
        for i in range(len(self.all_cards)):
            deck += " " + str(self.all_cards[i])
        return deck
        # return a string representing the deck



#define event handlers for buttons
def deal():
    global outcome, outcome2, outcome_var, in_play, game_deck, player_hand, dealer_hand, score
    outcome_var = 0
    outcome = "Hit or Stand?"
    outcome2 = ""
    if in_play:
        score -= 1
        outcome_var = 3
        outcome = "Trying to cheat? Score -1!"
        outcome2 = "Press deal to try again!"
        in_play = False

    # prevents player from cheating and redealing in the middle of a round
    else:
        game_deck = Deck()
        game_deck.shuffle()
        player_hand = Hand()
        dealer_hand = Hand()
        player_hand.add_card(game_deck.deal_card())
        dealer_hand.add_card(game_deck.deal_card())
        player_hand.add_card(game_deck.deal_card())
        dealer_hand.add_card(game_deck.deal_card())
        in_play = True

def hit():
    # replace with your code below
    global outcome, in_play, game_deck, player_hand, dealer_hand, score, win
    outcome_var = 0
    outcome = "Hit or Stand?"
    outcome2 = ""
    if in_play == True:
        if player_hand.get_value() <= 21:
            player_hand.add_card(game_deck.deal_card())
        if player_hand.get_value() > 21:
            score -= 1
            in_play = False
            win = False
            outcome_var = 2
            outcome = "Dealer wins! Try again?"
            outcome2 = ""
    # if the hand is in play, hit the player   
    # if busted, assign a message to outcome, update in_play and score
       
def stand():
    global outcome, outcome_var, in_play, game_deck, player_hand, dealer_hand, score, win
    if in_play == True:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(game_deck.deal_card())
        if dealer_hand.get_value() > 21:
            score += 1
            in_play = False
            win = True
            outcome_var = 1
            outcome = "Player wins! Play again?"
            outcome2 = ""
        elif dealer_hand.get_value() >= player_hand.get_value():
            score -= 1
            in_play = False
            win = False
            outcome_var = 2
            outcome = "Dealer wins! Try again?"
            outcome2 = ""
        elif player_hand.get_value() > dealer_hand.get_value():
            score += 1
            in_play = False
            win = True
            outcome_var = 1
            outcome = "Player wins! Play again?"
            outcome2 = ""
    # replace with your code below
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    # assign a message to outcome, update in_play and score

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    canvas.draw_text("Blackjack!", (100, 75), 75, "Black")
    standard_x = 175
    # assigns commonly used x coordinate to variable
    player_hand.draw(canvas, [standard_x + CARD_CENTER[0], 450])
    canvas.draw_text("Player", (standard_x, 425), 35, "Black")
    canvas.draw_text("Dealer", (standard_x, 150), 35, "Black")
    canvas.draw_text("Score: " + str(score), (standard_x + 200, 425), 30, "Black")
    canvas.draw_text("Value: " + str(player_hand.get_value()), (15, 500), 30, "Black")
    if outcome_var == 0:
        canvas.draw_text(outcome, (standard_x, 350), 30, "Black")
    elif outcome_var == 1:
        canvas.draw_text(outcome, (standard_x, 350), 30, "White")
    elif outcome_var == 2:
        canvas.draw_text(outcome, (standard_x, 350), 30, "Maroon")
    elif outcome_var == 3:
        canvas.draw_text(outcome, (20, 325), 49, "Red")
        canvas.draw_text(outcome2, (20, 375), 49, "Red")
    # changes how 'outcome' is drawn depending on result
    if in_play:
        canvas.draw_text("Value: ?", (15, 200), 30, "Black")
        dealer_hand.cards[1].draw(canvas, [standard_x + CARD_SIZE[0], 175])
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [standard_x + CARD_BACK_CENTER[0], 175 + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)
    elif in_play == False:
        dealer_hand.draw(canvas, [standard_x + CARD_CENTER[0], 175])
        canvas.draw_text("Value: " + str(dealer_hand.get_value()), (15, 200), 30, "Black")
    # hides dealer's hole card until the game is over    
    # canvas.draw_text('A', (20, 20), 12, 'Red')
    


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric
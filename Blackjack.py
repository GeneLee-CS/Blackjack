
# coding: utf-8

# In[ ]:


import random

# Spades --> \u2660
# Heart --> \u2665
# Diamond --> \u2666
# Club --> \u2663
suits = ("\u2660", "\u2665", "\u2666", "\u2663")
ranks = ('2', '3', '4', '5', '6', '7', '8', '9', 'J', 'K', 'Q', 'A' )
values = {'2': 2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'J':10,
        'Q':10, 'K':10, 'A':11}

playing = True


# In[ ]:


class Font:
    
# Bold letters to display card ranks
    BOLD = '\033[1m'
    RED = '\033[91m'
    END = '\033[0m'


# In[ ]:


class Card:
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
    
    def __str__(self):
        return self.rank + ' ' + self.suit
            


# In[ ]:


test_card = Card("\u2665",'5')
print (test_card)
print (Font.RED + Font.BOLD + str(test_card) + Font.END)


# In[ ]:


class Deck:
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))
    
    def __str__(self):
        full_deck = ''
        for card in self.deck:
            full_deck += '\n' + card.__str__()
    
    def shuffle(self):
        random.shuffle(self.deck)
    
    def deal(self):
        dealt_card = self.deck.pop()
        return dealt_card


# In[ ]:


class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0
        
    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'A':
            self.aces += 1
    
    def adjust_for_ace(self):
        if self.aces >= 1 and self.value > 21:
            self.value -= 10
            self.aces -= 1
        


# In[ ]:


class Chips:
    
    def __init__(self,total):
        self.total = total
        self.bet = 0
        
    def win_bet(self):
        self.total += self.bet
    
    def lose_bet(self):
        self.total -= self.bet


# In[ ]:


def take_bet(chips):
    
    while True:
        try:
            chips.bet = int(input('How much would you like to bet? '))
        except:
            print('Please enter a valid amount ')
        else:
            if chips.bet > chips.total:
                print('Sorry you do not have enough chips. You currently have ',chips.total)
            else:
                break


# In[ ]:


def hit(deck,hand):
    
    hit_card = deck.deal()
    hand.add_card(hit_card)
    hand.adjust_for_ace


# In[ ]:


def hit_or_stand(deck,hand):
    
    global playing
    
    while True:
        decision = input("\nWould you like to hit or stand ? Enter 'h' for hit or 's' for stand ")
        
        if decision.lower() == 'h':
            hit(deck,hand)
        elif decision.lower() == 's':
            print("Player stands. Dealer's turn")
            playing = False
        else:
            print("Please enter either 'h' or 's'")
            continue
        break


# In[ ]:


def show_some(player,dealer):
    
    print("\nYour hand: \n")
    for card in player.cards:
        print(card)
    print('\n')
    print("Dealer's hand: \n")
    print(dealer.cards[0])
    print("< Hidden Card >")

def show_all(player,dealer):
    
    print("\nYour hand: \n")
    for card in player.cards:
        print(card)
    print("\n")
    print("Dealer's hand: \n")
    for card in dealer.cards:
        print(card)


# In[ ]:


def player_busts(player,dealer,chips):
    
    print("Sorry, you busted")
    chips.lose_bet()

def player_wins(player,dealer,chips):
    print("Congratulations, you won!")
    chips.win_bet()

def dealer_busts(player,dealer,chips):
    print("Dealer busted. you won!")
    chips.win_bet()

def dealer_wins(player,dealer,chips):
    print("Dealer won, better luck next time.")
    chips.lose_bet()

def tie(player,dealer):
    print("Its a tie!")


# In[ ]:


print("Welcome to Blackjack")

player_chips = 0

while True:
    
    if player_chips == 0:
        try:
            buy_in_amount = int(input("How much would you like to buy in? "))
        
        except:
            print("Please enter a valid amount")
        
        player_chips = Chips(buy_in_amount)
        
    deck = Deck()
    deck.shuffle()
    
    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
    
    take_bet(player_chips)
    
    show_some(player_hand,dealer_hand)
    
    while playing:
        
        hit_or_stand(deck,player_hand)
        
        show_some(player_hand,dealer_hand)
        
        if player_hand.value > 21:
            player_busts(player_hand,dealer_hand,player_chips)
            break
    
    if player_hand.value <= 21:
        
        while dealer_hand.value < 17:
            hit(deck,dealer_hand)
            
        show_all(player_hand,dealer_hand)
        
        if dealer_hand.value > 21:
            dealer_busts(player_hand,dealer_hand,player_chips)
        
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand,dealer_hand,player_chips)
        
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand,dealer_hand,player_chips)
            
        else:
            tie(player_hand,dealer_hand)
    
    print('\n You now have {} chips'.format(player_chips.total))
    
    new_game = input("Would you like to play another round? y/n ")
    
    if player_chips.total == 0:
        replay = input("You're out of chips. WOuld you like to buy in again? y/n ")
        
        if replay.lower() == 'y':
            try:
                rebuy = int(input("How much would you like to buy in? "))
            except:
                print("Please enter a number")
            
        if replay.lower() == 'n':
            print("Thanks for playing")
            break
        
        player_chips = Chips(rebuy)
            
    if new_game.lower() == 'y':            
        playing = True
        continue
    else:
        print("Thanks for playing")
        break


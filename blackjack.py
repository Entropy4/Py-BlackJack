
"""
This is an Intermediate-Level Python program for an (almost) fully-fledged BlackJack game with heavy focus on OOP and Functions.


THE RULES OF THE GAME:
    
    A.   The rules are pretty much the same as regular BlackJack except for the absence of:
            1.    Split
            2.    Surrender    
            3.    Insurance
    B.   You can play this game on your own against a computerised dealer or along with upto 3 other local friends!
    C.   This particular BlackJack 'Table' follows S17 Rule i.e. if you have a hand with a total value of 17, you have the option to choose to stand.
    D.   You start out with 1000 Chips in your hand. Place bets wisely or risk losing all Chips and getting kicked out.


"""
from tabulate import tabulate
import random
from os import system, name
# import sleep to show output for some time period 
from time import sleep 
  
# define our clear function to clear screen (code shown below works for Mac, Linux and Windows too): 
def clear():
    '''
    PURPOSE:    Clears output screen
    '''
    if name == 'nt': 
        _ = system('cls')
    else:
        _ = system('clear')


suits=('Hearts','Diamonds','Spades','Clubs')
ranks=('Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Jack','Queen','King','Ace')
values={'Two':2,'Three':3,'Four':4,'Five':5,'Six':6,'Seven':7,'Eight':8,'Nine':9,'Ten':10,'Jack':10,'Queen':10,'King':10,'Ace':11}
players=[]
n=0


def no_of_players():
    '''
    PURPOSE:    Initializes a Blackjack session with 1-4 players (depending upon user input)
                Depending upon user input, initializes n+1 objects of Player class and appends them to the players list (extra 1 object for the automated Dealer) 
    '''
    global players
    while True:
        try:
            n=int(input('Enter the of players playing in this session (1-4): '))
        except:
            print("Whoops! Please enter integers only. Try again!")
            continue
        else:
            if n in range(1,5):
                dealer=Player("Dealer")
                players.append(dealer)
                for i in range(n):
                    p_name=input(f'Enter your name Player {i+1}: ')
                    players.append(Player(p_name))
                break
            else:
                print('Enter a number between 1 and 4 only. Please try again!')
                continue
                    


class Card():
    
    '''
    Class Attributes:   Suit
                        Rank
                        Value
    Class Methods:      parameterised constructor
                        dunder method to print card's suit and rank
    '''
    
    def __init__(self,suit,rank,value):
        self.suit=suit
        self.rank=rank
        self.value=value
    
    def __str__(self):
        return f'{self.rank} of {self.suit}'
    
    
    
class Deck():
    
    '''
    Class Attributes:   deck                        (a list containing objects of Card class)
    Class Methods:      parameterised constructor
                        shuffle                     (to shuffle the deck before each round)
                        deal                        (to pop a card from deck and return it)
                        reset_deck                  (to reset deck in preparation for next round)
                        dunder method to print entire deck for trouble-shooting                       
    '''
    
    def __init__(self):
        self.deck=[]
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank,values[rank]))
                
    def __str__(self):
        return self.deck
    
    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        return self.deck.pop()
    
    def reset_deck(self):
        del self.deck
        self.deck=[]
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank,values[rank]))
        


class Hand():
    
    '''
    Class Attributes:   cards                       (a list which will hold cards dealt to the hand's holder)
                        value                       (total value of the hand)
                        aces                        (total number of new unadjusted aces in hand)
                        adjd_aces                   (total number of adjusted aces -i.e. reduced value aces to try to keep hand value under 21- in hand)
    Class Methods:      parameterised constructor
                        add_card                    (adds newly dealt card to cards list)
                        adjust_for_aces             (should hand value exceed over 21 at any point in time, reduces unadjusted aces' value to 1 from 11)                       
    '''
    
    def __init__(self):
        
        self.cards=[]
        self.value=0
        self.aces=0
        self.adjd_aces=0
        
    def add_card(self,card):
        self.cards.append(card)
        self.value+=card.value
        if card.rank=='Ace':
            self.aces+=1
            
    def adjust_for_aces(self):
        if self.value>21:
            self.value-=10*self.aces
            self.aces-=1
            self.adjd_aces+=1


            
class Chips():
    
    '''
    Class Attributes:   total                       (amount of chips in hand inclusive of currently-betted amount)
                        bet                         (amount of chips bet in this round)
                        won                         (total amount of chips won from previous rounds)
                        lost                        (total amount of chips lost from previous rounds)
    Class Methods:      parameterised constructor
                        win_bet                     (to change attributes when player wins a round)
                        lose_bet                    (to change attributes when player loses a round)
                        dunder method to print chips balance of chip-holder                       
    '''
    
    def __init__(self):
        
        self.total = 1000
        self.bet = 0
        self.won = 0
        self.lost = 0
               
    def win_bet(self):
        self.total += self.bet
        self.won += self.bet
        self.bet = 0
        
    def lose_bet(self):
        global players
        self.total -= self.bet
        self.lost += self.bet
        players[0].chips.total+=self.bet
        players[0].chips.won += self.bet
        self.bet = 0
    
    def __str__(self):
        return f"Balance\nChips in hand (inclusive of betted amount):\t{self.total}\nBetted amount of Chips:\t\t\t\t{self.bet}"
        


class Player():
    
    '''
    Class Attributes:   name                        (name of player)
                        chips                       (an object of Chips class)
                        hand                        (an object of Hand class)
                        playing                     (boolean variable tracking if a player has finished the current round or not)
                        wins                        (total no. of wins from previous rounds)
                        losses                      (total no. of losses from previous rounds)
    Class Methods:      parameterised constructor
                        reset_hand                  (to reset hand after round is over)
                        dunder method to print name of player                       
    '''
    
    def __init__(self,name):
        self.name = name
        self.chips = Chips()
        self.hand = Hand()
        self.playing=True
        self.wins=0
        self.losses=0
        
    def __str__(self):
        return self.name
    
    def reset_hand(self):
        del self.hand
        self.hand=Hand()



#global variable for the playing-card deck
stacked_deck=Deck()



def take_bet(player):

    '''
    INPUT:      current_player object of the Player class     
    PURPOSE:    Takes the bet of the current player before the dealer hits all players twice
                This function should NOT be run for the dealer (despite the dealer also being an object of Player class)
    '''
    
    print("\n\nCurrent ",end='')
    print(player.chips)
    while True:
        try:
            bet_amt=int(input(f'Enter the amount of Chips you wish to bet {player.name}: '))
        except:
            print("Whoops! Please enter integers only. Try again!")
            continue
        else:
            if bet_amt<=0:
                print("Can't cheat the system here Einstein! Enter positive numbers only. Try again!")
                continue
            elif bet_amt<=player.chips.total:
                print(f"{player.name}, you chose to bet {bet_amt} Chips.")
                player.chips.bet=bet_amt
                print(player.chips)
                input('Press Enter To Continue')
                break
            else:
                print("Insufficient chips balance")
                continue
            


def hit(player):
    
    '''
    INPUT:      current_player object of the Player class     
    PURPOSE:    Hits the current player
                Should be run for all players including the dealer
                Has a different logic for Dealer's case where the dealer will always try to hit till the dealer's hand value is atleast 17
    '''
    
    global stacked_deck
    global n
    flagged=0
    if player.name=='Dealer' and len(player.hand.cards)>=2:
        for i in range(1,len(players)):
            if players[i].playing:
                flagged=1
        if flagged:
            while player.hand.value<17:
                drawn=stacked_deck.deal()
                player.hand.add_card(drawn)
                player.hand.adjust_for_aces()
            if player.hand.value > 21:
                dealer_busts()
        end_of_round(n)
    else:
        drawn=stacked_deck.deal()
        player.hand.add_card(drawn)
        player.hand.adjust_for_aces()
        
  
      
def hit_stand_or_double_down_(player):
    
    '''
    INPUT:      current_player object of the Player class     
    PURPOSE:    Takes the choice of the current player between Hit, Stand or Double Down before the dealer hits itself
                This function should NOT be run for the dealer (despite the dealer also being an object of Player class)
    '''    
    
    while True:
        choice=input(f'{player.name}, do you wish to Hit, Stand or Double Down? [H/S/D]: ')
        if choice=='H' or choice=='h':
            hit(player)
            show_some()
            if player.hand.value>=21:
                player_busts(player)
                show_some()
                break
        elif choice=='S' or choice=='s':
            player.playing=True
            break
        elif choice=='D' or choice=='d':
            while True:
                try:
                    bet_amt=int(input(f'Enter the amount you wish to bet further {player.name} \n(Note:\tYou can further bet a maximum amount of {player.chips.bet} Chips provided you have sufficient balance):  '))
                except:
                    print("Whoops! Please enter integers only. Try again!")
                    continue
                else:
                    if bet_amt + player.chips.bet <= player.chips.total and bet_amt <= player.chips.bet:
                        print(f"{player.name}, you chose to increase your bet by {bet_amt} Chips.")
                        player.chips.bet+=bet_amt
                        print(player.chips)
                        break
                    elif bet_amt + player.chips.bet <= player.chips.total and bet_amt > player.chips.bet:
                        print("Whoops! You can't increase your bet amount to more than double your current bet amount. Try again!")
                        continue
                    else:
                        print("Insufficient chips balance")
                        continue
            hit(player)
            if player.hand.value > 21:
                player_busts(player)
                show_some()
            else:
                player.playing=True
            break
        else:
            print("Whoops! Please enter 'H' for Hit, 'S' for Stand, or 'D' for Double Down only. Try again!")
            continue

   
     
def show_some():
    
    '''   
    PURPOSE:    Displays the BlackJack table, hiding the dealer's first card
                To be executed during the round, not after
                Uses tabulate library. Thus depending on the number of players, there are different print statements for each case
                Temporarily appends objects of NoneType to all players' hands to fill card vacancies. These objects are removed after the Table is displayed
                Hand size set to 11 as this the mathematically largest hand that could possibly exist in a 4-Deck Blacjjack game (4 Aces, 4 Twos, 3 Threes)
    '''
    
    global players
    for player in players:
        while len(player.hand.cards)<=11:
            player.hand.cards.append(None)
    
    if len(players)==2:
        print(tabulate([  [ '**********'             , players[1].hand.cards[0] ]  ,  
                          [ players[0].hand.cards[1] , players[1].hand.cards[1] ]  ,  
                          [ players[0].hand.cards[2] , players[1].hand.cards[2] ]  ,  
                          [ players[0].hand.cards[3] , players[1].hand.cards[3] ]  ,  
                          [ players[0].hand.cards[4] , players[1].hand.cards[4] ]  ,
                          [ players[0].hand.cards[5] , players[1].hand.cards[5] ]  ,
                          [ players[0].hand.cards[6] , players[1].hand.cards[6] ]  ,
                          [ players[0].hand.cards[7] , players[1].hand.cards[7] ]  ,
                          [ players[0].hand.cards[8] , players[1].hand.cards[8] ]  ,
                          [ players[0].hand.cards[9] , players[1].hand.cards[9] ]  ,
                          [ players[0].hand.cards[10] , players[1].hand.cards[10] ]  ] , players,  tablefmt="grid"))
    elif len(players)==3:
        print(tabulate([  [ '**********'             , players[1].hand.cards[0] , players[2].hand.cards[0] ]  ,  
                          [ players[0].hand.cards[1] , players[1].hand.cards[1] , players[2].hand.cards[1] ]  ,  
                          [ players[0].hand.cards[2] , players[1].hand.cards[2] , players[2].hand.cards[2] ]  ,  
                          [ players[0].hand.cards[3] , players[1].hand.cards[3] , players[2].hand.cards[3] ]  ,  
                          [ players[0].hand.cards[4] , players[1].hand.cards[4] , players[2].hand.cards[4] ]  ,
                          [ players[0].hand.cards[5] , players[1].hand.cards[5] , players[2].hand.cards[5] ]  ,
                          [ players[0].hand.cards[6] , players[1].hand.cards[6] , players[2].hand.cards[6] ]  ,
                          [ players[0].hand.cards[7] , players[1].hand.cards[7] , players[2].hand.cards[7] ]  ,
                          [ players[0].hand.cards[8] , players[1].hand.cards[8] , players[2].hand.cards[8] ]  ,
                          [ players[0].hand.cards[9] , players[1].hand.cards[9] , players[2].hand.cards[9] ]  ,
                          [ players[0].hand.cards[10] , players[1].hand.cards[10] , players[2].hand.cards[10] ]  ] , players,  tablefmt="grid"))
    elif len(players)==4:
        print(tabulate([  [ '**********'             , players[1].hand.cards[0] , players[2].hand.cards[0] , players[3].hand.cards[0] ]  ,  
                          [ players[0].hand.cards[1] , players[1].hand.cards[1] , players[2].hand.cards[1] , players[3].hand.cards[1] ]  ,  
                          [ players[0].hand.cards[2] , players[1].hand.cards[2] , players[2].hand.cards[2] , players[3].hand.cards[2] ]  ,  
                          [ players[0].hand.cards[3] , players[1].hand.cards[3] , players[2].hand.cards[3] , players[3].hand.cards[3] ]  ,  
                          [ players[0].hand.cards[4] , players[1].hand.cards[4] , players[2].hand.cards[4] , players[3].hand.cards[4] ]  ,  
                          [ players[0].hand.cards[5] , players[1].hand.cards[5] , players[2].hand.cards[5] , players[3].hand.cards[5] ]  ,
                          [ players[0].hand.cards[6] , players[1].hand.cards[6] , players[2].hand.cards[6] , players[3].hand.cards[6] ]  ,
                          [ players[0].hand.cards[7] , players[1].hand.cards[7] , players[2].hand.cards[7] , players[3].hand.cards[7] ]  ,
                          [ players[0].hand.cards[8] , players[1].hand.cards[8] , players[2].hand.cards[8] , players[3].hand.cards[8] ]  ,
                          [ players[0].hand.cards[9] , players[1].hand.cards[9] , players[2].hand.cards[9] , players[3].hand.cards[9] ]  ,
                          [ players[0].hand.cards[10] , players[1].hand.cards[10] , players[2].hand.cards[10] , players[3].hand.cards[10] ]  ] , players ,  tablefmt="grid"))
    elif len(players)==5:
        print(tabulate([  [ '**********'             , players[1].hand.cards[0] , players[2].hand.cards[0] , players[3].hand.cards[0] , players[4].hand.cards[0] ]  ,  
                          [ players[0].hand.cards[1] , players[1].hand.cards[1] , players[2].hand.cards[1] , players[3].hand.cards[1] , players[4].hand.cards[1] ]  ,  
                          [ players[0].hand.cards[2] , players[1].hand.cards[2] , players[2].hand.cards[2] , players[3].hand.cards[2] , players[4].hand.cards[2] ]  ,  
                          [ players[0].hand.cards[3] , players[1].hand.cards[3] , players[2].hand.cards[3] , players[3].hand.cards[3] , players[4].hand.cards[3] ]  ,  
                          [ players[0].hand.cards[4] , players[1].hand.cards[4] , players[2].hand.cards[4] , players[3].hand.cards[4] , players[4].hand.cards[4] ]  ,
                          [ players[0].hand.cards[5] , players[1].hand.cards[5] , players[2].hand.cards[5] , players[3].hand.cards[5] , players[4].hand.cards[5] ]  ,
                          [ players[0].hand.cards[6] , players[1].hand.cards[6] , players[2].hand.cards[6] , players[3].hand.cards[6] , players[4].hand.cards[6] ]  ,
                          [ players[0].hand.cards[7] , players[1].hand.cards[7] , players[2].hand.cards[7] , players[3].hand.cards[7] , players[4].hand.cards[7] ]  ,
                          [ players[0].hand.cards[8] , players[1].hand.cards[8] , players[2].hand.cards[8] , players[3].hand.cards[8] , players[4].hand.cards[8] ]  ,
                          [ players[0].hand.cards[9] , players[1].hand.cards[9] , players[2].hand.cards[9] , players[3].hand.cards[9] , players[4].hand.cards[9] ]  ,
                          [ players[0].hand.cards[10] , players[1].hand.cards[10] , players[2].hand.cards[10] , players[3].hand.cards[10] , players[4].hand.cards[10] ]  ] , players ,  tablefmt="grid"))

    for player in players:
        for i in range(player.hand.cards.count(None)):
            player.hand.cards.remove(None)        
            


def show_all():
    
    '''   
    PURPOSE:    Displays the entire BlackJack table, including the dealer's first card
                To be executed after the round, not during
                Uses tabulate library. Thus depending on the number of players, there are different print statements for each case
                Temporarily appends objects of NoneType to all players' hands to fill card vacancies. These objects are removed after the Table is displayed
                Hand size set to 11 as this the mathematically largest hand that could possibly exist in a 4-Deck Blacjjack game (4 Aces, 4 Twos, 3 Threes)
    '''
    
    global players
    for player in players:
        while len(player.hand.cards)<=11:
            player.hand.cards.append(None)
    
    if len(players)==2:
        print(tabulate([  [ players[0].hand.cards[0] , players[1].hand.cards[0] ]  ,  
                          [ players[0].hand.cards[1] , players[1].hand.cards[1] ]  ,  
                          [ players[0].hand.cards[2] , players[1].hand.cards[2] ]  ,  
                          [ players[0].hand.cards[3] , players[1].hand.cards[3] ]  ,  
                          [ players[0].hand.cards[4] , players[1].hand.cards[4] ]  ,
                          [ players[0].hand.cards[5] , players[1].hand.cards[5] ]  ,
                          [ players[0].hand.cards[6] , players[1].hand.cards[6] ]  ,
                          [ players[0].hand.cards[7] , players[1].hand.cards[7] ]  ,
                          [ players[0].hand.cards[8] , players[1].hand.cards[8] ]  ,
                          [ players[0].hand.cards[9] , players[1].hand.cards[9] ]  ,
                          [ players[0].hand.cards[10] , players[1].hand.cards[10] ]  ,
                          [ players[0].hand.value    , players[1].hand.value    ]  ] , players,  tablefmt="grid"))
    elif len(players)==3:
        print(tabulate([  [ players[0].hand.cards[0] , players[1].hand.cards[0] , players[2].hand.cards[0] ]  ,  
                          [ players[0].hand.cards[1] , players[1].hand.cards[1] , players[2].hand.cards[1] ]  ,  
                          [ players[0].hand.cards[2] , players[1].hand.cards[2] , players[2].hand.cards[2] ]  ,  
                          [ players[0].hand.cards[3] , players[1].hand.cards[3] , players[2].hand.cards[3] ]  ,  
                          [ players[0].hand.cards[4] , players[1].hand.cards[4] , players[2].hand.cards[4] ]  ,
                          [ players[0].hand.cards[5] , players[1].hand.cards[5] , players[2].hand.cards[5] ]  ,
                          [ players[0].hand.cards[6] , players[1].hand.cards[6] , players[2].hand.cards[6] ]  ,
                          [ players[0].hand.cards[7] , players[1].hand.cards[7] , players[2].hand.cards[7] ]  ,
                          [ players[0].hand.cards[8] , players[1].hand.cards[8] , players[2].hand.cards[8] ]  ,
                          [ players[0].hand.cards[9] , players[1].hand.cards[9] , players[2].hand.cards[9] ]  ,
                          [ players[0].hand.cards[10] , players[1].hand.cards[10] , players[2].hand.cards[10] ]  ,
                          [ players[0].hand.value    , players[1].hand.value    , players[2].hand.value    ]  ] , players,  tablefmt="grid"))
    elif len(players)==4:
        print(tabulate([  [ players[0].hand.cards[0] , players[1].hand.cards[0] , players[2].hand.cards[0] , players[3].hand.cards[0] ]  ,  
                          [ players[0].hand.cards[1] , players[1].hand.cards[1] , players[2].hand.cards[1] , players[3].hand.cards[1] ]  ,  
                          [ players[0].hand.cards[2] , players[1].hand.cards[2] , players[2].hand.cards[2] , players[3].hand.cards[2] ]  ,  
                          [ players[0].hand.cards[3] , players[1].hand.cards[3] , players[2].hand.cards[3] , players[3].hand.cards[3] ]  ,  
                          [ players[0].hand.cards[4] , players[1].hand.cards[4] , players[2].hand.cards[4] , players[3].hand.cards[4] ]  ,  
                          [ players[0].hand.cards[5] , players[1].hand.cards[5] , players[2].hand.cards[5] , players[3].hand.cards[5] ]  ,
                          [ players[0].hand.cards[6] , players[1].hand.cards[6] , players[2].hand.cards[6] , players[3].hand.cards[6] ]  ,
                          [ players[0].hand.cards[7] , players[1].hand.cards[7] , players[2].hand.cards[7] , players[3].hand.cards[7] ]  ,
                          [ players[0].hand.cards[8] , players[1].hand.cards[8] , players[2].hand.cards[8] , players[3].hand.cards[8] ]  ,
                          [ players[0].hand.cards[9] , players[1].hand.cards[9] , players[2].hand.cards[9] , players[3].hand.cards[9] ]  ,
                          [ players[0].hand.cards[10] , players[1].hand.cards[10] , players[2].hand.cards[10] , players[3].hand.cards[10] ]  ,
                          [ players[0].hand.value    , players[1].hand.value    , players[2].hand.value    , players[3].hand.value    ]  ] , players ,  tablefmt="grid"))
    elif len(players)==5:
        print(tabulate([  [ players[0].hand.cards[0] , players[1].hand.cards[0] , players[2].hand.cards[0] , players[3].hand.cards[0] , players[4].hand.cards[0] ]  ,  
                          [ players[0].hand.cards[1] , players[1].hand.cards[1] , players[2].hand.cards[1] , players[3].hand.cards[1] , players[4].hand.cards[1] ]  ,  
                          [ players[0].hand.cards[2] , players[1].hand.cards[2] , players[2].hand.cards[2] , players[3].hand.cards[2] , players[4].hand.cards[2] ]  ,  
                          [ players[0].hand.cards[3] , players[1].hand.cards[3] , players[2].hand.cards[3] , players[3].hand.cards[3] , players[4].hand.cards[3] ]  ,  
                          [ players[0].hand.cards[4] , players[1].hand.cards[4] , players[2].hand.cards[4] , players[3].hand.cards[4] , players[4].hand.cards[4] ]  ,  
                          [ players[0].hand.cards[5] , players[1].hand.cards[5] , players[2].hand.cards[5] , players[3].hand.cards[5] , players[4].hand.cards[5] ]  ,
                          [ players[0].hand.cards[6] , players[1].hand.cards[6] , players[2].hand.cards[6] , players[3].hand.cards[6] , players[4].hand.cards[6] ]  ,
                          [ players[0].hand.cards[7] , players[1].hand.cards[7] , players[2].hand.cards[7] , players[3].hand.cards[7] , players[4].hand.cards[7] ]  ,
                          [ players[0].hand.cards[8] , players[1].hand.cards[8] , players[2].hand.cards[8] , players[3].hand.cards[8] , players[4].hand.cards[8] ]  ,
                          [ players[0].hand.cards[9] , players[1].hand.cards[9] , players[2].hand.cards[9] , players[3].hand.cards[9] , players[4].hand.cards[9] ]  ,
                          [ players[0].hand.cards[10] , players[1].hand.cards[10] , players[2].hand.cards[10] , players[3].hand.cards[10] , players[4].hand.cards[10] ]  ,
                          [ players[0].hand.value    , players[1].hand.value    , players[2].hand.value    , players[3].hand.value    , players[4].hand.value    ]  ] , players ,  tablefmt="grid"))
    for player in players:
        for i in range(player.hand.cards.count(None)):
            player.hand.cards.remove(None)
            


def show_stats():
    
    '''   
    PURPOSE:    Displays the Player stats after each round ends, including rounds won/lost and chips won/lost
                Uses tabulate library. Thus depending on the number of players, there are different print statements for each case
    '''
    
    global players
    if len(players)==2:
        print(tabulate([  [ players[1].name , players[1].wins , players[1].losses , players[1].chips.won , players[1].chips.lost ]  ] , ["Player Name","Wins","losses","Chips Won","Chips lost"],  tablefmt="grid"))
    elif len(players)==3:
        print(tabulate([  [ players[1].name , players[1].wins , players[1].losses , players[1].chips.won , players[1].chips.lost ]  ,
                          [ players[2].name , players[2].wins , players[2].losses , players[2].chips.won , players[2].chips.lost ]  ] , ["Player Name","Wins","losses","Chips Won","Chips lost"],  tablefmt="grid"))
    elif len(players)==4:
        print(tabulate([  [ players[1].name , players[1].wins , players[1].losses , players[1].chips.won , players[1].chips.lost ]  ,
                          [ players[2].name , players[2].wins , players[2].losses , players[2].chips.won , players[2].chips.lost ]  ,
                          [ players[3].name , players[3].wins , players[3].losses , players[3].chips.won , players[3].chips.lost ]  ] , ["Player Name","Wins","losses","Chips Won","Chips lost"],  tablefmt="grid"))
    elif len(players)==5:
        print(tabulate([  [ players[1].name , players[1].wins , players[1].losses , players[1].chips.won , players[1].chips.lost ]  ,
                          [ players[2].name , players[2].wins , players[2].losses , players[2].chips.won , players[2].chips.lost ]  ,
                          [ players[3].name , players[3].wins , players[3].losses , players[3].chips.won , players[3].chips.lost ]  ,
                          [ players[4].name , players[4].wins , players[4].losses , players[4].chips.won , players[4].chips.lost ]  ] , ["Player Name","Wins","losses","Chips Won","Chips lost"],  tablefmt="grid"))



def player_busts(player):
    
    '''
    INPUT:      current_player object of Player class
    PURPOSE:    For 'Player Busted' events
                Changes player attributes accordingly
    '''
    
    print(f"{player.name}, unfortunately you've been busted.\n\n")
    player.losses+=1
    player.chips.lose_bet()
    player.playing=False
    input('Press Enter To Continue')



def dealer_busts():
    
    '''
    PURPOSE:    For 'Dealer Busted' events
                Changes all unbusted players' attributes accordingly
    '''
    
    global players
    for i in range(1,len(players)):
        if players[i].playing:
            player_wins(players[i])
        pass
        


def player_wins(player):
    
    '''
    INPUT:      current_player object of Player class
    PURPOSE:    For 'Player Wins' events
                Changes player attributes accordingly
    '''
    
    print(f"{player.name}, you win the bet! Congratulations!\n\n")
    player.wins+=1 
    player.chips.win_bet()
    player.playing=False



def player_loses(player):
    
    '''
    INPUT:      current_player object of Player class
    PURPOSE:    For 'Player Loses' events
                Changes player attributes accordingly
    '''
    
    print(f"{player.name}, you've lost the bet. Good luck next time.\n\n")
    player.losses+=1 
    player.chips.lose_bet()
    player.playing=False



def player_push(player):
    
    '''
    INPUT:      current_player object of Player class
    PURPOSE:    For 'Player and Dealer Tied' events
                Changes player attributes accordingly
    '''
    
    print(f"{player.name}, it's a push. Well done.\n\n")
    player.chips.bet=0
    player.playing=False



def reset_hands():
    
    '''
    PURPOSE:    Calls both hand reset functions and deck reset function to prepare for next round/session
                To be called after the current round ends
    '''
    
    global players
    global stacked_deck
    for player in players:
        player.reset_hand()
    stacked_deck.reset_deck()
    


def end_of_round(n):
    
    '''
    INPUT:      n                       (current round number)
    PURPOSE:    Handles events after all players and dealer have hit, and have to compare hand values
                Displays end-of-round Table, Player Stats and kicks players who have run out of chips to play
    '''
    
    global players
    clear()
    show_all()
    for i in range(1,len(players)):
        if players[i].playing:
            if players[i].hand.value > players[0].hand.value:
                player_wins(players[i])
            elif players[i].hand.value < players[0].hand.value:
                player_loses(players[i])
            else:
                player_push(players[i])
    input('Press Enter To Continue')
    clear()
    show_stats()
    sleep(1)
    print(f"\n\nRound {n} Over")
    kicked_players=[]
    for i in range(1,len(players)):
        if players[i].chips.total==0:
            print(f"\nLooks like you've run out of Chips, {players[i].name}. Unfortunately you won't be able to play any future rounds")
            kicked_players.append(players[i].name)
            #print(f"Marked {players[i].name} for Kicking")
    for i in range(len(kicked_players)):
        for player in players:
            if player.name in kicked_players:
                #print(f"Kicked {player.name}")
                players.remove(player)
        
    

def driver_fn():
    
    '''
    PURPOSE:    Handles the entire game logic's Big Picture
                Calls all the other functions as and when needed 
    '''
    
    global players
    global stacked_deck
    global n
    print("\nHello and welcome to Py_BlackJack!\nThe rules are pretty much the same as regular BlackJack except for the absence of:\n\t1.\tSplit\n\t2.\tSurrender\n\t3.\tInsurance")
    print("\nYou can play this game on your own against a computerised dealer or along with upto 3 other local friends!\n\nThis particular BlackJack 'Table' follows S17 Rule i.e. if you have a hand with a total value of 17, you have the option to choose to stand.\n\nYou start out with 1000 Chips in your hand. Place bets wisely or risk losing all Chips and getting kicked out.\n\nGood luck players, and have fun! :)")
    input('Press Enter To Continue')
    
    #Session Loop
    while True:
        clear()
        print("\nLoading...\n")
        n=0
        sleep(1.5)
        clear()
        print("Welcome to a new Session players!")
        no_of_players()
        input('Press Enter To Continue')
        #Round Loop
        while True:
            clear()
            n+=1
            print(f"\nRound {n} begins...\n\n")
            sleep(1.5)
            if n>1:
                reset_hands()
            stacked_deck.shuffle()
            for i in range(1,len(players)):
                take_bet(players[i])
            for i in range(2):
                for player in players:
                    hit(player)
            clear()
            show_some()
            sleep(3)
            for i in range(1,len(players)):
                hit_stand_or_double_down_(players[i])
            hit(players[0])
            while True:
                r_choice=input('Play another round everyone? [Y/N]: ')  
                if r_choice == 'N' or r_choice == 'n' or r_choice == 'Y' or r_choice == 'y':
                    break
                else:
                    print("Whoops! Please enter either 'Y' for Yes or 'N' for No only. Try again!")
                    continue
            if r_choice == 'N' or r_choice == 'n':
                break
            else:
                if len(players)==0:
                    print("No players left for playing the next round. Quitting this session..")
                    sleep(1.5)
                    break
                leaving_players=[]
                for i in range(1,len(players)):
                    while True:
                        s_choice=input(f"{players[i].name}, do you wish to play the next round? [Y/N]: ")
                        if s_choice == 'N' or s_choice == 'n' or s_choice == 'Y' or s_choice == 'y':
                            break
                        else:
                            print("Whoops! Please enter either 'Y' for Yes or 'N' for No only. Try again!")
                            continue
                    if s_choice == 'N' or s_choice == 'n':
                        print("Okay. Dropping you out of the Player's List...")
                        leaving_players.append(players[i].name)
                        #print(f"Marked {players[i].name} for Removal")
                        sleep(2)
                    else:
                        continue
                for i in range(len(leaving_players)):
                    for player in players:
                        if player.name in leaving_players:
                            #print(f"Kicked {player.name}")
                            players.remove(player)
                if len(players)==0:
                    print("No players left for playing the next round. Quitting this session..")
                    sleep(1.5)
                    break
        
        while True:
            g_choice=input('Start a new Session? [Y/N]: ')  
            if g_choice == 'N' or g_choice == 'n' or g_choice == 'Y' or g_choice == 'y':
                break
            else:
                print("Whoops! Please enter either 'Y' for Yes or 'N' for No only. Try again!")
                continue
        if g_choice == 'N' or g_choice == 'n':
            break
        else:
            del players
            players=[]
            continue
    print("Thank you for playing Py_BlackJack. Hope you enjoyed it!")
    input('Press Enter To Continue')
    clear()
 
    
driver_fn()
            
        
                
 
            

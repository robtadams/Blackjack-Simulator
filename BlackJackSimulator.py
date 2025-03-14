# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# BlackJackSimulator.py
# Wiley Sheehy
# 3/10/25

# Importing libraries
from random import * 
from time import sleep


# Game
class Game():
    
    # Card class
    class Card():

        # Initialization
        def __init__(self, rank, suit): # Rank, Suit
            self.rank = rank # Set rank
            self.suit = suit # Set suit

        # Getting a card's rank
        def getRank(self):
            return self.rank

        # Getting a card's suit
        def getSuit(self):
            return self.suit

        # Getting a card's blackjack value
        def BJValue(self, numAces = 0): # numAces is the number of aces in a hand
            if self.rank == 1: # Ace
                return 11, numAces + 1 # Return 11 and increase the number of aces
            elif self.rank > 1 and self.rank < 11: # 2 - 10
                return self.rank, 0 # Return the number on the card
            else: # Faces
                return 10, 0 # Face cards return 10

        # Getting a card's name
        def __str__(self):
            # Dictionary for the spelling of a card's rank
            rankDict = { 1:"Ace", 2:"Two", 3:"Three", 4:"Four", 5:"Five", 6:"Six", 7:"Seven", 8:"Eight", 9:"Nine", 10:"Ten", 11:"Jack", 12:"Queen", 13:"King"}

            # Dictionary for the speeling of a card's suit
            suitDict = { "d":"Diamonds", "c":"Clubs", "h":"Hearts", "s":"Spades"}
            return rankDict[self.rank] + " of " + suitDict[self.suit] # Return name

    # Main loop function
    def main(self):

        # Set up the deck
        self.SetUp()

        # Main loop 
        while self.running:
            
            """ Betting """

            # Print balance
            print("You have ${}".format(self.wallet))

            # Set bet to none
            self.bet = None

            # Asking for bet
            while self.bet == None:

                """ Making sure bet is valid """
                try: # Try the bet
                    self.bet = eval(input("\nHow much money are you going to bet? :"))
                
                except NameError: # If it is a variable

                    print("Please enter a valid input.")

                except SyntaxError: # If it is not a number

                    print("Please enter a valid input.")

                else: # If it is valid

                    if self.bet > self.wallet: # If the bet is greater than the balance
                        print("You can't bet more than you have.") # Print
                        self.bet = None # Reset bet
                    elif self.bet < 0: # If the bet is negative
                        print("You can't bet a negative amount.") # Print
                        self.bet = None # Reset bet
                    elif self.bet == 0: # If the bet is zero
                        print("If you aren't going to bet anything, you can't play.") # Print
                        sleep(1) # Wait 1 second
                        return # Stop playing

                
            print("------------------------------------------- \n\n")
            outcome = self.Game() # If the player wins or looses. Outcome is the multiplier for how much the player is paid
            self.wallet += self.bet * outcome # <-- Moved self.Game() up a line
        
    def SetUp(self):
        
        # Set up money
        self.wallet = 1000

        self.running = True

        # Set the number of aces in a hand to 0
        self.numAces = 0

        # Loop
        while True:
            try: # Try the number of decks
                self.deckNum = eval(input("How many decks are you playing with? :"))

            except: # If it isn't valid
                print("That was not a valid input.")

            else: # If it is valid
                if self.deckNum > 0:
                    break
                else: 
                    print("That was not a valid input.")

        self.buildDeck()

    def buildDeck(self):
                  
        self.deck = [] # Deck

        print("Building deck", end="", flush=True)
        for i in range(3):
            sleep(0.7)
            print(".", end="", flush=True)
        sleep(1)
        print("\n-------------------------------------------------------------------------------------")
        
        for i in range(self.deckNum): # For every deck
            
            for j in range(13): # For every rank
                
                for k in ["d", "c", "h", "s"]: # For every suit
                    
                    card = self.Card(1 + j, k) # Create a card
                    self.deck.append(card) # Add it to the deck
                    
        shuffle(self.deck) # Shuffle deck

    def Game(self):
        
        self.Start()
        isStanding = False
        isSplitting = False

        print("You have a {} and a {}, totaling to {}".format(self.playerHand[0], self.playerHand[1], self.playerTotal))

        # Player's turn
        while self.playerTotal <= 21 and isStanding == False:
            Action = input("Type in what are you going to do :")
            match Action:
                case "hit":
                    card, self.playerTotal = self.Hit(self.playerHand, self.playerTotal)
                    print("You draw a {}.".format(str(card)))
                case "stand":
                    isStanding = True
                case "double down":
                    self.bet = self.bet * 2
                    print(self.bet)
                    card, self.playerTotal = self.Hit(self.playerHand, self.playerTotal)
                    print("You draw a {}.".format(str(card)))
                    isStanding = True
                case "split":
                    
                    # check if player has 2 cards
                    if len(self.playerHand) == 2 and self.playerHand[0].BJValue() == self.playerHand[1].BJValue():
                        isSplitting = True
                        # check if player's cards are the same rank ^                  
                        # transfer one card to another hand
                        Hand2 = [self.playerHand.pop()]
                        Total2 = Hand2[0].BJValue()[0]
                        self.playerTotal = self.playerHand[0].BJValue()[0]
                        # duplicate bet on the other hand
                        # ask if they are going to hit on their first hand
                        print("You have {} on your first hand".format(self.playerTotal))
                        Action = input("Type in if you are going to hit or stand. \n (You can only hit once) :")
                        match Action:
                            case "hit":
                                card, self.playerTotal = self.Hit(self.playerHand, self.playerTotal)
                                print("You draw a {}.".format(str(card)))
                                isStanding = True
                            case "stand":
                                isStanding = True
                        # ask if they are going to hit on their second hand
                        print("You have {} on your second hand".format(Total2))
                        Action = input("Type in what are you going to do on your second hand. \n (You can only hit once) :")
                        match Action:
                            case "hit":
                                card, Total2 = self.Hit(Hand2, Total2)
                                print("You draw a {}.".format(str(card)))
                                isStanding = True
                            case "stand":
                                isStanding = True
                        # compare results on both hands
                    else:
                        print("You cannot split.")
        

        if self.playerTotal == 21 and len(self.playerHand) == 2 and self.dealerTotal != 21:
            print("You got a BlackJack, you win")
            return 1.5

        else:
            # Dealer's turn
            print("The dealer's full hand is {} and {}.".format(str(self.dealerHand[0]), str(self.dealerHand[1])))
            while self.dealerTotal < 17:
                var, self.dealerTotal = self.Hit(self.dealerHand, self.dealerTotal)
                sleep(1)
                print("\nThe dealer drew {}. Their total is {}.".format(str(var), self.dealerTotal))

            # Outcome

            outcome = 0

            if isSplitting:
                if Total2 > 21:
                    print("You bust with a total of {}, the Dealer wins.".format(Total2))
                    outcome += -1
                elif self.dealerTotal == Total2:
                    print("You matched the dealer's total of {}. It's a push. Nobody wins.".format(self.dealerTotal))
                    outcome += 0
                elif self.dealerTotal > 21 or Total2 > self.dealerTotal:
                    print("You have a total of {}, the dealer has a total of {}. You win!".format(Total2, self.dealerTotal))
                    outcome += 1
                else:
                    print("The dealer has a total of {}, which is more than your total of {}. You lose.".format(self.dealerTotal, Total2))
                    outcome += -1

            
            if self.playerTotal > 21:
                print("You bust with a total of {}, the Dealer wins.".format(self.playerTotal))
                return -1 + outcome
            if self.dealerTotal == self.playerTotal:
                print("You matched the dealer's total of {}. It's a push. Nobody wins.".format(self.dealerTotal))
                return 0 + outcome
            if self.dealerTotal > 21 or self.playerTotal > self.dealerTotal:
                print("You have a total of {}, the dealer has a total of {}. You win!".format(self.playerTotal, self.dealerTotal))
                return 1 + outcome
            print("The dealer has a total of {}, which is more than your total of {}. You lose.".format(self.dealerTotal, self.playerTotal))
            return -1 + outcome

        self.buildDeck()

    def Hit(self, hand, total):

        if len(self.deck) == 0:
            self.buildDeck()
            
        card = self.deck.pop()
        hand.append(card)

        cardVal, numAces = card.BJValue(self.numAces)
        total += cardVal
        self.numAces += numAces

        # If you would bust off of an Ace...
        if total > 21 and numAces > 0:

            self.numAces -= 1
            # Then only add 1 to your total, not 11
            total -= 10
            
        return card, total
            

    def Start(self):

        self.playerHand = []
        self.dealerHand = []
        
        self.playerTotal = 0
        self.dealerTotal = 0
        
        for i in range(2):
            var, self.playerTotal = self.Hit(self.playerHand, self.playerTotal)
            var, self.dealerTotal = self.Hit(self.dealerHand, self.dealerTotal)
        print("The dealer is showing {}.".format(self.dealerHand[0]))

        

game = Game()
game.main()
    
                     

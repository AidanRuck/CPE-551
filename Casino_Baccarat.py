"""
Final Project for CPE 551: Engineering Programming with Python
By: Aidan Ruck
Due: May 2025

Project Title: Casino Baccarat

Description:
This python program simulates a simplified game of Baccarat between a player and a banker (the dealer).
Baccarat is a popular casino game where the objective is to bet on which hand will win,
either Player or Banker, and have a total closest to 9. Cards are drawn from a standard 52-Card
deck. The scoring follows traditional Baccarat rules:

    - Aces are 1 point
    - 2-9 are face value
    - 10s and Face cards (Jack, Queen, King) are worth 0
    - Only the last digit of the total score is used (e.g. if the total is 15 it becomes 5)

Gameplay:
- The user starts with a virtual wallet and will place a bet each round
- The betting options:
    1. Player wins (which pays 2:1)
    2. Banker wins (which pays 2:1)
    3. Tie (pays 8:1)
- Two cards are dealt to Player and Banker
- Depending on what is scored, a fifth card may be drawn using the same rules
- The winner is determined by the final hand value. Ties result in a push if they are not bet on.

Structure:
1. Card Class:
    This defines the properties and Baccarat value of a playing card (suit and rank)
2. Deck Class:
    Manages the creation, shuffling, and dealing of the deck
3. BaccaratGame Class:
    Manages the logic, betting, drawing, scoring, and user interactions
    This includes:
        - draw_card(): draws and prints the card for player
        - draw_third_card(): handles the third card rules
        - calculate_score(): calculates the hand score (mod 10)
        - display_table(): prints the current hands and scores
        - play_round(): processes the full round including the bets and resolution
        - play_game(): loop for multiple rounds
"""

import random

# Start given code from Lecture 9
class Card:
    suit_list = ["Clubs", "Diamonds", "Hearts", "Spades"]
    rank_list = ["None", "Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]

    def __init__(self, suit = 0, rank = 2):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank_list[self.rank]} of {self.suit_list[self.suit]}"
# End of given code from Lecture 9

    # In Baccarat, an Ace is 1 (because you take first digit only of 11), 2-9 are face, and 10s and Face cards are worth 0 (they're ten, but first digit is zero)
    def baccarat_value(self):
        return min(self.rank, 9) if self.rank < 10 else 0
    
# Create new class for the deck of cards for the game
class Deck:
    # Create deck of 52 cards (standard size)
    def __init__(self):
        self.cards = [Card(suit, rank) for suit in range(4) for rank in range(1, 14)]

    # Create a shuffle for deck (cards in random order)
    def shuffle(self):
        # Uses random package to shuffle the deck
        random.shuffle(self.cards)

    # Deal a card (pop the top card of deck)
    def deal(self):
        return self.cards.pop()
    
# Create class for the game itself
class BaccaratGame:
    def __init__(self):
        # Create new deck
        self.deck = Deck()
        # Shuffle new deck
        self.deck.shuffle()
        # Create virtual wallet with $100 starting cash
        self.wallet = 100
        
    def calculate_score(self, hand):
        # Calculate the hand scores, only the first (ones) digit counts
        return sum(card.baccarat_value() for card in hand) % 10 #Modulo 10 to remove tenths place digit
    
    # If a hand is under or equal to 5, draw a third card (rule of the game)
    def draw_third_card(self, hand, score):
        if score <= 5:
            hand.append(self.deck.deal())

    # Create simple hand vizualisation
    def display_table(self, player_hand, banker_hand, player_score, banker_score):
        print("\n~~~~~~~~~~~~~~~~~ Baccarat Table ~~~~~~~~~~~~~~~~~")
        print("Player Hand:", ', '.join(str(card) for card in player_hand))
        print("Banker Hand:", ', '.join(str(card) for card in banker_hand))
        print(f"Player Score: {player_score}")
        print(f"Banker Score: {banker_score}")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    def draw_card(self, recipient_name, hand):
        card = self.deck.deal()
        hand.append(card)
        print(f"{recipient_name} draws: {card}")
        return card
    
    def draw_third_card(self, name, hand, score):
        if score <= 5:
            print(f"{name} draws a third card (score <= 5)")
            self.draw_card(name, hand)

    def play_round(self):
        # Detect if game is over
        if self.wallet <= 0:
            print("Unfortunately you have run out of money! Time to head home from the Casino.")
            return False
        
        # Main game menu choice
        # Player and Banker pay 2:1, Tie pays 8:1
        print(f"Your Wallet: ${self.wallet}")
        print("Choose your bet: ")
        print("1 - Player (2:1)")
        print("2 - Banker (2:1)")
        print("3 - Tie (8:1)")
        bet_choice = input("Enter your choice (1, 2, or 3): ")

        # Handles wrong inputs
        while bet_choice not in ['1', '2', '3']:
            bet_choice = input("Invalid selection. Please enter 1, 2, or 3: ")

        # Handles virtual wallet bets
        bet_amount = int(input("Please enter your bet amount: "))
        if bet_amount > self.wallet:
            print("You cannot bet more than you have! Try again.")
            return True
    
        # Deal initial cards
        player_hand = []
        banker_hand = []

        self.draw_card("Player", player_hand)
        self.draw_card("Banker", banker_hand)
        self.draw_card("Player", player_hand)
        self.draw_card("Banker", banker_hand)

        player_score = self.calculate_score(player_hand)
        banker_score = self.calculate_score(banker_hand)

        # Rules to draw a third card (if player is under or equal to 5)
        if player_score <= 5:
            self.draw_third_card("Player", player_hand, player_score)

        # Banker draws a third card (if banker is under or equal to 5)
        if banker_score <= 5:
            self.draw_third_card("Banker", banker_hand, banker_score)

        # Recalculate score after the third card is drawn (final score)
        player_score = self.calculate_score(player_hand)
        banker_score = self.calculate_score(banker_hand)

        # Show table
        self.display_table(player_hand, banker_hand, player_score, banker_score)

        # Determine outcome of hand
        result = "Tie"
        if player_score > banker_score:
            result = "Player"
        elif banker_score > player_score:
            result = "Banker"

        print("Result: ", result)

        # Determine if the player won
        # Win or lose, print winnings or losses
        if result == "Tie":
            if bet_choice == '3':
                winnings = bet_amount * 8
                print("You Won with a Tie! +${}".format(winnings - bet_amount))
                self.wallet += winnings - bet_amount
            else:
                # You do not lose if it is a tie and you did not bet tie
                print("It's a tie! Your bet was returned to you (Pushed).")
        elif bet_choice == '1' and result == "Player":
            winnings = bet_amount * 2
            print("You Won! +${}".format(winnings - bet_amount))
            self.wallet += bet_amount
        elif bet_choice == '2' and result == "Banker":
            winnings = int(bet_amount * 2) # At a real casino, house would take commission
            print("You Won! +${}".format(winnings - bet_amount))
            self.wallet += winnings - bet_amount
        else:
            print("You Lost! -${}".format(bet_amount))
            self.wallet -= bet_amount

        return True
    
    def play_game(self):
        print("Welcome to Casino Baccarat!")
        # Keep playing rounds until player wants to stop or cannot (loses all money)
        while True:
            if not self.play_round():
                break
            cont = input("Play another round? (y/n): ").lower()
            if cont != 'y':
                print("Game Over! Final Wallet: ${}".format(self.wallet))
                break
                
# Runs game (like a main() file)
if __name__ == "__main__":
    game = BaccaratGame()
    game.play_game()

# Lab 4 - game of go fish.  Team 7 (Vincent, Yvette)
# uses insertion sort

import random

# Card class representing a single playing card
class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return f"{self.rank} of {self.suit}"

# Deck class to manage a deck of cards
class Deck:
    def __init__(self):
        self.cards = []
        self.initialize_deck()

    def initialize_deck(self):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.cards = [Card(rank, suit) for suit in suits for rank in ranks]

    def shuffle_cards(self):
        random.shuffle(self.cards)

    def draw_card(self):
        if self.cards:
            return self.cards.pop()
        else:
            return None

# Player class to manage each player's hand
class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.books = []

    # Use insertion sort to keep the hand sorted after adding new cards
    def sort_hand(self):
        rank_order = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
        for i in range(1, len(self.hand)):
            key_card = self.hand[i]
            key_rank = rank_order[key_card.rank]
            j = i - 1
            while j >= 0 and rank_order[self.hand[j].rank] > key_rank:
                self.hand[j + 1] = self.hand[j]
                j -= 1
            self.hand[j + 1] = key_card

    def manage_player_hand(self, card):
        if card:
            self.hand.append(card)
            self.sort_hand()  # Sort the hand after adding a new card

    def ask_for_card(self):
        rank_order = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
        valid_ranks = sorted(set(card.rank for card in self.hand), key=lambda rank: rank_order[rank])

        while True:
            rank = input(f"{self.name}, which rank do you want to ask for? ({', '.join(valid_ranks)})\n")
            if rank not in valid_ranks:
                print("Invalid rank, please try again.")
            else:
                return rank

    def check_for_books(self):
        ranks_count = {}
        for card in self.hand:
            ranks_count[card.rank] = ranks_count.get(card.rank, 0) + 1
        books = [rank for rank, count in ranks_count.items() if count == 4]

        # Remove books from hand and add them to the player's books
        for book in books:
            self.hand = [card for card in self.hand if card.rank != book]
            self.books.append(book)

        return books

# GoFish class to manage the game
class GoFish:
    def __init__(self):
        self.players = []
        self.deck = None  # Initialize the deck to None
        self.current_turn = 0

    def initialize_game(self):
        self.deck = Deck()
        while True:
            try:
                num_players = int(input("Enter the number of players (2-8): "))
                if num_players < 2 or num_players > 8:
                    raise ValueError  # Trigger the error if invalid
                break
            except ValueError:
                print("Invalid entry, please try again. You must enter a number between 2 and 8.")

        for i in range(num_players):
            if i == 0:
                self.players.append(Player("comp"))  # Computer player
            else:
                name = input(f"Enter the name of player {i}: ")
                self.players.append(Player(name))

        # Shuffle the deck and deal cards
        self.deck.shuffle_cards()
        self.deal_cards(num_players)

    def deal_cards(self, num_players):
        num_cards = 7 if num_players < 5 else 5
        for _ in range(num_cards):
            for player in self.players:
                card = self.deck.draw_card()
                if card:
                    player.manage_player_hand(card)

    def determine_turn(self):
        self.current_turn = (self.current_turn + 1) % len(self.players)

    """def check_end_game(self):
    # Check if the deck is empty
        if len(self.deck.cards) == 0:
            return True

    # Check if any player has no cards but has at least one book
        for player in self.players:
            if len(player.hand) == 0 and len(player.books) > 0:
                return True

    # Otherwise, the game continues
        return False"""

    def check_end_game(self):
    # End the game if the deck is empty
        if len(self.deck.cards) == 0:
            return True

    # End the game if any player has no cards left and has at least one book
        for player in self.players:
            if len(player.hand) == 0 and len(player.books) > 0:
                return True

    # Otherwise, the game continues
        return False



    def play_turn(self):
        current_player = self.players[self.current_turn]

        # If it's the computer's turn
        if current_player.name == "comp":
            rank = random.choice([card.rank for card in current_player.hand])
            target_player = random.choice([player for player in self.players if player != current_player])
            print(f"{current_player.name} asks {target_player.name} for {rank}.")
            self.process_request(target_player, rank)
        else:
            rank = current_player.ask_for_card()

            # If there are only 2 players, the human can only ask the computer
            if len(self.players) == 2:
                target_player = self.players[0]  # 'comp' is always at index 0
            else:
                target_player = self.select_target_player(current_player)

            print(f"{current_player.name} asks {target_player.name} for {rank}.")
            self.process_request(target_player, rank)

        # Display the books (if any) of the current player
        books = current_player.check_for_books()
        if books:
            print(f"{current_player.name} completed a book: {', '.join(books)}")
        else:
            print(f"{current_player.name} has no completed books this turn.")

        self.determine_turn()

    def select_target_player(self, current_player):
        available_players = [player for player in self.players if player != current_player]
        print(f"Available players to ask: {', '.join([p.name for p in available_players])}")

        while True:
            target_name = input(f"{current_player.name}, who do you want to ask for a card from? ")
            target_player = next((player for player in available_players if player.name == target_name), None)
            if target_player:
                return target_player
            print("Invalid player, please try again.")

    def process_request(self, target_player, rank):
        cards_found = [card for card in target_player.hand if card.rank == rank]
        for card in cards_found:
            target_player.hand.remove(card)
            self.players[self.current_turn].manage_player_hand(card)

        if cards_found:
            print(f"{target_player.name} has {len(cards_found)} card(s) of rank {rank}.")
        else:
            print(f"{target_player.name} does not have that rank. Go Fish!")
            self.players[self.current_turn].manage_player_hand(self.deck.draw_card())

    def announce_winner(self):
        books_count = {player.name: len(player.books) for player in self.players}
        print("Final Books Count:")
        for player, count in books_count.items():
            print(f"{player}: {count} book(s)")

        max_books = max(books_count.values())
        winners = [name for name, count in books_count.items() if count == max_books]

        if winners:
            print(f"The winner(s): {', '.join(winners)} with {max_books} book(s)!")
        else:
            print("No books were completed.")



# Main game loop
def main():
    game = GoFish()
    game.initialize_game()
    
    # Main gameplay loop
    while not game.check_end_game():  # Keep playing until the game should end
        game.play_turn()

    game.announce_winner()  # Announce the winner once the game ends
    play_again = input("Do you want to play again? (yes/no): ").strip().lower()
    if play_again == 'yes':
        main()  # Restart the game
    else:
        print("Great game! See you next time!")


if __name__ == "__main__":
    main()

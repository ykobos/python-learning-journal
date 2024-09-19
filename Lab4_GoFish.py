import random

# Card class represents a single card with rank and suit
class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return f"{self.rank} of {self.suit}"

# Deck class manages a deck of 52 cards
class Deck:
    def __init__(self):
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        self.cards = [Card(rank, suit) for rank in ranks for suit in suits]
        self.shuffle_deck()

    # Shuffle the deck
    def shuffle_deck(self):
        random.shuffle(self.cards)

    # Draw a card from the deck
    def draw_card(self):
        return self.cards.pop() if self.cards else None

# Player class manages a player's hand and actions
class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.books = []

    def __repr__(self):
        return self.name

    # Sort player's hand using insertion sort
    def sort_hand(self):
        for i in range(1, len(self.hand)):
            key = self.hand[i]
            j = i - 1
            while j >= 0 and self.hand[j].rank > key.rank:
                self.hand[j + 1] = self.hand[j]
                j -= 1
            self.hand[j + 1] = key

    # Check if player has a rank in their hand
    def has_rank(self, rank):
        return any(card.rank == rank for card in self.hand)

    # Ask another player for cards of a particular rank
    def ask_for_card(self, other_player, rank):
        cards = [card for card in other_player.hand if card.rank == rank]
        for card in cards:
            other_player.hand.remove(card)
        return cards

    # Check for books (sets of 4 cards of the same rank)
    def check_for_books(self):
        rank_count = {}
        for card in self.hand:
            rank_count[card.rank] = rank_count.get(card.rank, 0) + 1

        for rank, count in rank_count.items():
            if count == 4:
                print(f"{self.name} made a book of {rank}s!")
                self.books.append(rank)
                self.hand = [card for card in self.hand if card.rank != rank]

    # Draw a card from the deck (Go Fish)
    def go_fish(self, deck):
        card = deck.draw_card()
        if card:
            print(f"{self.name} draws a card: {card}")
            self.hand.append(card)
            self.sort_hand()
        else:
            print("The deck is empty, no cards to draw.")

# GoFishGame class manages the game flow
class GoFishGame:
    def __init__(self, players):
        self.players = players
        self.deck = Deck()

        # Deal 7 cards for 2-4 players, 5 cards for 5-8 players
        if len(players) <= 4:
            self.deal_cards(7)
        else:
            self.deal_cards(5)

    # Deal cards to each player
    def deal_cards(self, num_cards):
        for player in self.players:
            for _ in range(num_cards):
                player.hand.append(self.deck.draw_card())
            player.sort_hand()

    # Play a player's turn
    def player_turn(self, player):
        print(f"\n{player.name}'s turn.")
        if len(player.hand) == 0:
            print(f"{player.name} has no cards left.")
            return

        # Computer's move (randomly choose a card and player to ask)
        if player.name == "computer_player":
            other_player = random.choice([p for p in self.players if p != player])
            chosen_card = random.choice(player.hand)
            rank = chosen_card.rank
            print(f"Computer asks {other_player.name} for {rank}s.")
            self.ask_for_card_interaction(player, other_player, rank)
            player.check_for_books()
            return

        # Human player's turn
        self.show_player_hand(player)
        other_player_name = input(f"Who do you want to ask for a card? (Available players: {', '.join(p.name for p in self.players if p != player)}): ").strip()
        other_player = self.get_player_by_name(other_player_name)
        if other_player is None or other_player == player:
            print("Invalid choice, try again.")
            return self.player_turn(player)

        rank = input(f"What rank do you want to ask {other_player_name} for? ").strip().upper()
        if not player.has_rank(rank):
            print(f"You don't have any {rank}s in your hand!")
            return self.player_turn(player)

        self.ask_for_card_interaction(player, other_player, rank)
        player.check_for_books()

    # Handle interaction when a player asks for a card
    def ask_for_card_interaction(self, player, other_player, rank):
        cards = other_player.ask_for_card(other_player, rank)
        if cards:
            print(f"{other_player.name} gives {len(cards)} {rank}(s) to {player.name}.")
            player.hand.extend(cards)
        else:
            print(f"{other_player.name} says 'Go Fish!'")
            player.go_fish(self.deck)

    # Check if the game has ended
    def check_game_end(self):
        return all(not player.hand for player in self.players) or not self.deck.cards

    # Display the books of each player at the end of the game
    def display_books(self):
        print("\nGame over! Here are the final books:")
        for player in self.players:
            print(f"{player.name}: {', '.join(player.books) if player.books else 'No books'}")

    # Play the full game
    def play_game(self):
        while not self.check_game_end():
            for player in self.players:
                self.player_turn(player)
                if self.check_game_end():
                    break
        self.display_books()

    # Show the current hand of a player
    def show_player_hand(self, player):
        print(f"{player.name}'s hand: {', '.join(str(card) for card in player.hand)}")

    # Get player by name
    def get_player_by_name(self, name):
        for player in self.players:
            if player.name.lower() == name.lower():
                return player
        return None

# Setup game: Prompt for player names and number of players
def setup_game():
    num_players = int(input("Enter the number of players (2-8, including the computer): "))
    while num_players < 2 or num_players > 8:
        num_players = int(input("Please enter a valid number of players (2-8): "))

    players = []
    for i in range(num_players - 1):
        player_name = input(f"Enter the name of player {i+1}: ").strip()
        players.append(Player(player_name))

    # Add the computer player as 'computer_player'
    players.append(Player("computer_player"))
    return players

# Main program
if __name__ == "__main__":
    players = setup_game()
    game = GoFishGame(players)
    game.play_game()



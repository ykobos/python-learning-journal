# Team 2 (Yasmeen, Yvette)
# use this version to turn in

import random
import tkinter as tk

# Node for linked list implementation of the deck
class Node:
    def __init__(self, card):
        self.card = card
        self.next = None

# Base class for cards
class Card:
    def __init__(self, name, description, cost):
        self.name = name
        self.description = description
        self.cost = cost

    def play(self, player, opponent):
        pass

# Unit card class inheriting from Card
class UnitCard(Card):
    def __init__(self, name, description, cost, attack, hp):
        super().__init__(name, description, cost)
        self.attack = attack
        self.hp = hp
        self.remaining_uses = 2  # Each UnitCard should start with its own uses
        self.can_attack = True

    def play(self, player, opponent):
        # Add the unit card to the player's battlefield
        player.battlefield.append(self)

    def attack_opponent(self, player, opponent):
        if self.remaining_uses > 0 and self.can_attack:
            opponent.hp -= self.attack
            self.remaining_uses -= 1
            if self.remaining_uses == 0:
                # Remove the card from the battlefield once it has no uses left
                player.battlefield.remove(self)
            return True
        return False

# Spell card class inheriting from Card
class SpellCard(Card):
    def __init__(self, name, description, cost, effect):
        super().__init__(name, description, cost)
        self.effect = effect

    def play(self, player, opponent):
        if self.effect == "damage":
            opponent.hp -= 1
        elif self.effect == "heal":
            player.hp += 2
        elif self.effect == "defend":
            player.hp -= 1
            # Reduce remaining uses of opponent's Savage Strike cards by 1
            for card in opponent.battlefield:
                if isinstance(card, UnitCard) and card.name == "Savage Strike":
                    card.remaining_uses -= 1
                    if card.remaining_uses <= 0:
                        opponent.battlefield.remove(card)

# Deck class implemented as a linked list
class Deck:
    def __init__(self):
        self.head = None
        self.size = 0

    def add_card(self, card):
        new_node = Node(card)
        new_node.next = self.head
        self.head = new_node
        self.size += 1

    def draw_card(self):
        if self.head is None:
            return None
        drawn_card = self.head.card
        self.head = self.head.next
        self.size -= 1
        return drawn_card

    def shuffle(self):
        cards = []
        current = self.head
        while current is not None:
            cards.append(current.card)
            current = current.next
        random.shuffle(cards)
        self.head = None
        for card in cards:
            self.add_card(card)

# Player class
class Player:
    def __init__(self, name, deck):
        self.name = name
        self.hp = 20
        self.deck = deck
        self.hand = []
        self.battlefield = []

    def draw_card(self):
        card = self.deck.draw_card()
        if card:
            self.hand.append(card)

    def play_card(self, card_index, opponent):
        if 0 <= card_index < len(self.hand):
            card = self.hand.pop(card_index)
            card.play(self, opponent)

    def end_turn(self):
        for card in self.battlefield:
            if isinstance(card, UnitCard):
                card.can_attack = True

# GUI class
class CardGameGUI:
    def __init__(self, root):
        self.root = root
        self.current_player = None
        self.opponent = None
        self.card_drawn = False

        # UI setup
        self.hp_label = tk.Label(root, text="")
        self.hp_label.pack()

        self.hand_frame = tk.Frame(root)
        self.hand_frame.pack()

        self.battlefield_frame = tk.Frame(root)
        self.battlefield_frame.pack()

        self.draw_button = tk.Button(root, text="Draw Card", command=self.draw_card)
        self.draw_button.pack()

        self.end_turn_button = tk.Button(root, text="End Turn", command=self.end_turn)
        self.end_turn_button.pack()

        self.log_text = tk.Text(root, height=10, width=50)
        self.log_text.pack()

        # Initialize game
        self.initialize_game()

    def initialize_game(self):
        deck1 = create_deck()
        deck2 = create_deck()

        self.player1 = Player("Player 1", deck1)
        self.player2 = Player("Player 2", deck2)

        self.current_player = self.player1
        self.opponent = self.player2

        self.update_display()

    def draw_card(self):
        if not self.card_drawn:
            self.current_player.draw_card()
            self.card_drawn = True
            self.update_display()

            # Get details of the drawn card
            drawn_card = self.current_player.hand[-1]  # Get the last card drawn
            self.log_text.insert(tk.END, f"{self.current_player.name} drew {drawn_card.name}: {drawn_card.description}. Points: {self.get_card_points(drawn_card)}\n")

    def play_card(self, card_index):
        if 0 <= card_index < len(self.current_player.hand):
            self.current_player.play_card(card_index, self.opponent)
            self.update_display()
            self.log_text.insert(tk.END, f"{self.current_player.name} played a card.\n")

    def attack_with_unit(self, unit_index):
        if 0 <= unit_index < len(self.current_player.battlefield):
            unit_card = self.current_player.battlefield[unit_index]
            if isinstance(unit_card, UnitCard) and unit_card.can_attack:
                if unit_card.attack_opponent(self.current_player, self.opponent):
                    self.update_display()
                    self.log_text.insert(tk.END, f"{self.current_player.name} attacked with {unit_card.name}.\n")

    def end_turn(self):
        self.card_drawn = False
        self.current_player.end_turn()
        self.current_player, self.opponent = self.opponent, self.current_player
        self.update_display()
        self.log_text.insert(tk.END, f"{self.current_player.name}'s turn.\n")

    def update_display(self):
        # Update HP display
        self.hp_label.config(text=f"{self.current_player.name} HP: {self.current_player.hp} - {self.opponent.name} HP: {self.opponent.hp}")

        # Clear previous buttons for the hand and battlefield
        for widget in self.hand_frame.winfo_children():
            widget.destroy()
        for widget in self.battlefield_frame.winfo_children():
            widget.destroy()

        # Update hand display
        for i, card in enumerate(self.current_player.hand):
            button = tk.Button(self.hand_frame, text=card.name, command=lambda i=i: self.play_card(i))
            button.pack(side=tk.LEFT)

        # Update battlefield display
        for i, unit in enumerate(self.current_player.battlefield):
            button = tk.Button(self.battlefield_frame, text=f"{unit.name} (Uses left: {unit.remaining_uses})", command=lambda i=i: self.attack_with_unit(i))
            button.pack(side=tk.LEFT)

    def get_card_points(self, card):
        """Return points gained/lost based on the card type."""
        if isinstance(card, UnitCard):
            return f"Attack {card.attack}, HP {card.hp}"
        elif isinstance(card, SpellCard):
            if card.effect == "damage":
                return "-1 HP to opponent"
            elif card.effect == "heal":
                return "+2 HP to player"
            elif card.effect == "defend":
                return "-1 HP to player, reduce opponent's attacks"
        return ""

# Create a deck of cards
def create_deck():
    deck = Deck()
    for _ in range(5):
        savage_strike_card = UnitCard("Savage Strike", "A powerful attack unit.", 3, 2, 1)
        deck.add_card(savage_strike_card)

    for _ in range(5):
        viper_bite_card = SpellCard("Viper's Bite", "Instant damage to opponent.", 2, "damage")
        deck.add_card(viper_bite_card)

    for _ in range(5):
        divine_renewal_card = SpellCard("Divine Renewal", "Heal yourself.", 2, "heal")
        deck.add_card(divine_renewal_card)

    for _ in range(5):
        ironclad_wall_card = SpellCard("Ironclad Wall", "Defend and reduce opponent's attack uses.", 3, "defend")
        deck.add_card(ironclad_wall_card)

    deck.shuffle()
    return deck

# Run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    gui = CardGameGUI(root)
    root.mainloop()

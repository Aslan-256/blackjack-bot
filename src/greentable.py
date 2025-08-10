from dealer import Dealer
from deck import Deck
from player import Player

class GreenTable:
    def __init__(self, verbose: bool = False):
        self.dealer = Dealer()
        self.players = [Player()]
        self.deck = Deck()
        self.verbose = verbose

    def check_winners(self):
        results = []
        for player in self.players:
            if player.is_busted():
                results.append(-1)
            elif self.dealer.is_busted() or player.get_hand_value() > self.dealer.get_hand_value() or (player.has_blackjack() and not self.dealer.has_blackjack()):
                results.append(1)
            elif player.get_hand_value() < self.dealer.get_hand_value() or (self.dealer.has_blackjack() and not player.has_blackjack()):
                results.append(-1)
            else:
                results.append(0)
        return results

    def dealer_turn_need(self):
        return not all(player.is_busted() for player in self.players)

    def start_game(self):
        self.log("Starting a new game...\n")

        # Shuffle deck if needed (if the index is at or beyond the black index)
        if self.deck.need_to_shuffle():
            self.deck.shuffle_deck()

        # Reset players and dealer
        self.players = [Player()]
        self.dealer.reset()

        # Deal initial cards
        self.players[0].add_card(self.deck.draw_card())
        self.dealer.add_card(self.deck.draw_card())
        self.players[0].add_card(self.deck.draw_card())
        self.dealer.add_card(self.deck.draw_card())
        self.log(f"Dealer's known card: {self.dealer.get_known_card().get_value()}\nPlayer's hand: {self.players[0].get_list_of_cards()}\n")

        # Player's turn, possible splitted
        self.log(f"Player's turn\nPlayer's hand: {self.players[0].get_list_of_cards()}\n")
        num_remaining_players = len(self.players)
        while num_remaining_players > 0:
            p = self.players[-1]
            num_remaining_players -= 1
            while True:
                if p.is_busted():
                    self.log("Player busted.")
                    break
                action = p.play(self.dealer.get_known_card())
                match action:
                    case 0:  # Hit
                        p.add_card(self.deck.draw_card())
                        self.log(f"Player choose to hit.\nPlayer's hand after hit: {p.get_list_of_cards()}\n")
                    case 1:  # Double Down
                        p.add_card(self.deck.draw_card())
                        self.log(f"Player choose to double down.\nPlayer's hand after double down: {p.get_list_of_cards()}\n")
                        break
                    case 2:  # Stand
                        self.log(f"Player choose to stand.")
                        break
                    case 3:  # Split
                        self.players.append(p.split())
                        num_remaining_players += 1
                        p.add_card(self.deck.draw_card())
                        self.players[-1].add_card(self.deck.draw_card())
                        self.log(f"Player choose to split.\nPlayer's first hand: {p.get_list_of_cards()}\nPlayer's second hand: {self.players[-1].get_list_of_cards()}\n")

        self.log("")
        # Dealer's turn
        if self.dealer_turn_need():
            self.log("Dealer's turn\nDealer's hand: " + str(self.dealer.get_list_of_cards()))
            while True:
                if self.dealer.is_busted():
                    self.log(f"Dealer busted.")
                    break
                action = self.dealer.play(self.dealer.get_known_card())
                match action:
                    case 0:  # Hit
                        self.dealer.add_card(self.deck.draw_card())
                        self.log(f"Dealer hits.\nDealer's hand after hit: {self.dealer.get_list_of_cards()}\n")
                    case 2:  # Stand
                        self.log(f"Dealer stands.")
                        break
        self.log("")

        self.log(f"Game ended.\nDealer's hand: {self.dealer.get_list_of_cards()}\n")
        for i, p in enumerate(self.players):
            self.log(f'Player {i}\'s hand: {p.get_list_of_cards()}')
        self.log("")

        return self.check_winners()

    def log(self, message: str):
        if self.verbose:
            print(message)

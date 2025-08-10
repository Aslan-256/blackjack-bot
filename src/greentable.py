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
        if self.verbose:
            print("Starting a new game...")
            print()

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
        if self.verbose:
            print(f"Dealer's known card: {self.dealer.get_known_card().get_value()}")
            print(f"Player's hand: {self.players[0].get_list_of_cards()}")
            print()

        # Player's turn, possible splitted
        if self.verbose:
            print("Player's turn:")
            print(f"Player's hand: {self.players[0].get_list_of_cards()}")
        num_remaining_players = len(self.players) 
        while num_remaining_players > 0:
            p = self.players[-1]
            num_remaining_players -= 1
            while True:
                if p.is_busted():
                    if self.verbose:
                        print(f"Player busted.")
                    break
                action = p.play(self.dealer.get_known_card())
                match action:
                    case 0: # Hit
                        p.add_card(self.deck.draw_card())
                        if self.verbose:
                            print(f"Player choose to hit.")
                            print(f"Player's hand after hit: {p.get_list_of_cards()}")
                    case 1: # Double Down
                        p.add_card(self.deck.draw_card())
                        if self.verbose:
                            print(f"Player choose to double down.")
                            print(f"Player's hand after double down: {p.get_list_of_cards()}")
                        break
                    case 2: # Stand
                        if self.verbose:
                            print(f"Player choose to stand.")
                        break
                    case 3: # Split
                        self.players.append(p.split())
                        num_remaining_players += 1
                        p.add_card(self.deck.draw_card())
                        self.players[-1].add_card(self.deck.draw_card())
                        if self.verbose:
                            print(f"Player choose to split.")
                            print(f"Player's first hand: {p.get_list_of_cards()}")
                            print(f"Player's second hand: {self.players[-1].get_list_of_cards()}")
                
        if self.verbose:
            print()

        # Dealer's turn
        if self.dealer_turn_need():
            if self.verbose:
                print("Dealer's turn:")  
                print(f"Dealer's hand: {self.dealer.get_list_of_cards()}")  
            while True:
                if self.dealer.is_busted():
                    if self.verbose:
                        print(f"Dealer busted.")
                    break
                action = self.dealer.play(self.dealer.get_known_card())
                match action:
                    case 0: # Hit
                        self.dealer.add_card(self.deck.draw_card())
                        if self.verbose:
                            print(f"Dealer hits.")
                            print(f"Dealer's hand after hit: {self.dealer.get_list_of_cards()}")
                    case 2: # Stand
                        if self.verbose:
                            print(f"Dealer stands.")
                        break            
        if self.verbose:
            print()
        
        if self.verbose:
            print("Game ended.")
            print(f"Dealer's hand: {self.dealer.get_list_of_cards()}")
            for player in self.players:
                print(f"{player._name}'s hand: {player.get_list_of_cards()}")
            print()
        
        return self.check_winners()
        

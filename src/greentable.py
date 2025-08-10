from colorama import Fore

from dealer import Dealer
from deck import Deck
from player import Player

RESET = "\x1b[0m"
BOLD = "\x1b[1m"
ITALIC = "\x1b[3m"
UNDERLINE = "\x1b[4m"
STRIKETHROUGH = "\x1b[9m"

class GreenTable:
    def __init__(self, verbose: bool = False):
        self.dealer = Dealer()
        self.players = [Player(money=1000)]
        self.deck = Deck()
        self.verbose = verbose
        self.bet = 1

        self.__results: list[list[int]] = []

    def __check_winners(self):
        results = []
        for player in self.players:
            if player.is_busted():
                player.set_money(player.get_money() - self.bet)
                results.append(-1)
            elif self.dealer.is_busted() or player.get_hand_value() > self.dealer.get_hand_value() or (player.has_blackjack() and not self.dealer.has_blackjack()):
                player.set_money(player.get_money() + self.bet)
                results.append(1)
            elif player.get_hand_value() < self.dealer.get_hand_value() or (self.dealer.has_blackjack() and not player.has_blackjack()):
                player.set_money(player.get_money() - self.bet)
                results.append(-1)
            else:
                results.append(0)
        return results

    def __dealer_turn_need(self):
        return not all(player.is_busted() for player in self.players)
    
    def set_table_bet(self, bet: int):
        self.bet = bet

    def start_game(self, n: int):
        for i in range(n):
            self.log(f"{Fore.GREEN}{BOLD}---STARTING GAME {RESET}{Fore.BLUE}{i}{Fore.GREEN}{BOLD}---{RESET}")

            # Shuffle deck if needed (if the index is at or beyond the black index)
            if self.deck.need_to_shuffle():
                self.deck.shuffle_deck()
                self.players[0].set_bet(1) # No counting when shuffling, so reset bet to 1
                self.log(f"Shuffling deck.")
            else: # If there is no shuffle needed, we can leverage the counting to choose a better bet
                true_count = self.deck.get_true_count()
                self.log(f"Count: {self.deck.get_counting()}")
                self.log(f"True count: {true_count:.2f}")
                if true_count >= 2:
                    self.players[0].set_bet(int(true_count))
                self.log(f"Current bet: {self.players[0].get_bet()}")
                
            

            # Reset players and dealer
            self.players = [self.players[0]]
            self.players[0].reset()
            self.dealer.reset()
            self.set_table_bet(self.players[0].get_bet())

            # Deal initial cards
            self.players[0].add_card(self.deck.draw_card())
            self.dealer.add_card(self.deck.draw_card())
            self.players[0].add_card(self.deck.draw_card())
            self.dealer.add_card(self.deck.draw_card())
            self.log(f"Dealer: {Fore.BLUE}{self.dealer.get_known_card().get_value()}{RESET}\nPlayer: {Fore.BLUE}{self.players[0].get_list_of_cards()}{RESET}")

            # Player's turn, possible splitted

            num_remaining_players = len(self.players)
            while num_remaining_players > 0:
                p = self.players[-1]
                self.log(f"{Fore.GREEN}{BOLD}---PLAYER TURN {RESET}{Fore.BLUE}{p.get_list_of_cards()}{Fore.GREEN}{BOLD}---{RESET}")
                num_remaining_players -= 1
                num_remaining_players += self.__turn(p)

            # Dealer's turn
            if self.__dealer_turn_need():
                self.log(f"{Fore.GREEN}{BOLD}---DEALER TURN {RESET}{Fore.BLUE}{str(self.dealer.get_list_of_cards())}{Fore.GREEN}{BOLD}---{RESET}")
                self.__turn(self.dealer)

            self.log(f"{Fore.GREEN}{BOLD}---GAME ENDED---{RESET}\nDealer: {Fore.BLUE}{self.dealer.get_list_of_cards()}{RESET}")
            for j, p in enumerate(self.players):
                self.log(f'Player {j}: {Fore.BLUE}{p.get_list_of_cards()}{RESET}')

            self.__results.append(self.__check_winners())
            self.log(f"Results: {Fore.BLUE}{self.__results[-1]}{RESET}")

    def __turn(self, p: Player) -> int:
        remaining_players = 0
        while True:
            if p.is_busted():
                self.log(f"{p.name} busted.")
                break
            action = p.play(self.dealer.get_known_card())
            match action:
                case 0:  # Hit
                    p.add_card(self.deck.draw_card())
                    self.log(f"{p.name} {BOLD}{Fore.RED}HIT{RESET}. --> {Fore.BLUE}{p.get_list_of_cards()}{RESET}")
                case 1:  # Double Down
                    self.set_table_bet(p.get_bet() * 2)
                    p.add_card(self.deck.draw_card())
                    self.log(f"{p.name} {BOLD}{Fore.RED}DOUBLE DOWN{RESET}. Bet: {p.get_bet()} --> {Fore.BLUE}{p.get_list_of_cards()}{RESET}")
                    break
                case 2:  # Stand
                    self.log(f"{p.name} {BOLD}{Fore.RED}STAND{RESET}.")
                    break
                case 3:  # Split
                    self.set_table_bet(p.get_bet() * 2) # We modify just a single player, maybe better to create a player with more thean one hand..
                    self.players.append(p.split())
                    p.add_card(self.deck.draw_card())
                    self.players[-1].add_card(self.deck.draw_card())
                    remaining_players = 1
                    self.log(f"{p.name} {BOLD}{Fore.RED}SPLIT{RESET}. Bet: {p.get_bet()}--> {Fore.BLUE}{p.get_list_of_cards()}{RESET}, {Fore.BLUE}{self.players[-1].get_list_of_cards()}{RESET}")
        return remaining_players

    def log(self, message: str):
        if self.verbose:
            print(message)

    def get_results(self):
        return self.__results.copy()
    
    def get_player_money(self):
        return [p.get_money() for p in self.players]
    

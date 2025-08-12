from colorama import Fore

from dealer import Dealer
from deck import Deck
from player import Player
from card import Card
from hand import Hand

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

        self.__results: list[list[int]] = []

    def __check_winners(self):
        results = []
        dealer_hand = self.dealer.get_hand()
        for player in self.players:
            for hand in player.hands:
                if hand.is_busted():
                    player.set_money(player.get_money() - hand.get_bet())
                    results.append(-1)
                elif dealer_hand.is_busted() or hand.get_soft_value() > dealer_hand.get_soft_value() or (player.has_blackjack(hand) and not self.dealer.has_blackjack(dealer_hand)):
                    player.set_money(player.get_money() + hand.get_bet())
                    if player.has_blackjack(hand):
                        self.log(f"{player.name} has a {BOLD}{Fore.BLUE}BLACKJACK{RESET}!")
                        player.set_money(player.get_money() + int(hand.get_bet() * 0.5))
                    results.append(1)
                elif hand.get_soft_value() < dealer_hand.get_soft_value() or (self.dealer.has_blackjack(dealer_hand) and not player.has_blackjack(hand)):
                    player.set_money(player.get_money() - hand.get_bet())
                    results.append(-1)
                else:
                    results.append(0)
        return results

    def __dealer_turn_need(self):
        for player in self.players:
            for hand in player.hands:
                if not hand.is_busted():
                    return True
        return False
    
    def start_game(self, n: int):
        for i in range(n):
            self.log(f"{Fore.GREEN}{BOLD}---STARTING GAME {i}---{RESET}")

            if self.deck.need_to_shuffle():# Shuffle deck if needed (if the index is at or beyond the black index)
                self.deck.shuffle_deck()
                self.players[0].set_basic_bet(1)  # Reset basic bet after shuffle
                true_count = 0
                self.log(f"Shuffling deck.")
            else: # If there is no shuffle needed, we can leverage the counting to choose a better bet
                true_count = self.deck.get_true_count()
                if true_count >= 2:
                    self.players[0].set_basic_bet(true_count)

            # Reset players and dealer
            self.players[0].reset()
            self.dealer.reset()

            self.log(f"Running count: {Fore.CYAN}{self.deck.get_counting()}{RESET}\n"
                    f"Deck remaining: {Fore.CYAN}{self.deck.get_deck_remaining()}{RESET}\n"
                    f"True count: {Fore.CYAN}{true_count:.2f}{RESET}\n"
                    f"Current bet: {Fore.CYAN}{self.players[0].get_basic_bet()}{RESET}")

            # Deal initial cards
            player_hand = self.players[0].get_hand()
            dealer_hand = self.dealer.get_hand()
            player_hand.add_card(self.deck.draw_card())
            dealer_hand.add_card(self.deck.draw_card())
            player_hand.add_card(self.deck.draw_card())
            dealer_hand.add_card(self.deck.draw_card())

            # Uncomment to test with specific cards
            # player_hand.add_card(Card(1))
            # dealer_hand.add_card(Card(10))
            # player_hand.add_card(Card(10))
            # dealer_hand.add_card(Card(10))

            self.log(f"Dealer: {Fore.BLUE}{self.dealer.get_known_card().get_value()}{RESET}\n"
                     f"Player: {Fore.BLUE}{player_hand.get_list_of_cards()}{RESET}")

            # Player's turn, possible splitted
            num_remaining_hands = len(self.players[0].hands)
            while num_remaining_hands > 0:
                # p = self.players[-1]
                hand = self.players[0].hands[-1]
                self.log(f"{Fore.GREEN}{BOLD}---PLAYER TURN {RESET}{Fore.BLUE}{hand.get_list_of_cards()}{Fore.GREEN}{BOLD}---{RESET}")
                num_remaining_hands -= 1
                num_remaining_hands += self.__turn(self.players[0], hand)

            # Dealer's turn
            if self.__dealer_turn_need():
                self.log(f"{Fore.GREEN}{BOLD}---DEALER TURN {RESET}{Fore.BLUE}{str(dealer_hand.get_list_of_cards())}{Fore.GREEN}{BOLD}---{RESET}")
                self.__turn(self.dealer, dealer_hand)

            self.log(f"{Fore.GREEN}{BOLD}---GAME ENDED---{RESET}\n"
                     f"Dealer: {Fore.BLUE}{dealer_hand.get_list_of_cards()}{RESET}")
            for j, hand in enumerate(self.players[0].hands):
                self.log(f'Player\'s hand {j}: {Fore.BLUE}{hand.get_list_of_cards()}{RESET}')

            self.__results.append(self.__check_winners())
            self.log(f"Results: {Fore.BLUE}{self.__results[-1]}{RESET}\n"
                     f"Player's money: {Fore.CYAN}{self.players[0].get_money()}{RESET}")

    def __turn(self, p: Player, h: Hand) -> int:
        remaining_hands = 0
        while True:
            if h.is_busted():
                self.log(f"{p.name} busted.")
                break
            if p.name == "Dealer": 
                action = p.dealer_play()
            else:
                action = p.playing_deviation(self.deck.get_true_count(), h, self.dealer.get_known_card())
            match action:
                case 0:  # Hit
                    h.add_card(self.deck.draw_card())
                    self.log(f"{p.name} {BOLD}{Fore.RED}HIT{RESET}. --> {Fore.BLUE}{h.get_list_of_cards()}{RESET}")
                case 1:  # Double Down
                    if p.is_splitted():
                        # TODO: handle double down after split in term of bet, idea: bet = [] list of at most two integers
                        pass
                    h.set_bet(h.get_bet() * 2)
                    h.add_card(self.deck.draw_card())
                    self.log(f"{p.name} {BOLD}{Fore.RED}DOUBLE DOWN{RESET}. Bet: {Fore.CYAN}{h.get_bet()}{RESET} --> {Fore.BLUE}{h.get_list_of_cards()}{RESET}")
                    break
                case 2:  # Stand
                    self.log(f"{p.name} {BOLD}{Fore.RED}STAND{RESET}.")
                    break
                case 3:  # Split
                    h.set_bet(h.get_bet() * 2)
                    p.split()
                    h.add_card(self.deck.draw_card())
                    self.players[0].hands[-1].add_card(self.deck.draw_card())
                    remaining_hands = 1
                    self.log(f"{p.name} {BOLD}{Fore.RED}SPLIT{RESET}. Bet: {Fore.CYAN}{h.get_bet()}{RESET} --> {Fore.BLUE}{h.get_list_of_cards()}{RESET}, {Fore.BLUE}{p.hands[-1].get_list_of_cards()}{RESET}")
                    self.log(f"{Fore.GREEN}{BOLD}---PLAYER TURN {RESET}{Fore.BLUE}{p.hands[-1].get_list_of_cards()}{Fore.GREEN}{BOLD}---{RESET}")
        return remaining_hands

    def log(self, message: str):
        if self.verbose:
            print(message)

    def get_results(self):
        return self.__results.copy()
    
    def get_player_money(self):
        return [p.get_money() for p in self.players]

    

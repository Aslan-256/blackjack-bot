from src.dealer import Dealer
from src.deck import Deck
from src.player import Player

class GreenTable:
    def __init__(self):
        self.dealer = Dealer()
        self.player = Player()
        self.deck = Deck()

    def start_game(self):
        self.deck.reset_deck()

        self.player.add_card(self.deck.get_card())
        self.dealer.add_card(self.deck.get_card())
        self.player.add_card(self.deck.get_card())
        self.dealer.add_card(self.deck.get_card())

        players = [self.dealer, self.player]
        done = []
        while len(players) > 0:
            p = players.pop()
            while True:
                action = p.play(self.dealer.get_known_card())
                match action:
                    case 0:
                        p.add_card(self.deck.get_card())
                    case 1:
                        p.add_card(self.deck.get_card())
                        done.append(p)
                        break
                    case 2:
                        done.append(p)
                        break
                    case 3:
                        players.append(p.split())
                        p.add_card(self.deck.get_card())
                        players[-1].add_card(self.deck.get_card())
                if p.is_busted():
                    done.append(p)
                    break

        for i, p in enumerate(done):
            print(f"{'Dealer' if i == len(done) - 1 else f'Player {i}'} ended with {p.get_hand_value()} {p.get_list_of_cards()}")

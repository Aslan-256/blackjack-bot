from dealer import Dealer
from deck import Deck
from player import Player

class GreenTable:
    def __init__(self):
        self.dealer = Dealer()
        self.player = Player()
        self.deck = Deck()

    def start_game(self, num_games: int = 1):
        self.deck.shuffle_deck()

        for i in range(num_games):
            self.player.add_card(self.deck.draw_card())
            self.dealer.add_card(self.deck.draw_card())
            self.player.add_card(self.deck.draw_card())
            self.dealer.add_card(self.deck.draw_card())

            players = [self.dealer, self.player]
            done = []
            #TODO: if all players bust dealer not has to play
            while len(players) > 0:
                p = players.pop()
                while True:
                    action = p.play(self.dealer.get_known_card())
                    match action:
                        case 0: # Hit
                            p.add_card(self.deck.draw_card())
                        case 1: # Stand
                            p.add_card(self.deck.draw_card())
                            done.append(p)
                            break
                        case 2: # Double down
                            done.append(p)
                            break
                        case 3: # Split
                            players.append(p.split())
                            p.add_card(self.deck.draw_card())
                            players[-1].add_card(self.deck.draw_card())
                    if p.is_busted():
                        done.append(p)
                        break
            # Win logic
            #TODO: if reached after split, blackjack counts as simple 21
            for i, p in enumerate(done):
                print(f"{'Dealer' if i == len(done) - 1 else f'Player {i}'} ended with {p.get_hand_value()} {p.get_list_of_cards()}")
            
            if self.deck.need_to_shuffle():
                self.deck.shuffle_deck()
    

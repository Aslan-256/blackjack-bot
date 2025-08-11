from typing import override

from card import Card
from player import Player
from hand import Hand

class Dealer(Player):
    def __init__(self):
        super().__init__(name = "Dealer")

    def get_known_card(self) -> Card:
        return self.hands[0].get_first_card() if self.hands else None

    @override
    def play(self,  player_hand: Hand, dealer_card: Card) -> int:
        if self.hands[0].has_ace() and self.hands[0].get_hard_value() > 5 and self.hands[0].get_hard_value() < 12:
            return 2
        return 0 if self.hands[0].get_hard_value() < 17 else 2

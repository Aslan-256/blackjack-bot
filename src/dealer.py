from typing import override

from card import Card
from player import Player

class Dealer(Player):
    def __init__(self):
        super().__init__(name = "Dealer")

    def reset(self):
        self._hand.clear()

    def get_known_card(self) -> Card:
        return self._hand[0]

    @override
    def play(self, dealer_card: Card, ) -> int:
        if self._has_ace() and self.get_hand_value() > 5 and self.get_hand_value() < 12:
            return 2
        return 0 if self.get_hand_value() < 17 else 2

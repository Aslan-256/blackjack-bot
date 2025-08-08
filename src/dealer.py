from typing import override

from src.card import Card
from src.player import Player

class Dealer(Player):
    def __init__(self):
        super().__init__(name = "Dealer")

    def get_known_card(self) -> Card:
        return self._hand[0]

    @override
    def play(self, dealer_card: Card, ) -> int:
        return 0 if self.get_hand_value() < 17 else 2

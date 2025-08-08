from enum import Enum

from src.card import Card

class Action(Enum):
    HIT = 0
    DOUBLE = 1
    STAND = 2
    SPLIT = 3

# 0 = hit
# 1 = double
# 2 = stand
# 3 = split

table = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 3
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 4
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 5
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 6
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 7
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 8

    [0, 0, 1, 1, 1, 1, 0, 0, 0, 0],  # 9
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],  # 10
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # 11
    [0, 0, 0, 2, 2, 2, 0, 0, 0, 0],  # 12
    [0, 2, 2, 2, 2, 2, 0, 0, 0, 0],  # 13
    [0, 2, 2, 2, 2, 2, 0, 0, 0, 0],  # 14
    [0, 2, 2, 2, 2, 2, 0, 0, 0, 0],  # 15
    [0, 2, 2, 2, 2, 2, 0, 0, 0, 0],  # 16

    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],  # 17
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],  # 18
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],  # 19
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],  # 20
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2]  # 21
]
ace_table = [
    [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],  # A,2
    [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],  # A,3
    [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],  # A,4
    [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],  # A,5
    [0, 0, 1, 1, 1, 1, 0, 0, 0, 0],  # A,6
    [0, 2, 1, 1, 1, 1, 2, 2, 0, 0],  # A,7
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],  # A,8
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2]  # A,9
]
split_table = [
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],  # A,A
    [0, 3, 3, 3, 3, 3, 3, 0, 0, 0],  # 2,2
    [0, 3, 3, 3, 3, 3, 3, 0, 0, 0],  # 3,3
    [0, 0, 0, 0, 3, 3, 0, 0, 0, 0],  # 4,4
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # 5,5
    [0, 3, 3, 3, 3, 3, 0, 0, 0, 0],  # 6,6
    [0, 3, 3, 3, 3, 3, 3, 0, 0, 0],  # 7,7
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],  # 8,8
    [2, 3, 3, 3, 3, 3, 2, 3, 3, 2],  # 9,9
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2]  # 10,10
]
no_split_table = [
    table[9],
    table[1],
    table[3],
    table[5],
    split_table[4],
    table[9],
    table[11],
    table[13],
    table[15],
    split_table[9]
]

class Player:
    def __init__(self, splitted: bool = False, name = "Player"):
        self._hand: list[Card] = []
        self.__splitted = splitted
        self._name = name

    def get_hand_value(self):
        return sum(card.get_value() for card in self._hand)

    def get_list_of_cards(self):
        return [card.get_value() for card in self._hand]

    def __same_cards(self):
        return self._hand[0].get_value() == self._hand[1].get_value()

    def __has_ace(self):
        return any(card.get_value() == 1 for card in self._hand)

    def add_card(self, card: Card):
        self._hand.append(card)
        print(f"{self._name} added card:", card.get_value())

    def play(self, dealer_card: Card, ) -> int:

        if len(self._hand) == 2 and self.__same_cards():
            if self.__splitted:
                return no_split_table[self.get_hand_value() // 2 - 1][dealer_card.get_value() - 1]
            return split_table[self.get_hand_value() // 2 - 1][dealer_card.get_value() - 1]

        if self.__has_ace():
            if self.get_hand_value() > 10:
                return table[self.get_hand_value() - 3][dealer_card.get_value() - 1]
            return ace_table[self.get_hand_value() - 3][dealer_card.get_value() - 1]

        return table[self.get_hand_value() - 3][dealer_card.get_value() - 1]

    def split(self):
        self.__splitted = True
        new_player = Player(True)
        new_player.add_card(self._hand.pop())
        return new_player

    def is_busted(self):
        return self.get_hand_value() > 21

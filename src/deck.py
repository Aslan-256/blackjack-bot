import random

from card import Card

class Deck:
    def __init__(self):
        self.__cards: list[Card] = []
        for i in range(6): # 6 decks
            for j in range(4): # 4 seeds
                for j in range(1, 11):  # Cards from 1 to 10
                    self.__cards.append(Card(j))
                for _ in range(3):  # Adding J, Q, K
                    self.__cards.append(Card(10))
        self.__idx = 0
        self.__black_idx = 0
        self.shuffle_deck()
        self.__counting = 0

    def draw_card(self) -> Card:
        out = self.__cards[self.__idx]
        self.__idx += 1

        match out.get_value():
            case 2, 3, 4, 5, 6:
                self.__counting += 1
            case 1, 10:
                self.__counting -= 1
            case _:
                pass

        return out

    def need_to_shuffle(self) -> bool:
        return self.__idx >= self.__black_idx

    def shuffle_deck(self):
        random.shuffle(self.__cards)
        self.__idx = 0
        self.__black_idx = random.randint(3 * 52, 4 * 52)

    def get_true_count(self) -> float:
        if self.__idx <= 52:
            return self.__counting / 6
        if self.__idx <= 104:
            return self.__counting / 5
        if self.__idx <= 156:
            return self.__counting / 4
        if self.__idx <= 208:
            return self.__counting / 3
        return self.__counting / 2

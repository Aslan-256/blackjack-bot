from card import Card

class Hand:
    def __init__(self, cards: list[Card] = [], bet: int = 1):
        self.__cards: list[Card] = cards
        self.__bet = bet

    def add_card(self, card: Card):
        self.__cards.append(card)

    def get_hard_value(self):
        return sum(card.get_value() for card in self.__cards)
    
    def get_first_card(self) -> Card:
        return self.__cards[0] if self.__cards else None
    
    def get_second_card(self) -> Card:
        return self.__cards[1] if len(self.__cards) > 1 else None

    def get_soft_value(self):
        value = self.get_hard_value()
        if self.has_ace() and value <= 11:
            return value + 10
        return value

    def get_list_of_cards(self):
        return [card.get_value() for card in self.__cards]
        
    def get_bet(self):
        return self.__bet
    
    def set_bet(self, bet: int):
        self.__bet = bet

    def same_cards(self):
        return self.__cards[0].get_value() == self.__cards[1].get_value()

    def has_ace(self):
        return any(card.get_value() == 1 for card in self.__cards)

    def is_busted(self):
        return self.get_hard_value() > 21
    
    def remove_last_card(self):
        if self.__cards:
            return self.__cards.pop()
        return None

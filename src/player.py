from card import Card
from hand import Hand

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
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # 11
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
    [0, 1, 1, 1, 1, 1, 2, 2, 0, 0],  # A,7
    [2, 2, 2, 2, 2, 1, 2, 2, 2, 2],  # A,8
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2]  # A,9
]
split_table = [
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],  # A,A
    [0, 3, 3, 3, 3, 3, 3, 0, 0, 0],  # 2,2
    [0, 3, 3, 3, 3, 3, 3, 0, 0, 0],  # 3,3
    [0, 0, 0, 0, 3, 3, 0, 0, 0, 0],  # 4,4
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],  # 5,5
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
    def __init__(self, splitted: bool = False, name = "Player", money = 1000):
        self.hands: list[Hand] = [Hand()]
        self.__splitted = splitted
        self.name = name
        self.__money = money
        self.__basic_bet = 1

    def reset(self):
        self.hands: list[Hand] = [Hand([], self.__basic_bet)]
        self.__splitted = False

    def get_hand(self) -> Hand:
        return self.hands[0] if self.hands else None

    def get_money(self):
        return self.__money
    
    def get_basic_bet(self) -> int:
        return self.__basic_bet
    
    def set_money(self, money: int):
        self.__money = money
    
    def set_basic_bet(self, bet: int):
        self.__basic_bet = bet

    def play(self, player_hand: Hand, dealer_card: Card) -> int:
        action = 0
        if len(player_hand.get_list_of_cards()) == 2 and player_hand.same_cards():
            if self.__splitted:
                action = no_split_table[player_hand.get_hard_value() // 2 - 1][dealer_card.get_value() - 1]
            else:
                action = split_table[player_hand.get_hard_value() // 2 - 1][dealer_card.get_value() - 1]
        elif player_hand.has_ace():
            if player_hand.get_hard_value() == 11:
                action = 2 # stand
            elif player_hand.get_hard_value() > 10:
                action = table[player_hand.get_hard_value() - 3][dealer_card.get_value() - 1]
            else:
                action = ace_table[player_hand.get_hard_value() - 3][dealer_card.get_value() - 1]
                # avoid double down if player has more than 2 cards
                if action == 1 and len(player_hand.get_list_of_cards()) > 2:
                    if player_hand.get_hard_value() == 8 or player_hand.get_hard_value() == 9:
                        action = 2 # stand
                    else:
                        action = 0 # hit
        else:
            action = table[player_hand.get_hard_value() - 3][dealer_card.get_value() - 1]
            # avoid double down if player has more than 2 cards
            if action == 1 and len(player_hand.get_list_of_cards()) > 2:
                action = 0 # hit

        return action

    def split(self):
        self.__splitted = True
        bet = self.hands[0].get_bet()
        first_hand = Hand([self.hands[0].get_first_card()], bet)
        second_hand = Hand([self.hands[0].get_second_card()], bet)
        self.hands = [first_hand, second_hand]
        
    def has_blackjack(self, hand: Hand) -> bool:
        return 1 in hand.get_list_of_cards() and 10 in hand.get_list_of_cards() and len(hand.get_list_of_cards()) == 2 and not self.__splitted
    
    def is_splitted(self):
        return self.__splitted
    
    def playing_deviation(self, true_count: float, player_hand: Hand, dealer_card: Card) -> int:
        player_cards = player_hand.get_list_of_cards()
        dealer_card_value = dealer_card.get_value()
        # split table
        if len(player_cards)==2 and player_hand.same_cards() and Card(10) in player_cards and not self.__splitted:
            if (dealer_card_value == 4 and true_count >= 6) or \
                (dealer_card_value == 5 and true_count >= 5) or \
                (dealer_card_value == 6 and true_count >= 4):
                return 3 # split
        # ace table
        elif player_hand.has_ace() and player_hand.get_hard_value() <= 10:
            if player_hand.get_hard_value() == 9:
                if (dealer_card_value == 4 and true_count >= 3) or \
                    (dealer_card_value == 5 and true_count >= 1):
                    return 1 # double down
                if dealer_card_value == 6 and true_count <= 0:
                    return 2 # stand
            if player_hand.get_hard_value() == 7:
                if dealer_card_value==2 and true_count >= 1:
                    return 1 # double down
        # normal table
        else:
            if player_hand.get_hard_value() == 16:
                if (dealer_card_value == 10 and true_count >= 0) or \
                    (dealer_card_value == 9 and true_count >= 4) or \
                    (dealer_card_value == 1 and true_count >= 3):
                    return 2 # stand
            if player_hand.get_hard_value() == 15:
                if (dealer_card_value == 10 and true_count >= 4) or \
                    (dealer_card_value == 1 and true_count >= 5):
                    return 2 # stand
            if player_hand.get_hard_value() == 13 and dealer_card_value == 2 and true_count <= -1:
                return 0 # hit
            if player_hand.get_hard_value() == 12:
                if (dealer_card_value == 2 and true_count >= 3) or \
                    (dealer_card_value == 3 and true_count >= 2):
                    return 2 # stand
                if dealer_card_value == 4 and true_count <= 0:
                    return 0 # hit
            if player_hand.get_hard_value() == 10:
                if (dealer_card_value == 10 and true_count >= 4) or \
                    (dealer_card_value == 1 and true_count >= 3):
                    return 1 # double down
            if player_hand.get_hard_value() == 9:
                if (dealer_card_value == 2 and true_count >= 1) or \
                    (dealer_card_value == 7 and true_count >= 3):
                    return 1 # double down
            if player_hand.get_hard_value() == 8:
                if dealer_card_value == 6 and true_count >= 2:
                    return 1 # double down
        return self.play(player_hand, dealer_card) 
    
    def test_table(self):
        # pritn for all pairs of cards the table row
        for i in range(1, 11):
            for j in range(1, 11):
                print(f"{i}, {j}: ", end='')
                for k in range(1, 11):
                    dealer_card = Card(k)
                    self._hand = [Card(i), Card(j)]
                    print(f"{self.play(dealer_card)}", end=' ')
                print()

'''
# simple test to check the table correctness

test_player = Player()
test_player.test_table()

test_player = Player(splitted=True)
test_player.test_table()
'''
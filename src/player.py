from card import Card
from hand import Hand

# 0 = hit
# 1 = double
# 2 = stand
# 3 = split

Hi = 0 # hit
D = 1 # double down
St = 2 # stand
Sp = 3 # split
Dh = 4 # double or hit
Ds = 5 # double or stand

table = [
    [Hi, Hi, Hi, Hi, Hi, Hi, Hi, Hi, Hi, Hi],  # 3
    [Hi, Hi, Hi, Hi, Hi, Hi, Hi, Hi, Hi, Hi],  # 4
    [Hi, Hi, Hi, Hi, Hi, Hi, Hi, Hi, Hi, Hi],  # 5
    [Hi, Hi, Hi, Hi, Hi, Hi, Hi, Hi, Hi, Hi],  # 6
    [Hi, Hi, Hi, Hi, Hi, Hi, Hi, Hi, Hi, Hi],  # 7
    [Hi, Hi, Hi, Hi, Hi, Hi, Hi, Hi, Hi, Hi],  # 8

    [Hi, Hi, Dh, Dh, Dh, Dh, Hi, Hi, Hi, Hi],  # 9
    [Hi, Dh, Dh, Dh, Dh, Dh, Dh, Dh, Dh, Hi],  # 10
    [Dh, Dh, Dh, Dh, Dh, Dh, Dh, Dh, Dh, Dh],  # 11
    [Hi, Hi, Hi, St, St, St, Hi, Hi, Hi, Hi],  # 12
    [Hi, St, St, St, St, St, Hi, Hi, Hi, Hi],  # 13
    [Hi, St, St, St, St, St, Hi, Hi, Hi, Hi],  # 14
    [Hi, St, St, St, St, St, Hi, Hi, Hi, Hi],  # 15
    [Hi, St, St, St, St, St, Hi, Hi, Hi, Hi],  # 16

    [St, St, St, St, St, St, St, St, St, St],  # 17
    [St, St, St, St, St, St, St, St, St, St],  # 18
    [St, St, St, St, St, St, St, St, St, St],  # 19
    [St, St, St, St, St, St, St, St, St, St],  # 2Hi
    [St, St, St, St, St, St, St, St, St, St]  # 21
]
ace_table = [
    [Hi, Hi, Hi, Hi, Dh, Dh, Hi, Hi, Hi, Hi],  # A,2
    [Hi, Hi, Hi, Hi, Dh, Dh, Hi, Hi, Hi, Hi],  # A,3
    [Hi, Hi, Hi, Dh, Dh, Dh, Hi, Hi, Hi, Hi],  # A,4
    [Hi, Hi, Hi, Dh, Dh, Dh, Hi, Hi, Hi, Hi],  # A,5
    [Hi, Hi, Dh, Dh, Dh, Dh, Hi, Hi, Hi, Hi],  # A,6
    [Hi, Ds, Ds, Ds, Ds, Ds, St, St, Hi, Hi],  # A,7
    [St, St, St, St, St, Ds, St, St, St, St],  # A,8
    [St, St, St, St, St, St, St, St, St, St]  # A,9
]
split_table = [
    [Sp, Sp, Sp, Sp, Sp, Sp, Sp, Sp, Sp, Sp],  # A,A
    [Hi, Sp, Sp, Sp, Sp, Sp, Sp, Hi, Hi, Hi],  # 2,2
    [Hi, Sp, Sp, Sp, Sp, Sp, Sp, Hi, Hi, Hi],  # 3,3
    [Hi, Hi, Hi, Hi, Sp, Sp, Hi, Hi, Hi, Hi],  # 4,4
    [Hi, Dh, Dh, Dh, Dh, Dh, Dh, Dh, Dh, Hi],  # 5,5
    [Hi, Sp, Sp, Sp, Sp, Sp, Hi, Hi, Hi, Hi],  # 6,6
    [Hi, Sp, Sp, Sp, Sp, Sp, Sp, Hi, Hi, Hi],  # 7,7
    [Sp, Sp, Sp, Sp, Sp, Sp, Sp, Sp, Sp, Sp],  # 8,8
    [St, Sp, Sp, Sp, Sp, Sp, St, Sp, Sp, St],  # 9,9
    [St, St, St, St, St, St, St, St, St, St]  # 10,10
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
        else:
            action = table[player_hand.get_hard_value() - 3][dealer_card.get_value() - 1]

        # avoid double down if player has more than 2 cards
        if len(player_hand.get_list_of_cards()) > 2:
            if action == Dh:
                action = Hi
            elif action == Ds:
                action = St
        else:
            if action in (Dh, Ds):
                action = D
        
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
        action = -1
        player_cards = player_hand.get_list_of_cards()
        dealer_card_value = dealer_card.get_value()
        # split table
        if len(player_cards)==2 and player_hand.same_cards() and Card(10) in player_cards and not self.__splitted:
            if (dealer_card_value == 4 and true_count >= 6) or \
                (dealer_card_value == 5 and true_count >= 5) or \
                (dealer_card_value == 6 and true_count >= 4):
                action = Sp 
        # ace table
        elif player_hand.has_ace() and player_hand.get_hard_value() <= 10:
            if player_hand.get_hard_value() == 9:
                if (dealer_card_value == 4 and true_count >= 3) or \
                    (dealer_card_value == 5 and true_count >= 1):
                    action = Ds
                elif dealer_card_value == 6 and true_count <= 0:
                    action = St
            elif player_hand.get_hard_value() == 7:
                if dealer_card_value==2 and true_count >= 1:
                    action = Dh
        # normal table
        else:
            if player_hand.get_hard_value() == 16:
                if (dealer_card_value == 10 and true_count >= 0) or \
                    (dealer_card_value == 9 and true_count >= 4) or \
                    (dealer_card_value == 1 and true_count >= 3):
                    action = St
            elif player_hand.get_hard_value() == 15:
                if (dealer_card_value == 10 and true_count >= 4) or \
                    (dealer_card_value == 1 and true_count >= 5):
                    action = St
            elif player_hand.get_hard_value() == 13 and dealer_card_value == 2 and true_count <= -1:
                action = Hi
            elif player_hand.get_hard_value() == 12:
                if (dealer_card_value == 2 and true_count >= 3) or \
                    (dealer_card_value == 3 and true_count >= 2):
                    action = St
                elif dealer_card_value == 4 and true_count <= 0:
                    action = Hi
            elif player_hand.get_hard_value() == 10:
                if (dealer_card_value == 10 and true_count >= 4) or \
                    (dealer_card_value == 1 and true_count >= 3):
                    action = Dh
            elif player_hand.get_hard_value() == 9:
                if (dealer_card_value == 2 and true_count >= 1) or \
                    (dealer_card_value == 7 and true_count >= 3):
                    action = Dh
            elif player_hand.get_hard_value() == 8:
                if dealer_card_value == 6 and true_count >= 2:
                    action = Dh
        if action == -1:
            action = self.play(player_hand, dealer_card) 

        # avoid double down if player has more than 2 cards
        if len(player_hand.get_list_of_cards()) > 2:
            if action == Dh:
                action = Hi
            elif action == Ds:
                action = St
        else:
            if action in (Dh, Ds):
                action = D

        return action
    
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
# TODO:
# - implement bust stop, avoiding dealers turn in case of player busting
# - understand why I'm loosing money

# -------------------------------------------------------------------------------
# --------------------------------GLOBAL VARIABLES-------------------------------
# -------------------------------------------------------------------------------
import random

# VERSIONS
verbose = False
counting = True

# PARAMETERS
num_games = 1000000

# INITIALIZATION
counting_value = 0
true_counting_value = 0
deck_idx = 0
final = False
black_card = 0
player_money = 1000000
chip = player_money // 1000  # 1000 chips of 1 unit each
bet = chip  # Initial bet is 1 chip
split_bet = [bet, bet]

# --------------------------------------------------------------------------------
# --------------------------------TABLE OF CHOICES--------------------------------
# --------------------------------------------------------------------------------
god_table = [None] * 37

# choices
h = "Hit"  # hit
d = "DobleDown"  # double down
s = "Stand"  # stand
p = "Split"  # split
## GOD TABLE ##
# EASY 1
god_table[0] = [h] * 10  # 3
god_table[1] = [h] * 10  # 4
god_table[2] = [h] * 10  # 5
god_table[3] = [h] * 10  # 6
god_table[4] = [h] * 10  # 7
god_table[5] = [h] * 10  # 8
# BASIC
god_table[6] = [h] * 2 + [d] * 4 + [h] * 4  # 9
god_table[7] = [h] + [d] * 8 + [h]  # 10
god_table[8] = [h] + [d] * 9  # 11
god_table[9] = [h] * 3 + [s] * 3 + [h] * 4  # 12
god_table[10] = [h] + [s] * 5 + [h] * 4  # 13
god_table[11] = [h] + [s] * 5 + [h] * 4  # 14
god_table[12] = [h] + [s] * 5 + [h] * 4  # 15
god_table[13] = [h] + [s] * 5 + [h] * 4  # 16
# EASY 2
god_table[14] = [s] * 10  # 17
god_table[15] = [s] * 10  # 18
god_table[16] = [s] * 10  # 19
god_table[17] = [s] * 10  # 20
god_table[18] = [s] * 10  # 21, BLACKJACK
# ACES
god_table[19] = [h] * 4 + [d] * 2 + [h] * 4  # A,2 (3)
god_table[20] = [h] * 4 + [d] * 2 + [h] * 4  # A,3 (4)
god_table[21] = [h] * 3 + [d] * 3 + [h] * 4  # A,4 (5)
god_table[22] = [h] * 3 + [d] * 3 + [h] * 4  # A,5 (6)
god_table[23] = [h] * 2 + [d] * 4 + [h] * 4  # A,6 (7)
god_table[24] = [h] + [s] + [d] * 4 + [s] * 2 + [h] * 2  # A,7 (8)
god_table[25] = [s] * 10  # A,8 (9)
god_table[26] = [s] * 10  # A,9 (10)
# SAME
god_table[27] = [p] * 10  # A,A   (2)  #SPLIT
god_table[28] = [h] + [p] * 6 + [h] * 3  # 2,2   (4)  #SPLIT
god_table[29] = [h] + [p] * 6 + [h] * 3  # 3,3   (6)  #SPLIT
god_table[30] = [h] * 4 + [p] * 2 + [h] * 4  # 4,4   (8)  #SPLIT
god_table[31] = [h] + [d] * 8 + [h]  # 5,5   (10)
god_table[32] = [h] + [p] * 5 + [h] * 4  # 6,6   (12) #SPLIT
god_table[33] = [h] + [p] * 6 + [h] * 3  # 7,7   (14) #SPLIT
god_table[34] = [p] * 10  # 8,8   (16) #SPLIT
god_table[35] = [s] + [p] * 5 + [s] + [p] * 2 + [s]  # 9,9   (18) #SPLIT
god_table[36] = [s] * 10  # 10,10 (20)

## NO SPLIT TABLE
# first 26 rows are equal to god_table ones
split_table = god_table.copy()
# let's remove split choices substituting them with the row corresponding to the normal value
split_table[27] = god_table[9]  # A,A   (2)  #NO SPLIT -> look at 12 (there is no 2-row) -> index 9
split_table[28] = god_table[1]  # 2,2   (4)  #NO SPLIT -> look at 4 -> index 1
split_table[29] = god_table[3]  # 3,3   (6)  #NO SPLIT -> look at 6 -> index 3
split_table[30] = god_table[5]  # 4,4   (8)  #NO SPLIT -> look at 8 -> index 5
split_table[31] = god_table[31]  # 5,5   (10)
split_table[32] = god_table[9]  # 6,6   (12) #NO SPLIT -> look at 12 -> index 9
split_table[33] = god_table[11]  # 7,7   (14) #NO SPLIT -> look at 14 -> index 11
split_table[34] = god_table[13]  # 8,8   (16) #NO SPLIT -> look at 16 -> index 13
split_table[35] = god_table[15]  # 9,9   (18) #NO SPLIT -> look at 18 -> index 15
split_table[36] = [s] * 10  # 10,10 (20)

def table_choice(player_value, dealer_card, ace_flag = False, same_flag = False, splitted = False):
    # let's assign the table
    if splitted:
        table = split_table
    else:
        table = god_table

    # if there is an ace, we pass values 3-10, with ace_flag=True
    # if there are same, we pass values 2-20, with same_flag=True
    if player_value == 21:  # Blackjack
        return "Stay"
    elif ace_flag:  # we are interested in rows 19-26
        return table[19 + player_value - 3][dealer_card - 1]
    elif same_flag:  # we are interested in rows 27-36
        assert player_value % 2 == 0, "Player value must be even for same."
        return table[27 + player_value // 2 - 1][dealer_card - 1]
    else:  # we are interested in rows 0-18
        return table[player_value - 3][dealer_card - 1]

# -------------------------------------------------------------------------------
# ------------------------------------COUNTING-----------------------------------
# -------------------------------------------------------------------------------

counting_dictionary = {
    2: 1, 3: 1, 4: 1, 5: 1, 6: 1,
    7: 0, 8: 0, 9: 0,
    10: -1, 1: -1
}

def counting_to_bet_percentage(true_counting_value):
    if true_counting_value <= 1:
        return 1
    else:
        return true_counting_value

def count_card(card):
    global counting_value
    counting_value += counting_dictionary[card]

def true_counting():
    global true_counting_value
    if deck_idx < 52:
        true_counting_value = counting_value / 6
    elif deck_idx < 104:
        true_counting_value = counting_value / 5
    elif deck_idx < 156:
        true_counting_value = counting_value / 4
    elif deck_idx < 208:
        true_counting_value = counting_value / 3
    else:
        true_counting_value = counting_value / 2

# ---------------------------------------------------------------------------
# --------------------------------DECK CODING--------------------------------
# ---------------------------------------------------------------------------

# comment: seeds are not used in this game, but we can keep them for future reference
# seeds_string = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
# seeds_dictionary = {"Hearts": 1, "Diamonds": 2, "Clubs": 3, "Spades": 4}
values_string = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
values_dictionary = { "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "Jack": 10, "Queen": 10, "King": 10, "Ace": 1 }
# deck_string = [(values_string[i],seeds_string[j]) for i in range(len(values_string)) for j in range(len(seeds_string))]
# deck_pairs = [(values_dictionary[values_string[i]],seeds_dictionary[seeds_string[j]]) for i in range(len(values_string)) for j in range(len(seeds_string))]*6
deck_pairs_no_seeds = [values_dictionary[value] for value in values_string] * 4 * 6

def shuffle_deck(deck):
    random.shuffle(deck)
    return deck

# ---------------------------------------------------------------------------
# ---------------------------------GAME DEMO---------------------------------
# ---------------------------------------------------------------------------
def flag_check_on_2_cards(player_card):
    ace_flag = False
    same_flag = False
    player_value = sum(player_card)
    if player_card[0] == player_card[1]:  # A,A-10,10
        same_flag = True
    elif 1 in player_card and player_value != 11:  # A,2-A,9
        ace_flag = True
    return ace_flag, same_flag

def play_game(deck):
    global deck_idx
    global final
    global counting_value
    global true_counting_value
    global bet
    global split_bet
    # print(initial_deck)
    splitted = False
    dealer_card = []
    player_card = []
    actual_card = deck[deck_idx]
    # first player's card
    player_card.append(actual_card)
    count_card(actual_card)
    true_counting()
    deck_idx += 1
    if deck_idx == black_card:
        final = True
        if verbose:
            print("Black card founded, last game before shuffle.")
    # first dealer's card
    actual_card = deck[deck_idx]
    dealer_card.append(actual_card)
    count_card(actual_card)
    true_counting()
    deck_idx += 1
    if deck_idx == black_card:
        final = True
        if verbose:
            print("Black card founded, last game before shuffle.")
    if verbose:
        print("dealer's first card:", dealer_card[0])
    # second player's card
    actual_card = deck[deck_idx]
    player_card.append(actual_card)
    count_card(actual_card)
    true_counting()
    deck_idx += 1
    if deck_idx == black_card:
        final = True
        if verbose:
            print("Black card founded, last game before shuffle.")
    if verbose:
        print("player's cards:", player_card)

    # second dealer's card
    actual_card = deck[deck_idx]
    dealer_card.append(actual_card)
    count_card(actual_card)
    true_counting()
    deck_idx += 1
    if deck_idx == black_card:
        final = True
        if verbose:
            print("Black card founded, last game before shuffle.")
    # print("hidden card:", second_dealer)

    # let's active the flags and spot 21
    player_value = sum(player_card)
    ace_flag, same_flag = flag_check_on_2_cards(player_card)
    if 1 in player_card and player_value == 11:
        player_value = 21

    choice = table_choice(player_value, dealer_card[0], ace_flag, same_flag, splitted)
    if verbose:
        print("first choice:", choice)

    # ACTIONS
    # - Hit: draw another card
    # - Double Down: double the bet and draw one more card
    # - Stand: keep the current hand and end the turn
    # - Split: split the cards into two hands if they are of the same value

    # Player's turn
    if verbose:
        print("Player's turn:")
    while choice != "Stand":
        assert choice in ["Hit", "DobleDown", "Split"]
        if choice == "Hit":
            actual_card = deck[deck_idx]
            player_card.append(actual_card)  # Simulating drawing a new card
            count_card(actual_card)
            true_counting()
            deck_idx += 1
            if deck_idx == black_card:
                final = True
                if verbose:
                    print("Black card founded, last game before shuffle.")
            if verbose:
                print("New card drawn:", player_card[-1])
            player_value = sum(player_card)
            if verbose:
                print("New player value:", player_value)
            if player_value > 21:
                if verbose:
                    print("Player busts!")
                break
        elif choice == "DobleDown":
            bet *= 2
            if verbose:
                print(f"Betting {bet} after double down")
            actual_card = deck[deck_idx]
            player_card.append(actual_card)  # Simulating drawing a new card
            count_card(actual_card)
            true_counting()
            deck_idx += 1
            if deck_idx == black_card:
                final = True
                if verbose:
                    print("Black card founded, last game before shuffle.")
            if verbose:
                print("New card drawn:", player_card[-1])
            player_value = sum(player_card)
            if verbose:
                print("New player value after double down:", player_value)
            if verbose and player_value > 21:
                print("Player busts after double down!")
            break
        elif choice == "Split":
            splitted = True
            split_bet = [bet, bet]
            if verbose:
                print(f"Betting another {bet} after a split")
            hand = [[player_card[0]], [player_card[1]]]
            # second card on hand[1]
            actual_card = deck[deck_idx]
            hand[0].append(actual_card)
            count_card(actual_card)
            true_counting()
            deck_idx += 1
            if deck_idx == black_card:
                final = True
                if verbose:
                    print("Black card founded, last game before shuffle.")
            # second card on hand[2]
            actual_card = deck[deck_idx]
            hand[1].append(actual_card)
            count_card(actual_card)
            true_counting()
            deck_idx += 1
            if deck_idx == black_card:
                final = True
                if verbose:
                    print("Black card founded, last game before shuffle.")
            if verbose:
                print("Split hands created:")
                print("Hand 1:", hand[0])
                print("Hand 2:", hand[1])
            for hand_idx in range(2):
                # let's active the flags and spot 21
                player_value = sum(hand[hand_idx])
                ace_flag, same_flag = flag_check_on_2_cards(hand[hand_idx])
                if 1 in hand[hand_idx] and player_value == 11:
                    player_value = 21

                choice = table_choice(player_value, dealer_card[0], ace_flag, same_flag, splitted)
                if verbose:
                    print(f"first choice for hand {hand_idx}:", choice)

                while choice != "Stand":
                    assert choice != "Split"
                    if choice == "Hit":
                        actual_card = deck[deck_idx]
                        hand[hand_idx].append(actual_card)  # Simulating drawing a new card
                        count_card(actual_card)
                        true_counting()
                        deck_idx += 1
                        if deck_idx == black_card:
                            final = True
                            if verbose:
                                print("Black card founded, last game before shuffle.")
                        if verbose:
                            print("New card drawn:", actual_card)
                        player_value = sum(hand[hand_idx])
                        if verbose:
                            print("New player value:", player_value)
                        if player_value > 21:
                            if verbose:
                                print("Player busts!")
                            break
                    elif choice == "DobleDown":
                        split_bet[hand_idx] *= 2
                        actual_card = deck[deck_idx]
                        hand[hand_idx].append(actual_card)  # Simulating drawing a new card
                        count_card(actual_card)
                        true_counting()
                        deck_idx += 1
                        if deck_idx == black_card:
                            final = True
                            if verbose:
                                print("Black card founded, last game before shuffle.")
                        if verbose:
                            print("New card drawn:", hand[hand_idx][-1])
                        player_value = sum(hand[hand_idx])
                        if verbose:
                            print("New player value after double down:", player_value)
                        if verbose and player_value > 21:
                            print("Player busts after double down!")
                        break

                    # Re-evaluate the choice after the action
                    ace_flag = False
                    same_flag = False
                    if 1 in hand[hand_idx] and player_value - 1 <= 10:  # we're checking if the sum of all the cards but the ace is less than or equal to 10, so we can count the ace as 11
                        if player_value == 11:
                            player_value = 21  # Blackjack
                        else:
                            ace_flag = True

                    choice = table_choice(player_value, dealer_card[0], ace_flag, same_flag, splitted)
                    if verbose:
                        print("Next choice:", choice)

                if 1 in hand[hand_idx] and player_value - 1 <= 10:  # we're checking if the sum of all the cards but the ace is less than or equal to 10, so we can count the ace as 11
                    player_value = player_value + 10
                if verbose:
                    print(f"Final player value for hand {hand_idx}:", player_value)
                    print()

            break

        # Re-evaluate the choice after the action
        ace_flag = False
        same_flag = False
        if 1 in player_card and player_value - 1 <= 10:  # we're checking if the sum of all the cards but the ace is less than or equal to 10, so we can count the ace as 11
            if player_value == 11:
                player_value = 21  # Blackjack
            else:
                ace_flag = True

        choice = table_choice(player_value, dealer_card[0], ace_flag, same_flag, splitted)
        if verbose:
            print("Next choice:", choice)

    if 1 in player_card and player_value - 1 <= 10:  # we're checking if the sum of all the cards but the ace is less than or equal to 10, so we can count the ace as 11
        player_value = player_value + 10
    if verbose:
        print("Final player value:", player_value)
        print()

    # Dealer's turn
    if verbose:
        print("Dealer's turn:")
        print("Dealer's cards:", dealer_card)
    dealer_value = sum(dealer_card)
    if 1 in dealer_card and dealer_value - 1 <= 10:  # we're checking if the sum of all the cards but the ace is less than or equal to 10, so we can count the ace as 11
        dealer_value = dealer_value + 10
    while dealer_value < 17:
        actual_card = deck[deck_idx]
        dealer_card.append(actual_card)  # Simulating drawing a new card
        count_card(actual_card)
        true_counting()
        deck_idx += 1
        if deck_idx == black_card:
            final = True
            if verbose:
                print("Black card founded, last game before shuffle.")
        if verbose:
            print("New dealer card drawn:", dealer_card[-1])
        dealer_value = sum(dealer_card)
        if verbose:
            print("New dealer value:", dealer_value)
    if dealer_value > 21:
        if verbose:
            print("Dealer busts!")
    else:
        if verbose:
            print("Final dealer value:", dealer_value)
    if verbose:
        print()

    # Determine the winner
    result = [0, -21]  # -21 flag value to indicate that there is no split
    if not splitted:
        player_value = sum(player_card)
        # first, let's check if there are blackjacks
        blackjack = (len(player_card) == 2) and (1 in player_card) and (10 in player_card)
        dealer_blackjack = (len(dealer_card) == 2) and (1 in dealer_card) and (10 in dealer_card)
        # let's determine now the winner
        if player_value > 21:
            if verbose:
                print("Dealer wins! Player busts.")
                print()
            result[0] = -1
        elif dealer_value > 21 or player_value > dealer_value or (blackjack and not dealer_blackjack):
            if blackjack and not dealer_blackjack:
                if verbose:
                    print("Player wins with a Blackjack!")
                    print()
                result[0] = 21
            else:
                if verbose:
                    print("Player wins!")
                    print()
                result[0] = 1
        elif player_value < dealer_value or (dealer_blackjack and not blackjack):
            if verbose:
                print("Dealer wins!")
                print()
            result[0] = -1
        else:
            if verbose:
                print("It's a tie!")
                print()
            result[0] = 0
    else:
        for hand_idx in range(2):
            player_value = sum(hand[hand_idx])
            # first, let's check if there are blackjacks
            blackjack = (len(hand[hand_idx]) == 2) and (1 in hand[hand_idx]) and (10 in hand[hand_idx])
            dealer_blackjack = (len(dealer_card) == 2) and (1 in dealer_card) and (10 in dealer_card)
            # let's determine now the winner
            if player_value > 21:
                if verbose:
                    print("Dealer wins! Player busts.")
                    print()
                result[hand_idx] = -1
            elif dealer_value > 21 or player_value > dealer_value or (blackjack and not dealer_blackjack):
                if blackjack and not dealer_blackjack:
                    if verbose:
                        print("Player wins with a Blackjack!")
                        print()
                    result[hand_idx] = 21
                else:
                    if verbose:
                        print("Player wins!")
                        print()
                    result[hand_idx] = 1
            elif player_value < dealer_value or (dealer_blackjack and not blackjack):
                if verbose:
                    print("Dealer wins!")
                    print()
                result[hand_idx] = -1
            else:
                if verbose:
                    print("It's a tie!")
                    print()
                result[hand_idx] = 0
    return result

player = 0
dealer = 0
tie = 0
actual_deck = shuffle_deck(deck_pairs_no_seeds)
black_card = random.randint(3 * 52, 4 * 52)
for _ in range(num_games):  # Play the game 100 times
    if counting:
        if verbose:
            print(f"Counting value: {counting_value}")
            print(f"True counting value: {true_counting_value}")
            print()
        bet = int(counting_to_bet_percentage(true_counting_value)) * chip
        if verbose:
            if int(counting_to_bet_percentage(true_counting_value)) >= 2:
                print(f"Betting {bet}")
            else:
                print("Betting 1000")
            print()
    result = play_game(actual_deck)
    if result[-1] == -21:
        if result[0] >= 1:
            player += 1
            if counting:
                if result[0] == 21:
                    player_money += bet * 1.5
                else:
                    player_money += bet
        elif result[0] == -1:
            dealer += 1
            if counting:
                player_money -= bet
        else:
            tie += 1
    else:  # split case
        for hand_idx in range(2):
            if result[hand_idx] >= 1:
                player += 1
                if counting:
                    if result[hand_idx] == 21:
                        player_money += split_bet[hand_idx] * 1.5
                    else:
                        player_money += split_bet[hand_idx]
            elif result[hand_idx] == -1:
                dealer += 1
                if counting:
                    player_money -= split_bet[hand_idx]
            else:
                tie += 1

    if counting and verbose:
        print(f"Player's money: {player_money}")
        print()
    if final == True:
        actual_deck = shuffle_deck(deck_pairs_no_seeds)
        black_card = random.randint(3 * 52, 4 * 52)
        deck_idx = 0
        final = False
        counting_value = 0
        true_counting_value = 0

print(f"Game results after {num_games} rounds:")
print(f"Player wins: {player}, Dealer wins: {dealer}, Ties: {tie}")
print(f"Player win percentage: {player / (player + dealer) * 100:.2f}%")  # 48.72%
print(f"Player win percentage counting ties: {player / (player + dealer + tie) * 100:.2f}%")  # 44.32%
print(f"Player money: {player_money}")

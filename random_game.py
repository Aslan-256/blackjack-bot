#-------------------------------------------------------------------------------
#---------------------------------GENERAL PARAMS--------------------------------
#-------------------------------------------------------------------------------
import random

verbose = False
counting = False 
num_games = 1000000
counting_value = 0
deck_idx = 0
final = False
black_card = 0

#--------------------------------------------------------------------------------
#--------------------------------TABLE OF CHOICES--------------------------------
#--------------------------------------------------------------------------------
god_table = [None]*37
# god_table_mid_game = [None]*19
#choices
h = "Hit"       #hit
d = "DobleDown" #double down
s = "Stand"     #stand
p = "Split"     #split
#EASY 1
god_table[0] = [h]*10                               #3
god_table[1] = [h]*10                               #4
god_table[2] = [h]*10                               #5
god_table[3] = [h]*10                               #6
god_table[4] = [h]*10                               #7
god_table[5] = [h]*10                               #8
#BASIC
god_table[6] = [h]*2 + [d]*4 + [h]*4                #9
god_table[7] = [h] + [d]*8 + [h]                    #10
god_table[8] = [h] + [d]*9                          #11
god_table[9] = [h]*3 + [s]*3 + [h]*4                #12
god_table[10] = [h] + [s]*5 + [h]*4                 #13
god_table[11] = [h] + [s]*5 + [h]*4                 #14
god_table[12] = [h] + [s]*5 + [h]*4                 #15
god_table[13] = [h] + [s]*5 + [h]*4                 #16
#EASY 2
god_table[14] = [s]*10                              #17
god_table[15] = [s]*10                              #18
god_table[16] = [s]*10                              #19
god_table[17] = [s]*10                              #20
god_table[18] = [s]*10                              #21, BLACKJACK
#ACES
god_table[19] = [h]*4 + [d]*2 + [h]*4               #A,2 (3)
god_table[20] = [h]*4 + [d]*2 + [h]*4               #A,3 (4)
god_table[21] = [h]*3 + [d]*3 + [h]*4               #A,4 (5)
god_table[22] = [h]*3 + [d]*3 + [h]*4               #A,5 (6)
god_table[23] = [h]*2 + [d]*4 + [h]*4               #A,6 (7)
god_table[24] = [h] + [s] + [d]*4 + [s]*2 + [h]*2   #A,7 (8)
god_table[25] = [s]*10                              #A,8 (9)
god_table[26] = [s]*10                              #A,9 (10)
#SAME
god_table[27] = [p]*10                              #A,A   (2)
god_table[28] = [h] + [p]*6 + [h]*3                 #2,2   (4)
god_table[29] = [h] + [p]*6 + [h]*3                 #3,3   (6)
god_table[30] = [h]*4 + [p]*2 + [h]*4               #4,4   (8)
god_table[31] = [h] + [d]*8 + [h]                   #5,5   (10)
god_table[32] = [h] + [p]*5 + [h]*4                 #6,6   (12)
god_table[33] = [h] + [p]*6 + [h]*3                 #7,7   (14)
god_table[34] = [p]*10                              #8,8   (16)
god_table[35] = [s] + [p]*5 + [s] + [p]*2 + [s]     #9,9   (18)
god_table[36] = [s]*10                              #10,10 (20)

# god_table_mid_game = god_table[0:19]

player_value_dictionary = {0:"3", 1:"4", 2:"5", 3:"6", 4:"7", 5:"8", 6:"9", 7:"10", 8:"11", 9:"12", 10:"13", 11:"14", 12:"15", 13:"16", 14:"17", 15:"18", 16:"19", 17:"20", 18:"21", 19:"A,2", 20:"A,3", 21:"A,4", 22:"A,5", 23:"A,6", 24:"A,7", 25:"A,8", 26:"A,9", 27:"A,A", 28:"2,2", 29:"3,3", 30:"4,4", 31:"5,5", 32:"6,6", 33:"7,7", 34:"8,8", 35:"9,9", 36:"10,10"}
# for i in range(len(god_table)):
#     print(f"{player_value_dictionary[i]}[{i}]: {god_table[i]}")

def table_choice(player_value, dealer_card, ace_flag=False, same_flag=False):
    #if there is an ace, we pass values 3-10, with ace_flag=True
    #if there are same, we pass values 2-20, with same_flag=True
    if player_value == 21:  # Blackjack
        return god_table[player_value-3][dealer_card - 1]
    elif ace_flag: #we are interested in rows 19-26
        return god_table[19 + player_value - 3][dealer_card - 1]
    elif same_flag: #we are interested in rows 27-36
        assert player_value%2 == 0, "Player value must be even for same."
        return god_table[27 + player_value//2 - 1][dealer_card - 1]
    else: #we are interested in rows 0-18
        return god_table[player_value-3][dealer_card - 1]
    
#-------------------------------------------------------------------------------
#------------------------------------COUNTING-----------------------------------
#-------------------------------------------------------------------------------

counting_dictionary = {
    "2": 1, "3": 1, "4": 1, "5": 1, "6": 1,
    "7": 0, "8": 0, "9": 0,
    "10": -1, "1": -1
}

def count_card(card):
    global counting_value
    counting_value += counting_dictionary[card]

#---------------------------------------------------------------------------
#--------------------------------DECK CODING--------------------------------
#---------------------------------------------------------------------------

#comment: seeds are not used in this game, but we can keep them for future reference
# seeds_string = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
# seeds_dictionary = {"Hearts": 1, "Diamonds": 2, "Clubs": 3, "Spades": 4}
values_string = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
values_dictionary = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "Jack": 10, "Queen": 10, "King": 10, "Ace": 1}
# deck_string = [(values_string[i],seeds_string[j]) for i in range(len(values_string)) for j in range(len(seeds_string))]
# deck_pairs = [(values_dictionary[values_string[i]],seeds_dictionary[seeds_string[j]]) for i in range(len(values_string)) for j in range(len(seeds_string))]*6
deck_pairs_no_seeds = [values_dictionary[value] for value in values_string]*4*6

def shuffle_deck(deck):
    random.shuffle(deck)
    return deck

#---------------------------------------------------------------------------
#---------------------------------GAME DEMO---------------------------------
#---------------------------------------------------------------------------
def play_game(deck):
    global deck_idx
    global final
    global counting_value
    # print(initial_deck)
    dealer_card = []
    player_card = []
    # first player's card
    player_card.append(deck[deck_idx])
    deck_idx += 1
    if deck_idx == black_card:
        final = True
    # first dealer's card
    dealer_card.append(deck[deck_idx])
    deck_idx += 1
    if deck_idx == black_card:
        final = True
    if verbose:
        print("dealer's card:", dealer_card[0])
    # second player's card
    player_card.append(deck[2])
    if verbose:
        print("player's cards:", player_card[0], player_card[1])
    # second dealer's card
    dealer_card.append(deck[deck_idx])
    deck_idx += 1
    if deck_idx == black_card:
        final = True
    # print("hidden card:", second_dealer)
        
    #let's active the flags with the player's value
    ace_flag = False
    same_flag = False
    player_value = sum(player_card)
    if player_card[0] == player_card[1]: # A,A-10,10 
        same_flag = True
    elif 1 in player_card: # A,2-A,9
        #here we have two cases: 
        # - 21 as A,10
        # - A,2-A,9
        if player_value == 11:
            player_value = 21 # Blackjack
        else:
            ace_flag = True  

    choice = table_choice(player_value, dealer_card[0], ace_flag, same_flag)
    if verbose:
        print("first choice:", choice)

    # ACTIONS
    # - Hit: draw another card
    # - Double Down: double the bet and draw one more card
    # - Stand: keep the current hand and end the turn
    # - Split: split the cards into two hands if they are of the same value

    count = 0

    #Player's turn
    if verbose:
        print("Player's turn:")
    while choice != "Stand":
        if choice == "Hit":
            player_card.append(deck[deck_idx])  # Simulating drawing a new card
            deck_idx += 1
            if deck_idx == black_card:
                final = True
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
            player_card.append(deck[deck_idx])  # Simulating drawing a new card
            deck_idx += 1
            if deck_idx == black_card:
                final = True
            if verbose:
                print("New card drawn:", player_card[-1])
            player_value = sum(player_card)
            if verbose:
                print("New player value after double down:", player_value)
            if player_value > 21:
                if verbose:
                    print("Player busts after double down!")
                break
            
        elif choice == "Split":
            if verbose:
                print("Splitting the hand is not implemented in this demo.")
            break
        
        # Re-evaluate the choice after the action
        ace_flag = False
        same_flag = False
        if 1 in player_card and player_value-1<=10: #we're checking if the sum of all the cards but the ace is less than or equal to 10, so we can count the ace as 11
            if player_value == 11:
                player_value = 21 # Blackjack
            else:
                ace_flag = True

        choice = table_choice(player_value, dealer_card[0], ace_flag, same_flag)
        if verbose:
            print("Next choice:", choice)

    if 1 in player_card and player_value-1<=10: #we're checking if the sum of all the cards but the ace is less than or equal to 10, so we can count the ace as 11
        player_value = player_value + 10
    if verbose:
        print("Final player value:", player_value)
        print()

    # Dealer's turn
    if verbose:
        print("Dealer's turn:")
        print("Dealer's cards:", dealer_card)
    dealer_value = sum(dealer_card)
    if 1 in dealer_card and dealer_value-1<=10: #we're checking if the sum of all the cards but the ace is less than or equal to 10, so we can count the ace as 11
        dealer_value = dealer_value + 10
    while dealer_value < 17:
        dealer_card.append(deck[4+count])  # Simulating drawing a new card
        if verbose:
            print("New dealer card drawn:", dealer_card[-1])
        dealer_value = sum(dealer_card)
        if verbose:
            print("New dealer value:", dealer_value)
        count += 1  # Increment count to simulate drawing new cards
    if dealer_value > 21:
        if verbose:
            print("Dealer busts!")
    else:
        if verbose:
            print("Final dealer value:", dealer_value)
    if verbose:
        print()

    # Determine the winner
    # first, let's check if there are blackjacks
    blackjack = (len(player_card)==2) and (1 in player_card) and (10 in player_card)
    dealer_blackjack = (len(dealer_card)==2) and (1 in dealer_card) and (10 in dealer_card)
    # let's determine now the winner
    if player_value > 21:
        if verbose:
            print("Dealer wins! Player busts.")
            print()
        return -1
    elif dealer_value > 21 or player_value > dealer_value or (blackjack and not dealer_blackjack):
        if verbose:
            print("Player wins!")
            print()
        return 1
    elif player_value < dealer_value:
        if verbose:
            print("Dealer wins!")
            print()
        return -1
    else:
        if verbose:
            print("It's a tie!")
            print()
        return 0

player = 0
dealer = 0
tie = 0
actual_deck = shuffle_deck(deck_pairs_no_seeds) 
black_card = random.randint(3*52, 4*52)
for _ in range(num_games):  # Play the game 100 times
    result = play_game(actual_deck)
    if result == 1:
        player += 1
    elif result == -1:
        dealer += 1
    else:
        tie += 1 
    if final == True:
        actual_deck = shuffle_deck(deck_pairs_no_seeds) 
        black_card = random.randint(3*52, 4*52)
        deck_idx = 0
        final = False
        counting_value = 0

print(f"Game results after {num_games} rounds:")
print(f"Player wins: {player}, Dealer wins: {dealer}, Ties: {tie}")
print(f"Player win percentage: {player/(player+dealer)*100:.2f}%") #48.72%
print(f"Player win percentage counting ties: {player/(player+dealer+tie)*100:.2f}%") #44.32%
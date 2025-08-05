#--------------------------------------------------------------------------------
#--------------------------------TABLE OF CHOICES--------------------------------
#--------------------------------------------------------------------------------
god_table = [None]*37
#choices
h = "Hit"       #hit
d = "DobleDown" #double down
s = "Stay"      #stay
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
#DOUBLES
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

player_value_dictionary = {0:"3", 1:"4", 2:"5", 3:"6", 4:"7", 5:"8", 6:"9", 7:"10", 8:"11", 9:"12", 10:"13", 11:"14", 12:"15", 13:"16", 14:"17", 15:"18", 16:"19", 17:"20", 18:"21", 19:"A,2", 20:"A,3", 21:"A,4", 22:"A,5", 23:"A,6", 24:"A,7", 25:"A,8", 26:"A,9", 27:"A,A", 28:"2,2", 29:"3,3", 30:"4,4", 31:"5,5", 32:"6,6", 33:"7,7", 34:"8,8", 35:"9,9", 36:"10,10"}
# for i in range(len(god_table)):
#     print(f"{player_value_dictionary[i]}[{i}]: {god_table[i]}")

def table_choice(player_value, dealer_card, ace_flag=False, double_flag=False):
    #if there is an ace, we pass values 3-10, with ace_flag=True
    #if there are doubles, we pass values 2-20, with double_flag=True
    if player_value == 21:  # Blackjack
        return god_table[player_value-3][dealer_card - 1]
    elif ace_flag: #we are interested in rows 19-26
        return god_table[19 + player_value - 3][dealer_card - 1]
    elif double_flag: #we are interested in rows 27-36
        assert player_value%2 == 0, "Player value must be even for doubles."
        return god_table[27 + player_value//2 - 1][dealer_card - 1]
    else: #we are interested in rows 0-18
        return god_table[player_value-3][dealer_card - 1]

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
    import random
    random.shuffle(deck)
    return deck

initial_deck = shuffle_deck(deck_pairs_no_seeds)

# print(initial_deck)
first_dealer = initial_deck[1]
print("dealer's card:", first_dealer)
second_dealer = initial_deck[3]
# print("hidden card:", second_dealer)
first_player = initial_deck[0]
second_player = initial_deck[2]
print("player's cards:", first_player, second_player)
    
#let's active the flags with the player's value
ace_flag = False
double_flag = False
player_value = first_player + second_player 
if first_player == second_player: # A,A-10,10 
    double_flag = True
elif first_player == 1 or second_player == 1: # A,2-A,9
    if player_value == 11:
        player_value = 21 # Blackjack
    else:
        ace_flag = True  

print("obvious choice:", table_choice(player_value, first_dealer, ace_flag, double_flag))
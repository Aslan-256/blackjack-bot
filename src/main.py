from greentable import GreenTable

def main():
    green_table = GreenTable(verbose = False)
    wins = 0
    losses = 0
    ties = 0
    green_table.start_game(1000000)
    results = green_table.get_results()

    for result in results:
        for p in result:
            if p == 1:
                wins += 1
            elif p == -1:
                losses += 1
            else:
                ties += 1

    player_money = green_table.players[0].get_money()

    print(f"\n\nTotal Wins: {wins}, Losses: {losses}, Ties: {ties}")
    print(f"Win Rate: {wins / (wins + losses + ties) * 100:.2f}%")
    (print(f"Win rate without ties: {wins / (wins + losses) * 100:.2f}%") if (wins + losses) > 0 else "N/A")
    print(f"Player's final money: {player_money}")


if __name__ == '__main__':
    main()

# TODO:
# - playing deviation based on true count
# - handle double down after split

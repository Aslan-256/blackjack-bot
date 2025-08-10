from greentable import GreenTable

def main():
    green_table = GreenTable(verbose=True)
    wins = 0
    losses = 0
    ties = 0
    for i in range(50):
        results = green_table.start_game()
        if green_table.verbose:
            print(f"Game {i + 1} results: {results}")
            print()
        for result in results:
            if result == 1:
                wins += 1
            elif result == -1:
                losses += 1
            else:
                ties += 1
    print(f"Total Wins: {wins}, Losses: {losses}, Ties: {ties}")
    print(f"Win Rate: {wins / (wins + losses + ties) * 100:.2f}%")
    print(f"Win rate without ties: {wins / (wins + losses) * 100:.2f}%")

if __name__ == '__main__':
    main()

# TODO:
# - count
# - money bet
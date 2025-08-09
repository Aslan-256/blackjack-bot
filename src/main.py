from greentable import GreenTable

def main():
    for i in range(1000000):
        print(f"Game {i + 1}")
        green_table = GreenTable()
        green_table.start_game()

if __name__ == '__main__':
    main()

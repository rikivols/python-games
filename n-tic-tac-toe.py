"""
A simple tic tac toe game enlarged to n x n board with two players playing against
each other.

User has to choose height of the board, what pieces the first player starts with.

Then making a move. The move is made by giving a number which corresponds
to the square he wants to place piece to. Numbers goes from one (upper left
square) towards the right down square (which has value n ^ 2).

The number of pieces to achieve win is in range 3 - 5 and depends on height
of the board.
"""


def initialize_game():
    """
    Starts the game

    :return: player1: 'X' or 'O' depending on input
             player2: 'X' or 'O' opposite value of player 1
    """

    # Chooze size of the board
    while True:
        try:
            size_board = int(input("Choose size of the board (3+): "))
        except ValueError:
            print("Wrong input")
            continue
        if size_board <= 2:
            print("Too small...")
            continue
        break

    player1 = None
    # choose player
    while player1 != 'X' and player1 != 'O':
        player1 = input("Do you want to be X or O?: ").upper()

    if player1 == 'X':
        player2 = 'O'
    else:
        player2 = 'X'

    game_arr = [[0 for x in range(size_board)] for y in range(size_board)]

    return player1, player2, game_arr, size_board


def print_board(game_arr, size_board):
    """
    Prints the board.

    :param game_arr: Array of the board with moves played.

    :return: Nothing, just prints the board.
    """

    for i in range(size_board):

        v = [' ' if x == 0 else x for x in game_arr[i]]
        if i == 0:
            for j in range(size_board):
                print(f"  {j+1} ", end='')
            print()
            print("----" * len(game_arr), end='')
            print("-")
        for j in range(size_board):
            if j == 0:
                print(f"|", end='')
            print(f" {v[j]} |", end='')
            if j == size_board - 1:
                print(f" {i*size_board}", end='')

        print()
        print("----" * len(game_arr), end='')
        print("-")
    print()


def make_move(game_arr, player_to_move, move, size_board):
    """
    Updates game_arr.

    :param game_arr: Array of the board with moves played
    :param player_to_move: 'X' or 'O' depending on which player is currently on move
    :param move: move made by player (1-9)

    :return: updated game_arr
    """

    counter = 0
    for i in range(size_board):
        for j in range(size_board):
            counter += 1
            if counter == move:
                game_arr[i][j] = player_to_move
                return game_arr


def is_ended(game_arr, win_needed, size_board):
    """
    Determines if the game has winner / has ended.

    :param game_arr: Array of the board with moves played
           win_needed: How many pieces in row / column / diagonal it takes to win

    :return: True / False  game was ended / continues
    """

    n = len(game_arr)

    def player_wins(num_of_x, num_of_o, position):
        """
        Handles simple logic of who has won and prints the message

        :arg num_of_x - number of 'X' pieces in particular order
             num_of_y - number of 'Y' pieces in particular order
             position - in which position are pieces controlled aligned
                        1 - in line
                        2 - in column
                        3 - in diagonal
        """

        if num_of_x == win_needed or num_of_o == win_needed:
            win_position = ""

            if position == 1:
                win_position = "line"
            elif position == 2:
                win_position = "column"
            elif position == 3:
                win_position = "diagonal"

            print_board(game_arr, size_board)
            print()
            print(f"Won by having {win_needed} pieces in one {win_position}.")

        if num_of_x == win_needed:
            print("Player with X wins, congratulations.")
            return True

        if num_of_o == win_needed:
            print(f"Player with O wins, congratulations.")
            return True

    """
    Checks every line if we have a winner.
    """

    for v in game_arr:
        num_of_x = 0
        num_of_o = 0
        for v2 in v:
            if v2 == 'X':
                num_of_x += 1
                num_of_o = 0
            elif v2 == 'O':
                num_of_x = 0
                num_of_o += 1

            if player_wins(num_of_x, num_of_o, 1):
                return True



    """
    ------------------------------------------
    """

    """
    Checks columns if we have a winner.
    """

    for i in range(n):
        num_of_x = 0
        num_of_o = 0
        for j in range(n):
            if game_arr[j][i] == 'X':
                num_of_x += 1
                num_of_o = 0
            elif game_arr[j][i] == 'O':
                num_of_x = 0
                num_of_o += 1

            if player_wins(num_of_x, num_of_o, 2):
                return True

    """
    ------------------------------------------
    """

    """
    Checks diagonals if we have winner.
    """

    # checking from left to right
    for i in range(n+1 - win_needed):
        for j in range(n+1 - win_needed):
            num_of_x = 0
            num_of_o = 0
            for y in range(win_needed):
                if game_arr[i+y][j+y] == 'X':
                    num_of_x += 1
                    num_of_o = 0
                elif game_arr[i+y][j+y] == 'O':
                    num_of_x = 0
                    num_of_o += 1

            if player_wins(num_of_x, num_of_o, 3):
                return True

    # checking from right to left
    for i in range(win_needed, n):
        for j in range(win_needed, n):
            num_of_x = 0
            num_of_o = 0
            for y in range(win_needed):
                if game_arr[i - y][j - y] == 'X':
                    num_of_x += 1
                    num_of_o = 0
                elif game_arr[i - y][j - y] == 'O':
                    num_of_x = 0
                    num_of_o += 1

            if player_wins(num_of_x, num_of_o, 3):
                return True

    """
    ------------------------------------------
    """


def start_game_again():

    while True:
        again = input("Start again? (y/n): ").lower()
        if again == 'y' or again == 'yes' or again == 'n' or again == 'no':
            break
        else:
            print("Wrong input, expected y/n")

    if again == 'n' or again == 'no':
        print("Thanks for playing.")
        return False

    return True


while True:

    player1, player2, game_arr, size_board = initialize_game()
    moves = []  # array of made moves (check duplicates)

    """ 
    Determine what number of continuous pieces wins. 
    """
    if size_board in range(3, 5):
        win_needed = 3
    elif size_board in range(5, 9):
        win_needed = 4
    else:
        win_needed = 5

    print()

    """
    ------------------------------------------
    """

    """ 
    Handles whole playing logic with help of various functions. 
    """
    for i in range(size_board**2):

        if i % 2 == 0:
            player_piece = player1
        else:
            player_piece = player2

        print_board(game_arr, size_board)

        if i == 0:

            print(f"Having {win_needed} pieces in order wins")
            print()

        while True:
            try:
                move = int(input(f"Please make a move player with {player_piece} (add upper and side number): "))
            except ValueError:
                print("Come on, it's not even a number.")
                continue

            if move not in range(1, size_board**2 + 1):
                print("Your move has incorrect form, should be index of square")
                continue
            if move in moves:
                print("There's already piece on the square.")
                continue

            moves.append(move)
            break

        print('\n' * 100)  # clear the console
        game_arr = make_move(game_arr, player_piece, move, size_board)

        if is_ended(game_arr, win_needed, size_board):
            break
    else:
        print_board(game_arr, size_board)
        print("Looks like the game ended in draw (booring).")

    """
    ------------------------------------------
    """

    # start game again
    if not start_game_again():
        break
    print()

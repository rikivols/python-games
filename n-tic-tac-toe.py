from random import randint


class Board:

    def __init__(self, size):
        """
        :param size: Size of the board.

        position: Current position on the board.
        moves_played: Contains all moves played to ban players from overriding pieces on board.
        win_needed: How many pieces in one row / column / diagonal are needed to win the game.
        """

        self.position = [[0 for _ in range(size)] for _ in range(size)]
        self.size = size
        self.moves_played = []

        # calculate how many pieces in one row / column / diagonal are needed for win
        if size >= 9:
            self.win_needed = 5
        elif size >= 5:
            self.win_needed = 4
        else:
            self.win_needed = 3

    def make_move(self, row, col, piece):
        """
        Makes a move: updates position and saves the move played.

        :param row: Row of lastly played move.
        :param col: Column of lastly played move.
        :param piece: Which piece played the move (X or O).
        """

        self.position[row][col] = piece
        self.moves_played.append([row, col])

    def has_ended(self, row, col, piece, player_name):
        """
        Checks if we the lastly played player is a winner / if game ended.

        :param row: Row of lastly played move.
        :param col: Column of lastly played move.
        :param piece: Which piece played the move (X or O).
        :param player_name: Name of player who played the move.

        The end of game is determined by lastly placed piece. We search just for player's pieces (:param piece),
        we don't care about opponent's. We check one row, one column and two diagonals (from left to right and
        from right to left) around the lastly placed piece. The row / column / diagonals checked are win_needed - 1
        squares long to both sides of lastly placed piece (if we're checking row, and win_needed is 3, we check
        this row from a position 2 squares to the left, and we search for winning pattern (3 pieces in row) up to
        2 squares to the right from the placed piece).

        We don't need to check more, the lastly placed piece couldn't influence more squares. Then we look if the
        player obtained a winning position pattern.

        returns: If the game ended: A massage of who won and how the win was obtained.
                 If the game still continues: Nothing.
        """

        pieces_row = 0
        pieces_col = 0
        pieces_lr = 0
        pieces_rl = 0

        # i is added / subtracted from row / col to check squares around the piece.
        for i in range(-self.win_needed + 1, self.win_needed):

            """ search rows """
            if 0 <= col + i < self.size:  # Avoid overflow.
                if self.position[row][col+i] == piece:
                    pieces_row += 1
                else:
                    pieces_row = 0

                if pieces_row >= self.win_needed:
                    return ' '.join((f"{player_name} (player with {piece} pieces) won by having {self.win_needed}",
                                    "pieces in one row, congratulations."))
            """ ----------- """

            """ search columns """
            if 0 <= row + i < self.size:  # Avoid overflow.
                if self.position[row+i][col] == piece:
                    pieces_col += 1
                else:
                    pieces_col = 0

                if pieces_col >= self.win_needed:
                    return ' '.join((f"{player_name} (player with {piece} pieces) won by having {self.win_needed}",
                                     "pieces in one row, congratulations."))
            """ ---------- """

            """ Search diagonals. """
            # Search diagonal from left to right.
            if 0 <= row + i < self.size:  # Avoid overflow.
                if 0 <= col + i < self.size:  # Avoid overflow.
                    if self.position[row+i][col+i] == piece:
                        pieces_lr += 1
                    else:
                        pieces_lr = 0

                # Search diagonal from right to left.
                if 0 <= col - i < self.size:  # Avoid overflow.
                    if self.position[row+i][col-i] == piece:
                        pieces_rl += 1
                    else:
                        pieces_rl = 0

                if pieces_lr >= self.win_needed or pieces_rl >= self.win_needed:
                    return ' '.join((f"{player_name} (player with {piece} pieces) won by having {self.win_needed}",
                                     "pieces in one diagonal, congratulations."))
            """ --------------- """

    def print_board(self):
        """ Prints current position. """

        for i in range(self.size):

            # Stores individual pieces in current row to print. If there's no pieces on square, stores ' '.
            v = [' ' if x == 0 else x for x in self.position[i]]

            """ Printing first 2 rows of the board. """
            if i == 0:
                # Printing numbers above the board which indicates index of column.
                for j in range(self.size):
                    q = len(str(j + 1))
                    print(" " * int(3-q) + f"{j + 1} ", end='')
                print()
                print("----" * len(self.position) + "-")
            """ ----------------------------------- """

            """ For printing all rows that contain pieces. """
            for j in range(self.size):
                if j == 0:
                    print(f"|", end='')
                print(f" {v[j]} |", end='')  # Printing pieces.
                if j == self.size - 1:
                    print(f" {i + 1}", end='')  # Printing numbers indicating squares for the players.
            """ -------------------------------------------- """

            """ Printing bottom borders of board """
            print()
            print("----" * len(self.position) + "-")
            """ -------------------------------- """

        print()


class Player:
    """ Template for creating and managing player1 and player2. """

    def __init__(self, name, piece, wins):
        """
        :param name: Name of player we want to create.
        :param piece: Which piece has the player (X or O).
        :param wins: How many games the player won.
        """

        self.name = name
        self.piece = piece
        self.wins = wins

    def add_win(self):

        self.wins += 1

    def print_score(self):

        print(f"{self.name} ({self.piece}): {self.wins} wins")


def assign_pieces(name1):
    """
    Assigns to player1 and player2 pieces according to the choice of player1.

    :param name1: Name of player1.
    :return: piece1, piece2: assigned pieces.
    """

    while True:
        piece1 = input(f"{name1} (player1), Do you want to be X or O?:\n").upper()

        if piece1 != 'X' and piece1 != 'O':
            print("Wrong format.\n")
            continue

        break

    if piece1 == 'X':
        piece2 = 'O'
    else:
        piece2 = 'X'

    return piece1, piece2


def get_board_size():
    """
    Asks player to choose the size of board until it's in correct form.

    :return: Size of board.
    """

    while True:
        try:
            size_board = int(input("Choose size of the board (3+):\n"))
        except ValueError:
            print("Wrong input / not integer\n")
            continue
        if size_board <= 2:
            print("Too small... Please select board of size 3 and more\n")
            continue
        break

    return size_board


def get_player_move(piece_on_move, name_on_move, size_board, moves_played, print_board):
    """
    Asks for player to make a move. Next it checks if the move is playable

    :param piece_on_move: Piece of the player on move (X or O).
    :param name_on_move: Name of player on move.
    :param size_board: Size of board.
    :param moves_played: All moves which have been played so far to avoid rewriting a piece.
    :param print_board: Function of class Board, which prints a board after execution.

    :return: row and column of correct / playable move made by player.
    """

    while True:
        print("To make a move, you have to provide row and column separated\n"
              "by space [row col], rows and columns starts at 1.\n\n"
              f"{name_on_move}, please make a move (player with {piece_on_move} pieces):\n", end='')
        try:
            row, col = map(int, input().rstrip().split())
        except ValueError:
            print_board()
            print("Incorrect form of move, please make sure it's in form -> row column separated by space.\n")
            continue

        # to index arrays
        row -= 1
        col -= 1

        print_board()

        if (row < 0 or row >= size_board) or (col < 0 or col >= size_board):
            print("Square doesn't exist / out of borders.\n")
            continue

        if [row, col] in moves_played:
            print("There's already piece on the square.\n")
            continue

        break

    return row, col


def start_again():
    """
    Asks player to start a game again.

    :return True if player chooses to play game again.
            False if player wants to stop playing.
    """

    while True:
        again = input("Start again? (y/n):\n").lower()
        if again == 'y' or again == 'yes' or again == 'n' or again == 'no':
            break
        else:
            print("Wrong input, expected y/n\n")

    if again == 'n' or again == 'no':
        return False

    return True


def play_game(player1, player2,  size_board):
    """
    Handles whole playing logic with help of various functions.

    Randomly decides which player should start first. Then prints a board, plays a move and checks if the game
    has ended in loop. Loops until all moves have been played, in that case declares draw. Updates wins in player1
    and player2 if the game wasn't drawn.

    :param player1: Instance of the class Player. Player1 doesn't mean he has to start first.
    :param player2: Another instance of class Player.
    :return: Nothing.
    """

    board = Board(size_board)

    # randomly assign who starts first
    starts_first = randint(1, 2)

    print("Randomly assigning who starts first...")
    if starts_first == 1:
        print(f"{player1.name} with pieces {player1.piece} starts first.\n")
    else:
        print(f"{player2.name} with pieces {player2.piece} starts first.\n")

    for i in range(size_board ** 2):

        print("Current score is:")
        player1.print_score()
        player2.print_score()
        print()

        board.print_board()

        if (i % 2 == 0 and starts_first == 1) or (i % 2 == 1 and starts_first == 2):  # player1 on move
            piece_on_move = player1.piece
            name_on_move = player1.name
        else:  # player2 on move
            piece_on_move = player2.piece
            name_on_move = player2.name

        if i == 0:
            print(f"Having {board.win_needed} pieces in order wins")
            print()

        # gets row and column of lastly played move
        row, col = get_player_move(piece_on_move, name_on_move, size_board, board.moves_played, board.print_board)

        print('\n' * 100)  # clear the console

        board.make_move(row, col, piece_on_move)

        if board.has_ended(row, col, piece_on_move, name_on_move):  # we have a winner

            board.print_board()
            print(board.has_ended(row, col, piece_on_move, name_on_move) + '\n')  # print message

            # add a win
            if name_on_move == player1.name:
                player1.add_win()
            else:
                player2.add_win()

            return

    board.print_board()
    print("Looks like the game ended in draw (booring).\n")


if __name__ == '__main__':

    name1 = input("Please enter your name player1:\n")
    name2 = input("Please enter your name player2:\n")
    piece1, piece2 = assign_pieces(name1)  # get who starts and get other player

    player1 = Player(name=name1, piece=piece1, wins=0)
    player2 = Player(name=name2, piece=piece2, wins=0)

    playing = True

    while playing:
        size_board = get_board_size()  # get size of board user wants to have

        play_game(player1, player2, size_board)  # starts playing game

        print("Current score is:")
        player1.print_score()
        player2.print_score()
        print()

        if not start_again():  # start game again or end game
            playing = False

    print(f"Game ended with score:")
    player1.print_score()
    player2.print_score()
    print()

    if player1.wins > player2.wins:
        print(f"Player {player1.name} won, congratulations.\n")
    elif player1.wins == player2.wins:
        print("Game ended in draw.\n")
    else:
        print(f"Player {player2.name} won, congratulations.\n")

    print("Thanks for playing!")

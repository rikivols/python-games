from random import choice


class Card:
    """
    Create a new card
    """
    suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
    ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
    values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10,
              'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

    def __init__(self):

        self.suit = choice(self.suits)
        self.rank = choice(self.ranks)

    def get_card_value(self):
        """ return the value of card """

        return self.values[self.rank]

    def get_card(self):
        """ return whole card """

        return [self.rank, self.suit]


class Deck:
    """
    class that holds all cards stores their values, checks if the game has already ended.

    Args: has_move - who is on move 1 - human, 0 - bot
    """

    def __init__(self, has_move):

        self.has_move = has_move
        self.player_deck_val = 0
        self.bot_deck_val = 0
        self.player_cards = []
        self.bot_cards = []

    def hit(self):
        """
        Give new card

        :return: updates player_deck_val and bot_deck_val
        """

        # prevent having card already used
        while True:
            card = Card()
            if card.get_card() not in self.player_cards and card.get_card() not in self.bot_cards:
                break

        card_value = card.get_card_value()

        # add card to deck
        if self.has_move == 1:
            self.player_cards.append(card.get_card())
        else:
            self.bot_cards.append(card.get_card())

        # add card value to deck
        if self.has_move == 1:
            # Ace can have values: 1 or 11
            if card_value == 11 and self.player_deck_val + 11 > 21:
                self.player_deck_val += 1
            else:
                self.player_deck_val += card_value
        else:
            if card_value == 11 and self.bot_deck_val + 11 > 21:
                self.bot_deck_val += 1
            else:
                self.bot_deck_val += card_value

    def check_lose(self):
        """ Checks if someones deck exceeded 21, therefore whenever he lost """

        if self.player_deck_val > 21:
            return True

        if self.bot_deck_val > 21:
            return True

    def get_cards(self, player):

        if player == 1:
            return self.player_cards
        else:
            return self.bot_cards

    def print_cards(self):
        """ A simple function that prints the deck (cards) of player or bot (who has move) """

        if self.has_move == 1:
            print("Your cards:")
            for i in self.get_cards(1):
                print(i)

            print(f"Your deck: {self.player_deck_val}")
            print()
        else:
            print("Bot's cards:")
            for i in self.get_cards(0):
                print(i)

            print(f"Bot's deck: {self.bot_deck_val}")
            print()


def play_game(num_of_player_wins, num_of_bot_wins):
    """ Simulates game between opponents, initializes game and handles game logic"""

    player_lost = False

    def get_input():
        """
        Asks for input from player

        :return True - get new input, False - stop asking for input
        """

        inp = ''
        while inp != "hit" and inp != "stay":
            inp = input("Do you want to hit or stay? (hit / stay): ").lower().strip()

        if inp == "hit":
            return True

        return False

    def declare_winner(num_of_player_wins, num_of_bot_wins):

        if player.player_deck_val > bot.bot_deck_val:
            print("Player's deck is greater, congratulations, you won the game.")
            num_of_player_wins += 1
        elif player.player_deck_val == bot.bot_deck_val:
            print("Looks like a draw, huh.")
        else:
            print("Bot's deck is greater, bot won the game.")
            num_of_bot_wins += 1

        return num_of_player_wins, num_of_bot_wins

    def end_game():

        print()
        print(f"Player wins: {num_of_player_wins}     Bot wins: {num_of_bot_wins}")

        if num_of_player_wins > num_of_bot_wins:
            print("Good job, you're winning.")

        elif num_of_player_wins == num_of_bot_wins:
            print("It's draw, wanna beat the bot?")

        else:
            print("C'mon, do you really want to be beat by a bot?")

    # initialize game
    player = Deck(1)
    bot = Deck(0)
    player.hit()
    player.hit()
    player.print_cards()

    """
    --------------------------- Making moves --------------------------------
    """

    # player plays
    while get_input():
        player.hit()
        player.print_cards()

        if player.check_lose():  # check if player's deck exceeded 21 (he lost)
            player.print_cards()
            num_of_bot_wins += 1
            print("Player's deck exceeded 21, bot won the game")
            end_game()
            return num_of_player_wins, num_of_bot_wins

    # bot plays
    if not player_lost:  # it's useless for bot to play if player had already lost
        print("\n"*100)
        print("Bot plays...")
        bot.hit()
        bot.hit()

        while bot.bot_deck_val < 17:  # bot stops hitting when it has 17 and more deck value
            bot.hit()

            if bot.check_lose():  # check if bot's deck exceeded 21 (he lost)
                num_of_player_wins += 1
                print("Bot's deck exceeded 21, bot won the game")
                end_game()
                return num_of_player_wins, num_of_bot_wins

    """
    ------------------------------------------------------------------------
    """

    """
    ------------------ Print message who won, end game ---------------------
    """

    player.print_cards()
    bot.print_cards()

    num_of_player_wins, num_of_bot_wins = declare_winner(num_of_player_wins, num_of_bot_wins)

    end_game()

    return num_of_player_wins, num_of_bot_wins


if __name__ == '__main__':

    num_of_player_wins = 0
    num_of_bot_wins = 0
    end = "yes"

    while end != 'n' and end != 'no':
        if end == "yes" or end == "y":
            num_of_player_wins, num_of_bot_wins = play_game(num_of_player_wins, num_of_bot_wins)
        end = input("Continue playing? y / n: ").lower().strip()

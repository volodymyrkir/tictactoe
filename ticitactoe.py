"""This module includes some logic to be extended for tictactoe game"""
# pylint: disable=too-few-public-methods, logging-fstring-interpolation, import-error
import math
from abc import ABC, abstractmethod
from random import choice
from log import get_logger

logger = get_logger()


class Player:
    """Class that implements Player entity with it's main logic """

    def __init__(self, name):
        self.name = name
        self.streak = 0

    @staticmethod
    def do_move(field):
        """Static method, that makes a move for particular player"""
        while True:
            try:
                move = int(input())
            except ValueError:
                print("Input CORRECT number")
                continue
            if move < 1 or move > 9:
                print("Input number is range [1,9]")
                continue
            if not field.is_free(move - 1):
                print("This cell is already filled, try another one")
                continue
            return move - 1


class View(ABC):
    """Base class for GUI"""

    def __init__(self, field):
        self.field = field

    @abstractmethod
    def show_board(self):
        """Might show board in some gui"""

    @abstractmethod
    def print_instructions(self, name1, name2):
        """Prints instructions for different GUI"""

    @abstractmethod
    def get_game_choice(self):
        """Asks user to continue the game"""

    @abstractmethod
    def get_menu_choice(self):
        """Returns user's choice in main menu"""

    @abstractmethod
    def init_loop(self):
        """Initiates main menu loop for GUIs"""


class TerminalView(View):
    """Implements base class for GUI in terminal"""

    def show_board(self):
        """Renders playground's view"""
        tab = "    "
        counter = 2
        label_counter = 1
        print(" ", end=tab)
        for i in range(int(math.sqrt(self.field.size))):
            print(str(i + 1) + tab, end="")
        for i in range(self.field.size):
            if counter == 2:
                print("\n" + str(label_counter) + tab + self.field.field[i] + tab, end="")
                label_counter += 1
                counter = 0
            else:
                print(self.field.field[i] + tab, end="")
                counter += 1
        print("\n")

    def print_instructions(self, name1, name2):
        """Prints instructions for terminal GUI"""
        print(f"X-PLAYER is {name1}, O-PLAYER is {name2}")
        print("""Game started!
Enter numbers from 1 to 9 according to this scheme:
        1 2 3 
        4 5 6 
        7 8 9\n""")

    def get_game_choice(self):
        """Gets user's choice for continuing the game"""
        print("Would you like to take a revenge?\n1.Yes\n2.No")
        while True:
            try:
                i = int(input())
            except ValueError:
                print("Input correct number!")
                continue
            if i < 1 or i > 2:
                print("Input number in range [1,2]")
                continue
            return i

    def get_menu_choice(self):
        """Gets user option to interact with menu"""
        while True:
            try:
                i = int(input())
            except ValueError:
                print("Enter correct value!")
                continue
            if i < 1 or i > 4:
                print("Enter correct number!")
                continue
            return i

    def init_loop(self):
        """Main menu looping method with some options to choose"""
        while True:
            print("""Welcome to main menu!Select one of the options:
1.New Game
2.Show win log file
3.Clear win log file
4.Exit""")
            menu_choice = self.get_menu_choice()
            if menu_choice == 1:  # Why is there no switch in Python???
                print("Enter Nickname of player 1:", end="")
                name1 = str(input())
                player1 = Player(name1)
                print("Enter Nickname of player 2:", end="")
                name2 = str(input())
                player2 = Player(name2)
                new_game = GameLoop(player1, player2, self.field, self)
                new_game.new_game()
            elif menu_choice == 2:
                with open("wins.log", "r", encoding="utf-8") as file:
                    for line in file.readlines():
                        print(line)
            elif menu_choice == 3:
                with open("wins.log", "w", encoding="utf-8"):
                    pass
                logger.warning("Log file cleared")
            else:
                break


class Field:  # Логика проверки поля
    """Class that implements playground for tictactoe"""
    last_play = 0

    def __init__(self, size):
        self.field = [" " for i in range(size)]
        self.size = size

    def check_all(self, symbol, size):
        """Checks whether there is a win combination"""
        field_size = int(math.sqrt(size))
        return (self.check_diagonal(symbol, field_size)
                or self.check_column(symbol, field_size)
                or self.check_row(symbol, field_size))

    def check_column(self, symbol: str, field_size: int):
        """Checks whether there is a win combination on any column"""
        for i in range(field_size):
            column_slice = self.field[i:int(field_size ** 2) - field_size + i + 1:field_size]
            if len(set(column_slice)) == 1 and column_slice[0] == symbol:
                return True
        return False

    def check_row(self, symbol: str, field_size: int):
        """Checks whether there is a win combination on any row"""
        for i in range(field_size):
            row_slice = self.field[i * field_size:i * field_size + field_size]
            if len(set(row_slice)) == 1 and row_slice[0] == symbol:
                return True
        return False

    def check_diagonal(self, symbol: str, field_size):
        """Checks whether there is a win combination on any diagonal"""
        first_diag_slice = self.field[0:int(field_size ** 2):field_size + 1]
        second_diag_slice = self.field[field_size - 1:int(field_size ** 2)
                                                      - field_size + 1:field_size - 1]
        first_cond = len(set(first_diag_slice)) == 1 and first_diag_slice[0] == symbol
        second_cond = len(set(second_diag_slice)) == 1 and second_diag_slice[0] == symbol
        return first_cond or second_cond

    def get_possible_moves(self):
        """Returns list of possible moves"""
        return [position for position in self.field if position == " "]

    def make_move(self, position, turn_char):
        """Makes a move"""
        self.field[position] = turn_char
        self.last_play = position

    def undo(self):
        """Returns state of game to prev. move"""
        self.field[self.last_play] = " "

    def draw_check(self):
        """Checks whether there is a draw combination on field"""
        return not self.field.__contains__(" ")

    def refresh_game(self):
        """Sets field gaps to default values"""
        for i in enumerate(self.field):
            self.field[i[0]] = " "

    def is_free(self, cell):
        """Checks whether particular cell is free"""
        return self.field[cell] == " "


class GameLoop:
    """Class, that implements looping over particular game"""
    x_move = True

    def __init__(self, player1: Player, player2: Player, field: Field, view: View):
        self.xplayer = choice([player1, player2])
        self.oplayer = player1 if player2 == self.xplayer else player2
        self.field = field
        self.view = view

    def new_game(self):
        """Main game-loop method"""
        self.view.print_instructions(self.xplayer.name, self.oplayer.name)
        game = True
        while game:
            self.view.show_board()
            if self.x_move:  # Логика, если ходит Х
                print(f"{self.xplayer.name}`s (X) turn.")
                move = self.xplayer.do_move(self.field)
                self.field.field[move] = "X"
                if self.field.check_all("X", self.field.size):  # Если Х победил
                    self.view.show_board()
                    if self.oplayer.streak >= 1 or self.xplayer.streak >= 1:  # Если идёт партия
                        logger.info(f"Score is now {self.xplayer.streak + 1}"
                                    f" --- {self.oplayer.streak}")
                    logger.info(f"{self.xplayer.name} (X) Wins!!!")
                    game = False
                    self.xplayer.streak += 1
            else:
                print(f"{self.oplayer.name}`s (O) turn.")
                move = self.oplayer.do_move(self.field)
                self.field.field[move] = "O"
                if self.field.check_all("O", self.field.size):
                    self.view.show_board()
                    if self.oplayer.streak >= 1 or self.xplayer.streak >= 1:  # Если идёт партия
                        logger.info(f"Score is now {self.xplayer.streak}"
                                    f" --- {self.oplayer.streak + 1}")
                    logger.info(f"{self.oplayer.name} (O) Wins!!!")
                    game = False
                    self.oplayer.streak += 1
            if self.field.draw_check():  # Если ничья
                logger.info(f"Friendship between {self.xplayer.name}"
                            f" and {self.oplayer.name} wins!")
                game = False
            self.x_move = not self.x_move
        game_choice = self.view.get_game_choice()
        if game_choice == 1:
            score = f"Current score: {self.xplayer.name} {self.xplayer.streak} --- " \
                    f"{self.oplayer.streak} {self.oplayer.name}"
            if self.oplayer.streak > 1 or self.xplayer.streak > 1:
                logger.info(f"Game goes on! Current score: {score}")
            else:
                logger.info(f"Game started! Current score: {score}")
            self.field.refresh_game()
            self.new_game()

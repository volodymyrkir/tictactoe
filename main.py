"""This module is a main module for tictactoe package"""
# pylint: disable=import-error
from ticitactoe import Field
from ui_tictactoe import PygameView


def main():
    """Main method to init tictactoe game"""
    PygameView(Field(9)).init_loop()


if __name__ == "__main__":
    main()

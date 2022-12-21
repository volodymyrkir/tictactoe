"""This module is a main module for tictactoe package"""
from ticitactoe import TerminalView, Field
from ui_tictactoe import PygameView

def main():
    """Main method to init tictactoe game"""
    PygameView(Field(9)).init_loop()


main()

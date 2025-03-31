""" Module containing the main function for running the scrabble game """

import arcade
from modules import ScrabbleUI, config
from ui import StartScreen, WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE

def main():
    """ Method to run the scrabble game """

    window = arcade.Window(config.WINDOW_WIDTH, config.WINDOW_HEIGHT, config.WINDOW_TITLE)
    # window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

    start_screen = StartScreen()  # Start with the start screen

    window.show_view(start_screen)

    arcade.run()

if __name__ == '__main__':
    main()
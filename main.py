""" Module containing the main function for running the scrabble game """

import arcade
from modules import StartScreen, config

def main():
    """ Method to run the scrabble game """
    window = arcade.Window(config.WINDOW_WIDTH, config.WINDOW_HEIGHT, config.WINDOW_TITLE)

    start_screen = StartScreen()  # Start with the start screen

    window.show_view(start_screen)

    arcade.run()

if __name__ == '__main__':
    main()

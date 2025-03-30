""" Module containing the main function for running the scrabble game """

import arcade
from modules import ScrabbleUI, config

def main():
    """ Method to run the scrabble game """

    window = arcade.Window(config.WINDOW_WIDTH, config.WINDOW_HEIGHT, config.WINDOW_TITLE)

    scrabble = ScrabbleUI()

    window.show_view(scrabble)

    arcade.run()

if __name__ == '__main__':
    main()

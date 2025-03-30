""" Module containing several config values for various modules """

import arcade

WINDOW_WIDTH, WINDOW_HEIGHT = arcade.get_display_size()
WINDOW_TITLE = "Scrabble"
BOARD_SIZE = min(WINDOW_WIDTH, WINDOW_HEIGHT) * 0.6
ROWS = 15
COLS = 15
TILE_SIZE = int(BOARD_SIZE / 15)
TILE_GAP = TILE_SIZE * 0.1
DOCK_SIZE_X = BOARD_SIZE
DOCK_SIZE_Y = int(BOARD_SIZE)
BORDER_X = (WINDOW_WIDTH - BOARD_SIZE) // 2
BORDER_Y = (WINDOW_HEIGHT - BOARD_SIZE) // 2

with open("./assets/dictionary.csv", "r", encoding='utf-8') as file:
    DICTIONARY = {line.strip() for line in file}

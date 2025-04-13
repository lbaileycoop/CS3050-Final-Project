"""Module containing several config values for various modules"""

import arcade
import pygtrie

WINDOW_WIDTH, WINDOW_HEIGHT = arcade.get_display_size()
WINDOW_TITLE = "Scrabble"
BOARD_SIZE = min(WINDOW_WIDTH, WINDOW_HEIGHT) * 0.6
SIZE = 15
TILE_SIZE = int(BOARD_SIZE / 15)
TILE_GAP = TILE_SIZE * 0.1
DOCK_SIZE_X = BOARD_SIZE
DOCK_SIZE_Y = int(BOARD_SIZE)
BORDER_X = (WINDOW_WIDTH - BOARD_SIZE) // 2
BORDER_Y = (WINDOW_HEIGHT - BOARD_SIZE) // 2

# Position constants for dynamic graphics
BOARD_START_X = BORDER_X
BOARD_START_Y = BORDER_Y * 1.5
RACK_TILE_SPACING = BOARD_SIZE // 6
BUTTON_X = WINDOW_WIDTH - BORDER_X * 0.6
BOARD_CENTER_X = 7 * (TILE_SIZE + TILE_GAP) + BORDER_X
BOARD_CENTER_Y = (SIZE - 8) * (TILE_SIZE + TILE_GAP) + BORDER_Y * 1.5

BOARD_BACKGROUND = BOARD_CENTER_X - 7, BOARD_CENTER_Y
TURN_DISP_BACKGROUND = WINDOW_WIDTH * 0.13, WINDOW_HEIGHT + 30
SCOREBOARD_BACKGROUND = WINDOW_WIDTH * 0.13, WINDOW_HEIGHT * 0.58
LETTER_DIST_BACKGROUND = WINDOW_WIDTH * 0.87, WINDOW_HEIGHT * 0.58
RACK_BACKGROUND = WINDOW_WIDTH // 2, BORDER_Y * 0.8

BACKGROUND_COORDS: dict[str, tuple[float, float]] = {
    "board": BOARD_BACKGROUND,
    "turn_display": TURN_DISP_BACKGROUND,
    "scoreboard": SCOREBOARD_BACKGROUND,
    "letter_dist": LETTER_DIST_BACKGROUND,
    "rack": RACK_BACKGROUND,
}

LETTER_DIST = "\
A - 9     J - 1     S - 4  \
--------------------------- \
    B - 2     K - 1     T - 6 \
--------------------------- \
    C - 2     L - 4     U - 4 \
--------------------------- \
    D - 4     M - 2     V - 2 \
--------------------------- \
    E - 12    N - 6     W - 2 \
--------------------------- \
    F - 2     O - 8     X - 1 \
--------------------------- \
    G - 3     P - 2     Y - 2 \
--------------------------- \
    H - 2     Q - 1     Z - 1 \
--------------------------- \
    I - 9   R - 6   Blank - 2"

ALPHABET = {
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
}

DICTIONARY = pygtrie.CharTrie()
with open("./assets/dictionary.csv", "r", encoding="utf-8") as file:
    for line in file:
        DICTIONARY[line.strip()] = True

""" Module containing utility functions for other modules """

from typing import Tuple
from itertools import permutations, combinations

from .config import ROWS, COLS, DICTIONARY
from .tile import Tile

def to_coords(index: int) -> Tuple[int, int]:
    """Returns the x and y values of a tile based on the 1-d index"""
    return (index % COLS, (index // COLS))

def from_coords(x: int, y: int) -> Tuple[int, int]:
    """Returns the 1-d index of a tile based on the x and y values"""
    return x + ((ROWS - y) * COLS)

def valid_word(word: str) -> bool:
    """ Retruns True if the word exists in the dictionary, false otherwise """
    return DICTIONARY.has_key(word)

def tiles_to_str(tiles: list[Tile]) -> str:
    """ Returns the corresponding string created by a list of tiles """
    return ''.join([tile.letter for tile in tiles])
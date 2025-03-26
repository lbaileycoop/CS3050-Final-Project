from .config import *
from typing import Tuple
from itertools import permutations, combinations

def to_coords(index: int) -> Tuple[int, int]:
    """Returns the x and y values of a tile based on the 1-d index"""
    return (index % COLS, (index // COLS))

def from_coords(x: int, y: int) -> Tuple[int, int]:
    """Returns the 1-d index of a tile based on the x and y values"""
    return x + ((ROWS - y) * COLS)

def valid_word(word):
    """ Retruns True if the word exists in the dictionary, false otherwise """
    return word in DICTIONARY

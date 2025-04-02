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

def get_possible_words(input_string: str = "", num_free_letters: int = 0):
    """ 
    Gets valid words that can be formed with the given letters (tiles)
    Can be used for AI to decide a move for them to play
    
    Attributes: 
        input_string (str): collection of letters to find valid words for
        num_free_letters (int): the number of free letters (blank tiles) to add to the search
    Returns:
        list of all valid words that can be formed from the given letters/tiles
    """
    def get_permutations(s):
        return set(''.join(p) for p in permutations(s))

    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm' \
                'n', 'o', 'p' 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    words = set()

    free_letter_combinations = set()
    if num_free_letters > 0:
        for free_letters in combinations(alphabet, num_free_letters):
            free_letter_combinations.add(''.join(free_letters))
    else:
        free_letter_combinations.add("")

    for free_letters in free_letter_combinations:
        available_letters = input_string + free_letters

        n = len(available_letters)
        for length in range(2, n + 1):
            for subset in combinations(available_letters, length):
                subset_str = ''.join(subset)
                for perm in get_permutations(subset_str):
                    if valid_word(perm):
                        words.add(perm)

    return list(words)

def tiles_to_str(tiles: list[Tile]) -> str:
    """ Returns the corresponding string created by a list of tiles """
    return ''.join([tile.letter for tile in tiles])

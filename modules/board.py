""" Module containing the definition for a Board object """

from .tile import Tile, TILES
from .utils import valid_word


TW = TILES['triple_word']
DW = TILES['double_word']
TL = TILES['triple_letter']
DL = TILES['double_letter']
BA = TILES['base']
ST = TILES['star']

ORIGINAL_BOARD = [
            [TW, BA, BA, DL, BA, BA, BA, TW, BA, BA, BA, DL, BA, BA, TW],
            [BA, DW, BA, BA, BA, TL, BA, BA, BA, TL, BA, BA, BA, DW, BA],
            [BA, BA, DW, BA, BA, BA, DL, BA, DL, BA, BA, BA, DW, BA, BA],
            [DL, BA, BA, DW, BA, BA, BA, DL, BA, BA, BA, DW, BA, BA, DL],
            [BA, BA, BA, BA, DW, BA, BA, BA, BA, BA, DW, BA, BA, BA, BA],
            [BA, TL, BA, BA, BA, TL, BA, BA, BA, TL, BA, BA, BA, TL, BA],
            [BA, BA, DL, BA, BA, BA, DL, BA, DL, BA, BA, BA, DL, BA, BA],
            [TW, BA, BA, DL, BA, BA, BA, ST, BA, BA, BA, DL, BA, BA, TW],
            [BA, BA, DL, BA, BA, BA, DL, BA, DL, BA, BA, BA, DL, BA, BA],
            [BA, TL, BA, BA, BA, TL, BA, BA, BA, TL, BA, BA, BA, TL, BA],
            [BA, BA, BA, BA, DW, BA, BA, BA, BA, BA, DW, BA, BA, BA, BA],
            [DL, BA, BA, DW, BA, BA, BA, DL, BA, BA, BA, DW, BA, BA, DL],
            [BA, BA, DW, BA, BA, BA, DL, BA, DL, BA, BA, BA, DW, BA, BA],
            [BA, DW, BA, BA, BA, TL, BA, BA, BA, TL, BA, BA, BA, DW, BA],
            [TW, BA, BA, DL, BA, BA, BA, TW, BA, BA, BA, DL, BA, BA, TW],
        ]

class Board():
    """
    Class representing the Scrabble board

    Attributes:
        Board (list(Tile)) : 2D list representing the board's current state
    """
    def __init__(self):
        """ Initialize a Board object """
        self.current_turn_tiles = []

        # 2D list to store the current board state
        self.board = ORIGINAL_BOARD

    def get_board(self):
        """ Getter function for the current Board """
        return self.board

    def update_tile(self, x: int, y: int, tile: Tile):
        """ Function to update a tile in the board """
        self.board[y][x] = tile

    def remove_tile(self, x: int, y: int):
        """ 
        Function to remove tiles from the board
            
        Only used on player's turn to allow changing of tiles
        """
        self.board[y][x] = ORIGINAL_BOARD[y][x]
        to_remove = None
        for placed_tile in self.current_turn_tiles:
            if placed_tile[0] == x and placed_tile[1] == y:
                to_remove = placed_tile
                break

        if to_remove:
            self.current_turn_tiles.remove(to_remove)

        return self.board[y][x]

    def get_current_turn_tiles(self):
        """ Getter function for the list of tiles placed this turn """
        return self.current_turn_tiles

    def clear_current_turn_tiles(self):
        """ Clears the tiles placed this turn """
        self.current_turn_tiles = []

    def get_word_score(self, placed_tiles):
        """ Calculate the score for a word play """

        score = 0
        word_multiplier = 1

        word = ""
        for x, y, tile in placed_tiles:
            letter_score = tile.value
            letter_multiplier = 1

            # Check for letter multipliers
            special_tile = ORIGINAL_BOARD[y][x]
            if special_tile == DL:
                letter_multiplier = 2
            elif special_tile == TL:
                letter_multiplier = 3
            elif special_tile in [DW, ST]:
                word_multiplier *= 2
            elif special_tile == TW:
                word_multiplier *= 3

            score += letter_score * letter_multiplier

            word += tile.letter

        #validate word
        if not valid_word(word):
            return False

        return score * word_multiplier

    def get_tile_at(self, row, col):
        """ Returns the tile at the given coordinates """
        return self.board[row][col]

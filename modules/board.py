""" Module containing the definition for a Board object """

from .tile import Tile, TILES
from .utils import valid_word
from typing import Tuple


TW = TILES['triple_word']
DW = TILES['double_word']
TL = TILES['triple_letter']
DL = TILES['double_letter']
BA = TILES['base']
ST = TILES['star']
EMPTY_TILES = [TW, DW, TL, DL, BA, ST]

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
        board (list(Tile)) : 2D list representing the board's current state
        current_turn_tiles (list((Tile, (int, int)))) : list containing all tiles placed this turn,
                                                        and the coords they were placed at
        first_turn (bool) : tracks if this is the first turn of the game
    """
    def __init__(self):
        """ Initialize a Board object """
        self.current_turn_tiles = []
        self.first_turn = True

        # 2D list to store the current board state
        self.board = [
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

    def get_board(self):
        """ Getter function for the current Board """
        return self.board
    
    def set_board(self, new_board):
        """ Setter function for the board """
        self.board = [[None for _ in range(15)] for _ in range(15)]
        for row in range(15):
            for col in range(15):
                self.board[row][col] = new_board[row][col]
    
        self.clear_current_turn_tiles()

    def update_tile(self, x: int, y: int, tile: Tile):
        """ Function to update a tile in the board """
        self.board[y][x] = tile
        self.current_turn_tiles.append((tile, (y, x)))

    def remove_tile(self, x: int, y: int):
        """ 
        Function to remove tiles from the board
            
        Only used on player's turn to allow changing of tiles
        """
        self.board[y][x] = ORIGINAL_BOARD[y][x]
        to_remove = None
        for placed_tile in self.current_turn_tiles:
            tile, (row, col) = placed_tile
            if row == y and col == x:
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

    def validate_turn(self):
        """ Validate turn and calculate its score 
        
        output:
            word (str): The word that were formed during the turn # Should be changed to a list of strings for when multiple words are created in a single turn
            is_valid (bool): True/False whether the turn is valid or not
            score (int): The score total for this turn
        """
        # TODO
        # currently just placeholders here, the function needs to be completely implemented
        # Needs to validate word by:
        # 1. Ensuring words are placed in a straight line
        # 2. Ensuring words are connected to other played words (except for first turn)
        # 3. Getting ALL words created, in the case that 2 or more are created in a single turn
        # 4. Validating all words against the dictionary
        # 5. Properly calculating score (the current implementation does not work)
        # 6. Dealing with blank tiles
        # Doesn't all have to be done in this one function

        word = ""

        if not self.current_turn_tiles:
            return False, 0
            
        total_score = 0
        for tile, (row, col) in self.current_turn_tiles:
            letter_score = tile.value
            word += tile.letter
            letter_multiplier = 1
            word_multiplier = 1
            
            special_tile = ORIGINAL_BOARD[row][col]
            if special_tile == DL:
                letter_multiplier = 2
            elif special_tile == TL:
                letter_multiplier = 3
            elif special_tile == DW or special_tile == ST:
                word_multiplier = 2
            elif special_tile == TW:
                word_multiplier = 3
            
            tile_score = letter_score * letter_multiplier * word_multiplier
            total_score += tile_score
        
        self.clear_current_turn_tiles()
        self.first_turn = False
            
        return word, True, total_score

    def get_tile_at(self, row, col):
        """ Returns the tile at the given coordinates """
        return self.board[row][col]

    def get_turn_score(self):
        """
        Calculate the total score for the current turn
        
        Returns:
            tuple: (is_valid, score) - boolean indicating if the turn is valid and the total score
        """
        return self.validate_turn()
""" Module containing the definition for a Board object """

from .tile import Tile, TILES
from .utils import valid_word, tiles_to_str


TW = TILES['triple_word']
DW = TILES['double_word']
TL = TILES['triple_letter']
DL = TILES['double_letter']
BA = TILES['base']
ST = TILES['star']
EMPTY_TILES = [TW, DW, TL, DL, BA, ST]
CENTER_COORDS = (7, 7)

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

ALPHABET = {'a','b','c','d','e','f',
            'g','h','i','j','k','l',
            'm','n','o','p','q','r',
            's','t','u','v','v','w',
            'x','y','z'}

CROSS_CHECKS_DOWN = [[ALPHABET for _ in range(len(ORIGINAL_BOARD))] for _ in range(len(ORIGINAL_BOARD))]
CROSS_CHECKS_ACROSS = [[ALPHABET for _ in range(len(ORIGINAL_BOARD))] for _ in range(len(ORIGINAL_BOARD))]

class Board():
    """
    Class representing the Scrabble board

    Attributes:
        board (list(list(Tile))) : 2D list representing the board's current state
        current_turn_tiles (list(Tile)) : list containing all tiles placed this turn
    """
    def __init__(self):
        """ Initialize a Board object """
        self.current_turn_tiles: list[Tile] = []

        # 2D list to store the current board state
        self.board: list[list[Tile]] = ORIGINAL_BOARD

    def get_board(self):
        """ Getter function for the current Board """
        return self.board

    def update_tile(self, row: int, col: int, tile: Tile):
        """ Function to update a tile in the board """
        self.board[row][col] = tile
        tile.coords = (row, col)
        self.current_turn_tiles.append(tile)

    def remove_tile(self, row: int, col: int):
        """ 
        Function to remove tiles from the board
            
        Only used on player's turn to allow changing of tiles
        """
        self.board[row][col] = ORIGINAL_BOARD[row][col]
        to_remove = None
        for placed_tile in self.current_turn_tiles:
            if placed_tile[0] == col and placed_tile[1] == row:
                to_remove = placed_tile
                break

        if to_remove:
            self.current_turn_tiles.remove(to_remove)

        return self.board[row][col]

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
        for row, col, tile in placed_tiles:
            letter_score = tile.value
            letter_multiplier = 1

            # Check for letter multipliers
            special_tile = ORIGINAL_BOARD[row][col]
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

    def get_tile_at(self, row: int, col: int):
        """ Returns the tile at the given coordinates """
        return self.board[row][col]

    def validate_turn(self) -> bool:
        """ Returns a list of all words created by the placed tiles """

        def find_center(coords: tuple[int, int], visited: list[tuple[int, int]]):
            """ 
            Searches the board using depth-first search to ensure that the tile 
            at the given coordinates can eventually trace back to the center tile
            """

            if coords == CENTER_COORDS:
                return True
            if coords in visited:
                return False

            visited.append(coords)
            found = False
            row = coords[0]
            col = coords[1]

            if (-1 < row+1 < len(self.board) and -1 < col < len(self.board[0])
                and self.get_tile_at(row+1, col) not in EMPTY_TILES):
                found = found or find_center((coords[0]+1, coords[1]), visited)
            if (-1 < row-1 < len(self.board) and -1 < col < len(self.board[0])
                and self.get_tile_at(row-1, col) not in EMPTY_TILES):
                found = found or find_center((coords[0]-1, coords[1]), visited)
            if (-1 < row < len(self.board) and -1 < col+1 < len(self.board[0])
                and self.get_tile_at(row, col+1) not in EMPTY_TILES):
                found = found or find_center((coords[0], coords[1]+1), visited)
            if (-1 < row < len(self.board) and -1 < col+1 < len(self.board[0])
                and self.get_tile_at(row, col-1) not in EMPTY_TILES):
                found = found or find_center((coords[0], coords[1]-1), visited)

            return found

        words_are_valid = True
        connects_to_center = True
        tiles_in_line = True

        for i, tile in enumerate(self.current_turn_tiles):
            coords = tile.coords

            connects_to_center = connects_to_center and find_center(tile.coords, [])

            if i > 0:
                tiles_in_line = tiles_in_line and (coords[0] == self.current_turn_tiles[i-1].coords[0] or
                                                   coords[1] == self.current_turn_tiles[i-1].coords[1])


        words = self.find_words()
        if len(words) == 0:
            words_are_valid = False

        for word in words:
            words_are_valid = words_are_valid and valid_word(tiles_to_str(word))

        return (words_are_valid and
                connects_to_center and 
                tiles_in_line)
    
    def find_words(self) -> list[list[Tile]]:
        words = []
        for tile in self.current_turn_tiles:
            coords = tile.coords

            down_word = (self.find_string(coords, -1, 0)[::-1] + 
                         self.find_string(coords, 1, 0)[1:])
            across_word = (self.find_string(coords, 0, -1)[::-1] + 
                           self.find_string(coords, 0, 1)[1:])

            if len(down_word) > 1 and down_word not in words:
                words.append(down_word)
            if len(across_word) > 1 and across_word not in words:
                words.append(across_word)
        
        return words


    def find_string(self, coords: tuple[int, int], drow: int, dcol: int):
            """ 
            Searches the board in a specified direction, and 
            adds all tiles to a list until an empty tile is found 
            """

            row = coords[0]
            col = coords[1]
            letters = []
            tile = self.get_tile_at(row, col)
            while not tile in EMPTY_TILES:
                letters.append(tile)
                row += drow
                col += dcol
                if -1 < row < len(self.board) and -1 < col < len(self.board[0]):
                    tile = self.get_tile_at(row, col)
                else:
                    break

            return letters

    def update_cross_checks(self):
        """ Updates the cross-check lists whenever a move is played """
        words = self.find_words()

        for tile in self.current_turn_tiles:
            coords = tile.coords

            if self.current_turn_tiles[0].coords[0] - self.current_turn_tiles[-1].coords[0] == 0:
                across = True
            else:
                across = False

            if across:
                CROSS_CHECKS_ACROSS[coords[0]][coords[1]] = []
                
                if coords[0]-1 > -1:
                    CROSS_CHECKS_ACROSS[
                        coords[0]-1][coords[1]] = {letter for letter in ALPHABET 
                                                if valid_word(letter+
                                                                tiles_to_str(self.find_string(coords, 1, 0))[0])}
                if coords[0]+1 < len(self.board):
                    CROSS_CHECKS_ACROSS[
                        coords[0]+1][coords[1]] = {letter for letter in ALPHABET
                                                if valid_word(tiles_to_str(self.find_string(coords, -1, 0))[::-1]+
                                                                letter)}
            
            if not across or len(self.current_turn_tiles) == 1:
                CROSS_CHECKS_DOWN[coords[0]][coords[1]] = []
                
                if coords[1]-1 > -1:
                    CROSS_CHECKS_DOWN[
                        coords[0]][coords[1]-1] = {letter for letter in ALPHABET
                                                if valid_word(letter+
                                                                tiles_to_str(self.find_string(coords, 0, 1)))}
                if coords[1]+1 < len(self.board[0]):
                    CROSS_CHECKS_DOWN[
                        coords[0]][coords[1]+1] = {letter for letter in ALPHABET
                                                if valid_word(tiles_to_str(self.find_string(coords, 0, -1))[::-1]+
                                                                letter)}

        for word in words:
            if word[1].coords[0] - word[0].coords[0] == 0:
                across = True
                row = word[1].coords[0]
            else:
                across = False
                col = word[1].coords[1]

            if across:
                if word[0].coords[1]-1 > -1:
                    CROSS_CHECKS_ACROSS[row][word[0].coords[1]-1] = []
                if word[-1].coords[1]+1 < len(self.board[0]):
                    CROSS_CHECKS_ACROSS[row][word[-1].coords[1]+1] = []
            else:
                if word[0].coords[0]-1 > -1:
                    CROSS_CHECKS_DOWN[word[0].coords[0]-1][col] = []
                if word[-1].coords[0]+1 < len(self.board):
                    CROSS_CHECKS_DOWN[word[-1].coords[0]+1][col] = []

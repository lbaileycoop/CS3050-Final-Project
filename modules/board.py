""" Module containing the definition for a Board object """

from .tile import Tile, TILES
from .utils import valid_word


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

ALPHABET = ['a','b','c','d','e','f',
            'g','h','i','j','k','l',
            'm','n','o','p','q','r',
            's','t','u','v','v','w',
            'x','y','z']

CROSS_CHECKS_DOWN = [[ALPHABET * len(ORIGINAL_BOARD)] * len(ORIGINAL_BOARD)]
CROSS_CHECKS_ACROSS = [[ALPHABET * len(ORIGINAL_BOARD)] * len(ORIGINAL_BOARD)]

class Board():
    """
    Class representing the Scrabble board

    Attributes:
        board (list(Tile)) : 2D list representing the board's current state
        current_turn_tiles (list((Tile, (int, int)))) : list containing all tiles placed this turn,
                                                        and the coords they were placed at
    """
    def __init__(self):
        """ Initialize a Board object """
        self.current_turn_tiles = []
        self.current_turn_coords = []

        # 2D list to store the current board state
        self.board = ORIGINAL_BOARD

    def get_board(self):
        """ Getter function for the current Board """
        return self.board

    def update_tile(self, x: int, y: int, tile: Tile):
        """ Function to update a tile in the board """
        self.board[y][x] = tile
        self.current_turn_tiles.append(tile)
        self.current_turn_coords.append((y, x))

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

    def validate_turn(self, is_first_turn=False):
        """ Returns a list of all words created by the placed tiles """

        def find_center(coords, visited):
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
            x = coords[0]
            y = coords[1]

            if (-1 < x+1 < len(self.board) and -1 < y < len(self.board[0])
                and self.get_tile_at(x+1, y) not in EMPTY_TILES):
                found = found or find_center((coords[0]+1, coords[1]), visited)
            if (-1 < x-1 < len(self.board) and -1 < y < len(self.board[0])
                and self.get_tile_at(x-1, y) not in EMPTY_TILES):
                found = found or find_center((coords[0]-1, coords[1]), visited)
            if (-1 < x < len(self.board) and -1 < y+1 < len(self.board[0])
                and self.get_tile_at(x, y+1) not in EMPTY_TILES):
                found = found or find_center((coords[0], coords[1]+1), visited)
            if (-1 < x < len(self.board) and -1 < y+1 < len(self.board[0])
                and self.get_tile_at(x, y-1) not in EMPTY_TILES):
                found = found or find_center((coords[0], coords[1]-1), visited)

            return found


        def search_dir(coords, dx, dy):
            """ 
            Searches the board in a specified direction, and 
            adds all tiles to a list until an empty tile is found 
            """

            x = coords[0]
            y = coords[1]
            letters = ''
            tile = self.get_tile_at(x, y)
            while not tile in EMPTY_TILES:
                letters += tile.letter
                x += dx
                y += dy
                if -1 < x < len(self.board)and -1 < y < len(self.board[0]):
                    tile = self.get_tile_at(x, y)
                else:
                    break

            return letters

        words_are_valid = True
        connects_to_center = True
        tiles_in_line = True

        words = []

        for i, coords in enumerate(self.current_turn_coords):

            connects_to_center = connects_to_center and find_center(coords, [])

            if i > 1:
                if not (coords[0] == self.current_turn_coords[i-1][0] or
                        coords[1] == self.current_turn_coords[i-1][1]):
                    tiles_in_line = False

            x_word = search_dir(coords, -1, 0)[::-1] + search_dir(coords, 1, 0)[1:]
            y_word = search_dir(coords, 0, -1)[::-1] + search_dir(coords, 0, 1)[1:]

            if len(x_word) > 1 and x_word not in words:
                words.append(x_word)
            if len(y_word) > 1 and y_word not in words:
                words.append(y_word)

        for word in words:
            if not valid_word(word):
                words_are_valid = False

        if is_first_turn:
            return (words, words_are_valid, connects_to_center,
                    tiles_in_line, len(self.current_turn_tiles) > 1)
        return words, words_are_valid and connects_to_center and tiles_in_line

    def update_cross_checks(self, across):
        """ Updates the cross-check lists whenever a move is played """

        # TODO: update cross checks at the end of each played word
        for i, coords in enumerate(self.current_turn_coords):
            if across:
                CROSS_CHECKS_ACROSS[
                    coords[0]-1, coords[1]] = {letter for letter in ALPHABET 
                                               if valid_word(letter+self.search_dir(coords, 0, 1))}
                CROSS_CHECKS_ACROSS[
                    coords[0]+1, coords[1]] = {letter for letter in ALPHABET
                                               if valid_word(self.search_dir(coords, 0, -1)[::-1]+letter)}
            else:
                CROSS_CHECKS_DOWN[
                    coords[1]-1, coords[0]] = {letter for letter in ALPHABET
                                               if valid_word(letter+self.search_dir(coords, 1, 0))}
                CROSS_CHECKS_DOWN[
                    coords[1]+1, coords[0]] = {letter for letter in ALPHABET
                                               if valid_word(self.search_dir(coords, -1, 0)[::-1]+letter)}

        
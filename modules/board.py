"""Module containing the definition for a Board object"""

from .tile import Tile, TILES
from .utils import valid_word, tiles_to_str


TW = TILES["triple_word"]
DW = TILES["double_word"]
TL = TILES["triple_letter"]
DL = TILES["double_letter"]
BA = TILES["base"]
ST = TILES["star"]
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


class Board:
    """
    Class representing the Scrabble board

    Attributes:
        board (list(list(Tile))) : 2D list representing the board's current state
        current_turn_tiles (list(Tile)) : list containing all tiles placed this turn
    """

    def __init__(self):
        """Initialize a Board object"""
        self.current_turn_tiles: list[Tile] = []

        # 2D list to store the current board state
        self.board: list[list[Tile]] = [
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

    def get_board(self) -> list[list[Tile]]:
        """Getter function for the current Board"""
        return self.board

    def set_board(self, new_board: list[list[Tile]]):
        """Setter function for the board"""
        self.board = [[None for _ in range(15)] for _ in range(15)]
        for row in range(15):
            for col in range(15):
                self.board[row][col] = new_board[row][col]

        self.clear_current_turn_tiles()

    def update_tile(self, row: int, col: int, tile: Tile):
        """Function to update a tile in the board"""
        self.board[row][col] = tile
        tile.coords = (row, col)
        self.current_turn_tiles.append(tile)

    def remove_current_tile(self, tile: Tile):
        """Removes a given tile from the board and from current turn tiles"""
        row = tile.coords[0]
        col = tile.coords[1]

        self.board[row][col] = ORIGINAL_BOARD[row][col]
        self.current_turn_tiles.remove(tile)

    def clear_current_turn_tiles(self):
        """Clears the tiles placed this turn"""
        while len(self.current_turn_tiles) > 0:
            self.remove_current_tile(self.current_turn_tiles[0])

    def get_current_turn_tiles(self) -> list[Tile]:
        """Getter function for the list of tiles placed this turn"""
        return self.current_turn_tiles

    def reset_current_turn_tiles(self):
        """Sets current_turn_tiles back to an empty list for a new turn"""
        self.current_turn_tiles = []

    def play_turn(self) -> tuple[bool, dict[str, int]]:
        """Performs the logic for attempting to play a turn"""
        words = self.find_words()

        words_dict: dict[str, int] = {}
        legal_turn = self.validate_turn(words)

        if legal_turn:
            words_dict = self.score_words(words)
            self.reset_current_turn_tiles()

        return legal_turn, words_dict

    def score_words(self, words: list[list[Tile]]) -> dict[str, int]:
        """Returns a dict matching every word in words to its score"""
        words_dict: dict[str, int] = {}

        for word in words:
            words_dict[tiles_to_str(word)] = self.score_word(word)

        return words_dict

    def score_word(self, word: list[Tile]) -> int:
        """Returns the score for a played word"""
        word_score = 0
        word_multiplier = 1

        for tile in word:
            row = tile.coords[0]
            col = tile.coords[1]

            letter_multiplier = 1

            letter_score = tile.value

            if tile in self.current_turn_tiles:
                # If tile was played this turn, check for multipliers
                board_location = ORIGINAL_BOARD[row][col]

                if board_location == DL:
                    letter_multiplier *= 2
                elif board_location == TL:
                    letter_multiplier *= 3
                elif board_location in (DW, ST):
                    word_multiplier *= 2
                elif board_location == TW:
                    word_multiplier *= 3

            word_score += letter_score * letter_multiplier

        return word_score * word_multiplier

    def get_tile_at(self, row: int, col: int) -> Tile:
        """Returns the tile at the given coordinates"""
        return self.board[row][col]

    def validate_turn(self, words) -> bool:
        """Returns true if the played tiles makes a valid turn, otherwise False"""

        def find_center(
            coords: tuple[int, int], visited: list[tuple[int, int]]
        ) -> bool:
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

            if (
                -1 < row + 1 < len(self.board)
                and -1 < col < len(self.board[0])
                and self.get_tile_at(row + 1, col) not in EMPTY_TILES
            ):
                found = found or find_center((coords[0] + 1, coords[1]), visited)
            if (
                -1 < row - 1 < len(self.board)
                and -1 < col < len(self.board[0])
                and self.get_tile_at(row - 1, col) not in EMPTY_TILES
            ):
                found = found or find_center((coords[0] - 1, coords[1]), visited)
            if (
                -1 < row < len(self.board)
                and -1 < col + 1 < len(self.board[0])
                and self.get_tile_at(row, col + 1) not in EMPTY_TILES
            ):
                found = found or find_center((coords[0], coords[1] + 1), visited)
            if (
                -1 < row < len(self.board)
                and -1 < col + 1 < len(self.board[0])
                and self.get_tile_at(row, col - 1) not in EMPTY_TILES
            ):
                found = found or find_center((coords[0], coords[1] - 1), visited)

            return found

        words_are_valid = True
        connects_to_center = True
        tiles_in_line = True

        for i, tile in enumerate(self.current_turn_tiles):
            coords = tile.coords

            connects_to_center = connects_to_center and find_center(tile.coords, [])

            if i > 0:
                tiles_in_line = tiles_in_line and (
                    coords[0] == self.current_turn_tiles[i - 1].coords[0]
                    or coords[1] == self.current_turn_tiles[i - 1].coords[1]
                )

        if len(words) == 0:
            words_are_valid = False

        for word in words:
            words_are_valid = words_are_valid and valid_word(tiles_to_str(word))

        return words_are_valid and connects_to_center and tiles_in_line

    def find_words(self) -> list[list[Tile]]:
        """Finds all words created by the current turn"""
        words: list[list[Tile]] = []
        for tile in self.current_turn_tiles:
            coords = tile.coords

            down_word: list[Tile] = (
                self.find_string(coords, -1, 0)[::-1]
                + self.find_string(coords, 1, 0)[1:]
            )
            across_word: list[Tile] = (
                self.find_string(coords, 0, -1)[::-1]
                + self.find_string(coords, 0, 1)[1:]
            )

            if len(down_word) > 1 and down_word not in words:
                words.append(down_word)
            if len(across_word) > 1 and across_word not in words:
                words.append(across_word)

        return words

    def find_string(self, coords: tuple[int, int], drow: int, dcol: int) -> list[Tile]:
        """
        Searches the board in a specified direction, and
        adds all tiles to a list until an empty tile is found
        """

        row = coords[0]
        col = coords[1]
        letters: list[Tile] = []
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

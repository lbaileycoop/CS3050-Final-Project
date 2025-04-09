"""Module containing the definition for a Board object"""

from .tile import Tile, TILES
from .config import ALPHABET, ROWS, COLS
from .utils import valid_word, tiles_to_str, copy_list
from .player import Player


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

CROSS_CHECKS_ACROSS = [[ALPHABET for _ in range(COLS)] for _ in range(ROWS)]
CROSS_CHECKS_DOWN = [[ALPHABET for _ in range(ROWS)] for _ in range(COLS)]


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
        """Sets the tile at the passed coordinates to the passed tile"""
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

    def reset_blanks(self):
        """Changes any blank tiles placed this turn back into blanks"""
        for tile in self.current_turn_tiles:
            if tile.value == 0:
                tile.reset_blank()

    def get_current_turn_tiles(self) -> list[Tile]:
        """Getter function for the list of tiles placed this turn"""
        return self.current_turn_tiles

    def reset_current_turn_tiles(self):
        """Sets current_turn_tiles back to an empty list for a new turn"""
        self.current_turn_tiles = []

    def play_turn(self, player: Player) -> tuple[bool, dict[str, int]]:
        """Performs the logic for attempting to play a turn"""
        words = self.find_words()

        words_dict: dict[str, int] = {}
        legal_turn = self.validate_turn(words)

        if legal_turn:
            words_dict = self.score_words(words)
            self.update_cross_checks()
            self.reset_current_turn_tiles()
        else:
            self.reset_blanks()
            player.add_tiles(self.get_current_turn_tiles())
            self.clear_current_turn_tiles()

        return legal_turn, words_dict

    def test_turn(
        self, move: list[tuple[Tile, tuple[int, int]]]
    ) -> tuple[bool, dict[str, int]]:
        """Performs the logic for testing if a turn is legal"""
        backup_board = copy_list(self.board)

        for tile in move:
            self.update_tile(tile[1][0], tile[1][1], tile[0])

        words = self.find_words()

        words_dict: dict[str, int] = {}
        legal_turn = self.validate_turn(words)

        if legal_turn:
            words_dict = self.score_words(words)

        self.board = backup_board

        self.clear_current_turn_tiles()

        return legal_turn, sum(words_dict.values())

    def score_words(self, words: list[list[Tile]]) -> dict[str, int]:
        """Returns a dict matching every word in words to its score"""
        words_dict: dict[str, int] = {}

        for word in words:
            words_dict[tiles_to_str(word)] = self.score_word(word)

        if len(self.current_turn_tiles) == 7:
            words_dict["BINGO!!!"] = 50

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
                and -1 < col - 1 < len(self.board[0])
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

    def update_cross_checks(self):
        """Updates the cross-check lists for whenever a move is played"""

        self.update_cross_checks_letters()
        self.update_cross_checks_words()

    def update_cross_checks_letters(self):
        """Updates the cross-check lists parralel to every letter played"""
        for tile in self.get_current_turn_tiles():
            coords = tile.coords

            across = bool(
                self.get_current_turn_tiles()[0].coords[0]
                - self.get_current_turn_tiles()[-1].coords[0]
            )

            if across:
                CROSS_CHECKS_ACROSS[coords[0]][coords[1]] = []

                if coords[0] - 1 > -1:
                    CROSS_CHECKS_ACROSS[coords[0] - 1][coords[1]] = {
                        letter
                        for letter in ALPHABET
                        if valid_word(
                            letter + tiles_to_str(self.find_string(coords, 1, 0))[0]
                        )
                    }

                if coords[0] + 1 < ROWS:
                    CROSS_CHECKS_ACROSS[coords[0] + 1][coords[1]] = {
                        letter
                        for letter in ALPHABET
                        if valid_word(
                            tiles_to_str(self.find_string(coords, -1, 0))[::-1] + letter
                        )
                    }

            if not across or len(self.get_current_turn_tiles()) == 1:
                CROSS_CHECKS_DOWN[coords[0]][coords[1]] = []

                if coords[1] - 1 > -1:
                    CROSS_CHECKS_DOWN[coords[0]][coords[1] - 1] = {
                        letter
                        for letter in ALPHABET
                        if valid_word(
                            letter + tiles_to_str(self.find_string(coords, 0, 1))
                        )
                    }
                if coords[1] + 1 < COLS:
                    CROSS_CHECKS_DOWN[coords[0]][coords[1] + 1] = {
                        letter
                        for letter in ALPHABET
                        if valid_word(
                            tiles_to_str(self.find_string(coords, 0, -1))[::-1] + letter
                        )
                    }

    def update_cross_checks_words(self):
        """Updates the cross-check lists perpendicular to every word played"""
        words = self.find_words()

        for word in words:
            row, col = 0, 0
            if word[1].coords[0] - word[0].coords[0] == 0:
                across = True
                row = word[1].coords[0]
            else:
                across = False
                col = word[1].coords[1]

            if across:
                if word[0].coords[1] - 1 > -1:
                    CROSS_CHECKS_ACROSS[row][word[0].coords[1] - 1] = []
                if word[-1].coords[1] + 1 < COLS:
                    CROSS_CHECKS_ACROSS[row][word[-1].coords[1] + 1] = []
            else:
                if word[0].coords[0] - 1 > -1:
                    CROSS_CHECKS_DOWN[word[0].coords[0] - 1][col] = []
                if word[-1].coords[0] + 1 < ROWS:
                    CROSS_CHECKS_DOWN[word[-1].coords[0] + 1][col] = []

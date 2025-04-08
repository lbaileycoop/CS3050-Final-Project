"""Module that contains the definition for an AI object"""

from .config import ROWS, COLS, ALPHABET
from .board import Board, EMPTY_TILES
from .rack import Rack
from .tile import Tile
from .utils import valid_word, tiles_to_str, find_permutations_recursive, copy_list

CROSS_CHECKS_ACROSS = [[ALPHABET for _ in range(COLS)] for _ in range(ROWS)]
CROSS_CHECKS_DOWN = [[ALPHABET for _ in range(ROWS)] for _ in range(COLS)]


class AI:
    """TODO"""

    def __init__(self, board: Board, rack: Rack):
        self.board = board
        self.rack = rack

    def update_cross_checks(self):
        """Updates the cross-check lists for whenever a move is played"""

        self.update_cross_checks_letters()
        self.update_cross_checks_words()

    def update_cross_checks_letters(self):
        """Updates the cross-check lists parralel to every letter played"""
        for tile in self.board.get_current_turn_tiles():
            coords = tile.coords

            across = bool(
                self.board.get_current_turn_tiles()[0].coords[0]
                - self.board.get_current_turn_tiles()[-1].coords[0]
            )

            if across:
                CROSS_CHECKS_ACROSS[coords[0]][coords[1]] = []

                if coords[0] - 1 > -1:
                    CROSS_CHECKS_ACROSS[coords[0] - 1][coords[1]] = {
                        letter
                        for letter in ALPHABET
                        if valid_word(
                            letter
                            + tiles_to_str(self.board.find_string(coords, 1, 0))[0]
                        )
                    }

                if coords[0] + 1 < ROWS:
                    CROSS_CHECKS_ACROSS[coords[0] + 1][coords[1]] = {
                        letter
                        for letter in ALPHABET
                        if valid_word(
                            tiles_to_str(self.board.find_string(coords, -1, 0))[::-1]
                            + letter
                        )
                    }

            if not across or len(self.board.get_current_turn_tiles()) == 1:
                CROSS_CHECKS_DOWN[coords[0]][coords[1]] = []

                if coords[1] - 1 > -1:
                    CROSS_CHECKS_DOWN[coords[0]][coords[1] - 1] = {
                        letter
                        for letter in ALPHABET
                        if valid_word(
                            letter + tiles_to_str(self.board.find_string(coords, 0, 1))
                        )
                    }
                if coords[1] + 1 < COLS:
                    CROSS_CHECKS_DOWN[coords[0]][coords[1] + 1] = {
                        letter
                        for letter in ALPHABET
                        if valid_word(
                            tiles_to_str(self.board.find_string(coords, 0, -1))[::-1]
                            + letter
                        )
                    }

    def update_cross_checks_words(self):
        """Updates the cross-check lists perpendicular to every word played"""
        words = self.board.find_words()

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

    def across_moves(
        self,
    ) -> list[list[tuple[Tile, tuple[int, int]]]]:
        possible_moves: list[list[tuple[Tile, tuple[int, int]]]] = []

        for row in range(len(self.board.get_board())):
            possible_moves += self.moves_in_row(row)

        return possible_moves

    def moves_in_row(self, row: int) -> list[list[tuple[Tile, tuple[int, int]]]]:
        possible_moves: list[list[tuple[Tile, tuple[int, int]]]] = []

        letters_in_row = tiles_to_str(
            tile for tile in self.board.get_board()[row] if tile not in EMPTY_TILES
        )

        possible_words = find_permutations_recursive(
            "".join(self.rack.get_rack_letters()) + letters_in_row, []
        )
        feasable_words = []

        if letters_in_row != "":
            for word in possible_words:
                for letter in letters_in_row:
                    if letter in word:
                        feasable_words.append(word)
        elif row == 7:
            feasable_words = possible_words

        for word in feasable_words:
            first_letter = word[0]

            for col in range(COLS - len(word)):
                tile = self.board.get_tile_at(row, col)

                if (
                    tile.letter == first_letter
                    and col + len(word) <= COLS
                    or tile in EMPTY_TILES
                ):
                    move = self.find_word(
                        word, (row, col), [], copy_list(self.rack.get_rack())
                    )
                    if move is not None and move not in possible_moves:
                        possible_moves.append(move)

        return possible_moves

    def find_word(
        self,
        target: str,
        coords: tuple[int, int],
        curr: list[tuple[Tile, tuple[int, int]]],
        remaining_rack: list[Tile],
    ):

        if target == "":
            return curr

        if coords is None:
            return None

        square = self.board.get_tile_at(coords[0], coords[1])
        next_letter = target[0]
        remaining_rack = copy_list(remaining_rack)
        curr = copy_list(curr)

        if square not in EMPTY_TILES:
            if square.letter == next_letter:
                return self.find_word(
                    target[1:],
                    self.next_coords(coords),
                    curr,
                    remaining_rack,
                )
            return None

        if next_letter in CROSS_CHECKS_ACROSS[coords[0]][coords[1]]:
            for tile in remaining_rack.copy():
                if next_letter == tile.letter:
                    curr.append((tile, coords))
                    remaining_rack.remove(tile)
                    return self.find_word(
                        target[1:],
                        self.next_coords(coords),
                        curr,
                        remaining_rack,
                    )
        return None

    def next_coords(self, coords: tuple[int, int]) -> tuple[int, int] | None:
        """
        Returns the coordinates of the next square in the row, or
        None if passed square is the end of the row
        """
        if coords[1] + 1 < COLS:
            return (coords[0], coords[1] + 1)
        return None
